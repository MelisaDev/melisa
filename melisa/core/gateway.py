import json
import asyncio
import sys
import zlib
import time
from asyncio import ensure_future
from dataclasses import dataclass
from typing import Dict, Any

import aiohttp

from ..exceptions import GatewayError, PrivilegedIntentsRequired, LoginFailure
from ..listeners import listeners
from ..models.user import BotActivity
from ..utils import APIObjectBase


@dataclass
class GatewayBotInfo(APIObjectBase):
    """Gateway info from the `gateway/bot` endpoint"""
    url: str
    shards: int
    session_start_limit: dict


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

    def __init__(self,
                 client,
                 shard_id: int = 0,
                 num_shards: int = 1,
                 **kwargs):

        self.GATEWAY_VERSION = "9"
        self.interval = None
        self.intents = client.intents
        self.sequence = None
        self.__session = aiohttp.ClientSession()
        self.session_id = None
        self.client = client
        self.latency = float('inf')
        self.ws = None
        self.loop = asyncio.get_event_loop()

        self.__raise_close_codes: Dict[int, Any] = {
            4004: LoginFailure("Token is not valid"),
            4010: GatewayError("Invalid shard"),
            4011: GatewayError("Sharding required"),
            4012: GatewayError("Invalid API version"),
            4013: GatewayError("Invalid intents"),
            4014: PrivilegedIntentsRequired("Disallowed intents")
        }

        self.listeners = listeners

        self._last_send = 0

        self.auth = {
                "token": self.client._token,
                "intents": self.intents,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "melisa",
                    "$device": "melisa"
                },
                "compress": True,
                "shard": [shard_id, num_shards],
                "presence": self.generate_presence(kwargs.get("start_activity"), kwargs.get("start_status"))
            }

        self._zlib: zlib._Decompress = zlib.decompressobj()
        self._buffer: bytearray = bytearray()

    async def connect(self) -> None:
        self.ws = await self.__session.ws_connect(
            f'wss://gateway.discord.gg/?v={self.GATEWAY_VERSION}&encoding=json&compress=zlib-stream')

        if self.session_id is None:
            await self.send_identify()
            self.loop.create_task(self.receive())
            await self.check_heartbeating()
        else:
            await self.resume()

    async def check_heartbeating(self):
        await asyncio.sleep(20)

        if self._last_send + 60.0 < time.perf_counter():
            await self.ws.close(code=4000)
            await self.handle_close(4000)

        await self.check_heartbeating()

    async def send(self, payload: str) -> None:
        await self.ws.send_str(payload)

    async def parse_websocket_message(self, msg):
        if type(msg) is bytes:
            self._buffer.extend(msg)

            if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
                return None
            msg = self._zlib.decompress(self._buffer)
            msg = msg.decode('utf-8')
            self._buffer = bytearray()

        return json.loads(msg)

    async def handle_data(self, data):
        if data['op'] == self.DISPATCH:
            self.sequence = int(data["s"])
            event_type = data["t"].lower()

            event_to_call = self.listeners.get(event_type)

            if event_to_call is not None:
                ensure_future(event_to_call(self.client, self, data["d"]))

        elif data['op'] == self.INVALID_SESSION:
            await self.ws.close(code=4000)
            await self.handle_close(4000)
        elif data['op'] == self.HELLO:
            await self.send_hello(data)
        elif data['op'] == self.HEARTBEAT_ACK:
            self.latency = time.perf_counter() - self._last_send

    async def receive(self) -> None:
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
        if close_code is None:
            return
        else:
            await self.handle_close(close_code)

    async def handle_close(self, code: int) -> None:
        if code == 4009:
            await self.resume()
            return
        else:
            err = self.__raise_close_codes.get(code)

            if err:
                raise err

        await self.connect()

    async def send_heartbeat(self, interval: float) -> None:
        if not self.ws.closed:
            await self.send(self.opcode(self.HEARTBEAT, self.sequence))
            self._last_send = time.perf_counter()
            await asyncio.sleep(interval)
            self.loop.create_task(self.send_heartbeat(interval))

    async def close(self, code: int = 4000) -> None:
        if self.ws:
            await self.ws.close(code=code)
        self._buffer.clear()

    async def send_hello(self, data: Dict) -> None:
        interval = data['d']['heartbeat_interval'] / 1000
        await asyncio.sleep((interval - 2000) / 1000)
        self.loop.create_task(self.send_heartbeat(interval))

    async def send_identify(self) -> None:
        await self.send(self.opcode(
            self.IDENTIFY,
            self.auth
        ))

    async def resume(self) -> None:
        await self.send(
            self.opcode(
                self.RESUME,
                {
                    'token': self.client._token,
                    'session_id': self.session_id,
                    'seq': self.sequence,
                }
            )
        )

    @staticmethod
    def generate_presence(activity: BotActivity = None, status: str = None):
        data = {
            "since": time.time() * 1000,
            "afk": False
        }

        if activity is not None:
            activity_to_set = {
                "name": activity.name,
                "type": int(activity.type)
            }

            if int(activity.type) == 1 and activity.url:
                activity_to_set["url"] = activity.url

            data["activities"] = [activity_to_set]

        if status is not None:
            data["status"] = str(status)

        return data

    async def update_presence(self, data: dict):
        await self.send(self.opcode(self.PRESENCE_UPDATE, data))

    @staticmethod
    def opcode(opcode: int, payload) -> str:
        data = {
            "op": opcode,
            "d": payload
        }
        return json.dumps(data)
