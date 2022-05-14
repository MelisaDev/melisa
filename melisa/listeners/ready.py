# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.user import User


async def on_ready_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    guilds = payload.get("guilds")

    self.cache._set_none_guilds(guilds)

    self.user = User.from_dict(payload.get("user"))

    await self.dispatch("on_shard_ready", (gateway.shard_id, ))

    return


def export() -> Coro:
    return on_ready_listener
