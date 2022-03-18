# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio

from ..utils.types import Coro
from ..models.user import User


async def on_ready_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    guilds = payload.get("guilds")

    self.guilds = dict(map(lambda i: (i["id"], None), guilds))
    self.user = User.from_dict(payload.get("user"))

    custom_listener = self._events.get("on_shard_ready")

    if custom_listener is not None:
        asyncio.ensure_future(custom_listener(gateway.shard_id))

    return


def export() -> Coro:
    return on_ready_listener
