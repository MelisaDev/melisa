# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.guild import Guild


async def guild_create_listener(self, gateway, payload: dict):
    guild_was_cached_as_none = False

    guild = Guild.from_dict(payload)

    if self.cache.get_guild(guild.id) is not None:
        guild_was_cached_as_none = True

    self.cache.set_guild(guild)

    if guild_was_cached_as_none is False:
        await self.dispatch("on_guild_create", (guild,))

    return


def export() -> Coro:
    return guild_create_listener
