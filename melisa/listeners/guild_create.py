# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.guild import Guild


async def guild_create_listener(self, gateway, payload: dict):
    guild_was_cached_as_none = False

    guild = Guild.from_dict(payload)

    if self.guilds.get(guild.id, "empty") != "empty":
        guild_was_cached_as_none = True

    self.guilds[str(guild.id)] = guild

    if guild_was_cached_as_none is False:
        await self.dispatch("on_guild_create", guild)

    return


def export() -> Coro:
    return guild_create_listener
