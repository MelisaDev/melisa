# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio

from ..utils.types import Coro
from ..models.guild import Guild


async def guild_update_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    new_guild = Guild.from_dict(payload)
    old_guild = self.guilds.get(new_guild.id)

    self.guilds[new_guild.id] = new_guild

    custom_listener = self._events.get("on_guild_update")

    if custom_listener is not None:
        asyncio.ensure_future(custom_listener(old_guild, new_guild))

    return


def export() -> Coro:
    return guild_update_listener
