# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.guild import Guild


async def guild_update_listener(self, gateway, payload: dict):
    new_guild = Guild.from_dict(payload)
    old_guild = self.guilds.get(new_guild.id)

    self.guilds[new_guild.id] = new_guild

    await self.dispatch("on_guild_update", (old_guild, new_guild))

    return


def export() -> Coro:
    return guild_update_listener
