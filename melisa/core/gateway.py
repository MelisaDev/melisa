import json
import asyncio
import zlib
import time
from asyncio import ensure_future
from dataclasses import dataclass
from typing import Dict, Any

import websockets

from ..exceptions import InvalidPayload, GatewayError, PrivilegedIntentsRequired, LoginFailure
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
        self.session_id = None
        self.client = client
        self.shard_id = shard_id
        self.latency = float('inf')
        self.connected = False

        self.__close_codes: Dict[int, Any] = {
            4001: GatewayError("Invalid opcode was sent"),
            4002: InvalidPayload("Invalid payload was sent."),
            4003: GatewayError("Payload was sent prior to identifying"),
            4004: LoginFailure("Token is not valid"),
            4005: GatewayError(
                "Authentication was sent after client already authenticated"
            ),
            4007: GatewayError("Invalid sequence sent when starting new session"),
            4008: GatewayError("Client was rate limited"),
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
                    "$os": "windows",
                    "$browser": "melisa",
                    "$device": "melisa"
                },
                "compress": True,
                "shard": [shard_id, num_shards],
                "presence": self.generate_presence(kwargs.get("start_activity"), kwargs.get("start_status"))
            }

        self._zlib: zlib._Decompress = zlib.decompressobj()
        self._buffer: bytearray = bytearray()

    async def websocket_message(self, msg):
        if type(msg) is bytes:
            self._buffer.extend(msg)

            if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
                return None
            msg = self._zlib.decompress(self._buffer)
            msg = msg.decode('utf-8')
            self._buffer = bytearray()

        return json.loads(msg)

    async def start_loop(self):
        async with websockets.connect(
                f'wss://gateway.discord.gg/?v={self.GATEWAY_VERSION}&encoding=json&compress=zlib-stream') \
                as self.websocket:
            await self.hello()
            if self.interval is None:
                return
            self.connected = True
            await asyncio.gather(self.heartbeat(), self.receive())

    async def close(self, code: int = 1000):
        await self.websocket.close(code=code)

    async def resume(self):
        resume_data = {
            "seq": self.sequence,
            "session_id": self.session_id,
            "token": self.client._token
        }

        await self.send(self.RESUME, resume_data)

    async def receive(self):
        async for msg in self.websocket:
            msg = await self.websocket_message(msg)

            if msg is None:
                return None

            if msg["op"] == self.HEARTBEAT_ACK:
                self.latency = time.time() - self._last_send

            if msg["op"] == self.DISPATCH:
                self.sequence = int(msg["s"])
                event_type = msg["t"].lower()

                event_to_call = self.listeners.get(event_type)

                if event_to_call is not None:
                    await event_to_call(self.client, self, msg["d"])

            if msg["op"] != self.DISPATCH:
                if msg["op"] == self.RECONNECT:
                    await self.websocket.close()
                    await self.resume()

    async def send(self, opcode, payload):
        data = self.opcode(opcode, payload)

        if opcode == self.HEARTBEAT:
            self._last_send = time.time()

        await self.websocket.send(data)

    async def heartbeat(self):
        while self.interval is not None:
            await self.send(self.HEARTBEAT, self.sequence)
            self.connected = True
            await asyncio.sleep(self.interval)

    async def hello(self):
        await self.send(self.IDENTIFY, self.auth)

        ret = await self.websocket.recv()

        data = await self.websocket_message(ret)

        opcode = data["op"]

        if opcode != 10:
            return

        self.interval = (data["d"]["heartbeat_interval"] - 2000) / 1000

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
        await self.send(self.PRESENCE_UPDATE, data)

    @staticmethod
    def opcode(opcode: int, payload) -> str:
        data = {
            "op": opcode,
            "d": payload
        }
        return json.dumps(data)
