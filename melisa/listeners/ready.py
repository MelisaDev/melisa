# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.user import User


async def on_ready_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    guilds = payload.get("guilds")

    if self._none_guilds_cached is False:
        self.guilds = dict(map(lambda i: (i["id"], None), guilds))
        self._none_guilds_cached = True

    self.user = User.from_dict(payload.get("user"))

    await self.dispatch("on_shard_ready", gateway.shard_id)

    return


def export() -> Coro:
    return on_ready_listener
