# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import asyncio
import logging
import sys
import zlib
import time
from asyncio import ensure_future
from dataclasses import dataclass
from typing import Dict, Any

import aiohttp

from ..exceptions import GatewayError, PrivilegedIntentsRequired, LoginFailure
from ..listeners import listeners
from ..models.user import Activity
from ..utils import APIModelBase, json

_logger = logging.getLogger("melisa.gateway")


@dataclass
class GatewayBotInfo(APIModelBase):
    """Gateway info from the `gateway/bot` endpoint"""

    url: str
    shards: int
    session_start_limit: dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        self: GatewayBotInfo = super().__new__(cls)

        self.url = data.get("url")
        self.shards = data.get("shards")
        self.session_start_limit = data.get("session_start_limit")

        return self


class Gateway:

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

    def __init__(self, client, shard_id: int = 0, num_shards: int = 1, **kwargs):
        self.interval = None
        self.intents = client.intents
        self.sequence = None
        self.__session = aiohttp.ClientSession()
        self.session_id = None
        self.client = client
        self.latency = float("inf")
        self.ws = None
        self.loop = asyncio.get_event_loop()
        self.shard_id = shard_id
        self.not_closed = True

        self.__raise_close_codes: Dict[int, Any] = {
            4004: LoginFailure("Token is not valid"),
            4010: GatewayError("Invalid shard"),
            4011: GatewayError("Sharding required"),
            4012: GatewayError("Invalid API version"),
            4013: GatewayError("Invalid intents"),
            4014: PrivilegedIntentsRequired("Disallowed intents"),
        }

        self.listeners = listeners

        self._last_send = 0

        self.auth = {
            "token": self.client._token,
            "intents": self.intents,
            "properties": {
                "$os": sys.platform,
                "$browser": "Discord iOS"
                if kwargs.get("mobile") is not None
                else "MelisaPy",
                "$device": "Melisa Python Library",
            },
            "compress": True,
            "shard": [shard_id, num_shards],
            "presence": self.generate_presence(
                kwargs.get("start_activity"), kwargs.get("start_status")
            ),
        }

        self._zlib: zlib._Decompress = zlib.decompressobj()
        self._buffer: bytearray = bytearray()

    async def connect(self) -> None:
        self.ws = await self.__session.ws_connect(
            "wss://gateway.discord.gg/?v=10&encoding=json&compress=zlib-stream"
        )
        _logger.debug("(Shard %s) Starting...", self.shard_id)

        self._zlib: zlib._Decompress = zlib.decompressobj()
        self._buffer = bytearray()
        self.not_closed = True

        await self.send_identify()
        self.loop.create_task(self.receive())
        await self.check_heartbeating()

    async def check_heartbeating(self):
        while self.not_closed:
            await asyncio.sleep(20)

            if self._last_send + 60.0 < time.perf_counter():
                _logger.warning(
                    "(Shard %s) ack not received. Attempting to reconnect.",
                    self.shard_id,
                )
                await self.ws.close(code=4000)
                await self.handle_close(4000)

    async def send(self, payload: str) -> None:
        _logger.debug("(Shard %s) Sending payload: %s", self.shard_id, payload)
        await self.ws.send_str(payload)

    async def parse_websocket_message(self, msg):
        try:
            if type(msg) is bytes:
                self._buffer.extend(msg)

                if len(msg) < 4 or msg[-4:] != b"\x00\x00\xff\xff":
                    return None
                msg = self._zlib.decompress(self._buffer)
                msg = msg.decode("utf-8")
                self._buffer = bytearray()

            return json.loads(msg)
        except zlib.error:
            return None

    async def handle_data(self, data):
        """Handles received data and process it"""

        _logger.debug(
            "(Shard %s) Data with %s opcode received", self.shard_id, data["op"]
        )

        if data["op"] == self.DISPATCH:
            self.sequence = int(data["s"])

            _logger.debug(
                "(Shard %s) Set sequence number to %s", self.shard_id, data["s"]
            )

            event_type = data["t"].lower()

            event_to_call = self.listeners.get(event_type)

            if event_to_call is not None:
                ensure_future(event_to_call(self.client, self, data["d"]))

        elif data["op"] == self.INVALID_SESSION:
            _logger.debug(
                "(Shard %s) Invalid session, attempting to reconnect", self.shard_id
            )
            await self.ws.close(code=4000)
            await self.handle_close(4000)
        elif data["op"] == self.HELLO:
            await self.send_hello(data)
        elif data["op"] == self.HEARTBEAT_ACK:
            _logger.debug(
                "(Shard %s) received heartbeat ack",
                self.shard_id,
            )
            self.latency = time.perf_counter() - self._last_send
        elif data["op"] == self.RECONNECT:
            _logger.debug(
                "(Shard %s) Requested to reconnect to Discord. "
                "Closing session and attempting to resume",
                self.shard_id,
            )
            await self.close(1012)

    async def receive(self) -> None:
        """Receives and parses received data"""
        while self.not_closed:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = await self.parse_websocket_message(msg.data)
                    if data:
                        await self.handle_data(data)
                elif msg.type == aiohttp.WSMsgType.TEXT:
                    await self.handle_data(msg.data)
                else:
                    raise RuntimeError

            close_code = self.ws.close_code

            if close_code is not None:
                await self.handle_close(close_code)

    async def handle_close(self, code: int) -> None:
        if code == 4009:
            await self.resume()
            return
        else:
            err = self.__raise_close_codes.get(code)

            if err:
                raise err

        _logger.info(
            "(Shard %s) disconnected from the Discord Gateway without any errors. Reconnecting...",
            self.shard_id,
        )

        self.not_closed = False

        await self.connect()

    async def send_heartbeat(self, interval: float) -> None:
        if not self.ws.closed:
            _logger.debug(
                "(Shard %s) Sending next heartbeat in %s", self.shard_id, interval
            )
            await self.send(self.opcode(self.HEARTBEAT, self.sequence))
            self._last_send = time.perf_counter()
            await asyncio.sleep(interval)
            self.loop.create_task(self.send_heartbeat(interval))

    async def close(self, code: int = 4000) -> None:
        if self.ws:
            self.not_closed = False
            await self.ws.close(code=code)

        self._buffer.clear()

    async def send_hello(self, data: Dict) -> None:
        interval = data["d"]["heartbeat_interval"] / 1000
        await asyncio.sleep((interval - 2000) / 1000)
        self.loop.create_task(self.send_heartbeat(interval))

    async def send_identify(self, resume: bool = False) -> None:
        if resume:
            _logger.debug("(Shard %s) Resuming connection with Discord", self.shard_id)

            await self.send(
                self.opcode(
                    self.RESUME,
                    {
                        "token": self.client._token,
                        "session_id": self.session_id,
                        "seq": self.sequence,
                    },
                )
            )
            return

        await self.send(self.opcode(self.IDENTIFY, self.auth))

    async def resume(self) -> None:
        await self.send(
            self.opcode(
                self.RESUME,
                {
                    "token": self.client._token,
                    "session_id": self.session_id,
                    "seq": self.sequence,
                },
            )
        )

    @staticmethod
    def generate_presence(activity: Activity = None, status: str = None):
        data = {"since": time.time() * 1000, "afk": False}

        if activity is not None:
            data["activities"] = [activity.to_dict()]

        if status is not None:
            data["status"] = str(status)

        return data

    async def update_presence(self, data: dict):
        _logger.debug("[Shard %s] Updating presence...", self.shard_id)
        await self.send(self.opcode(self.PRESENCE_UPDATE, data))

    @staticmethod
    def opcode(opcode: int, payload) -> str:
        data = {"op": opcode, "d": payload}
        return json.dumps(data)
