# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio

from ..utils.types import Coro
from ..models.guild import Guild


async def guild_create_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    guild_was_cached_as_none = False

    guild = Guild.from_dict(payload)

    if self.guilds.get(guild.id, "empty") != "empty":
        guild_was_cached_as_none = True

    self.guilds[guild.id] = guild

    custom_listener = self._events.get("on_guild_create")

    if custom_listener is not None and guild_was_cached_as_none is False:
        asyncio.ensure_future(custom_listener(guild))

    return


def export() -> Coro:
    return guild_create_listener
