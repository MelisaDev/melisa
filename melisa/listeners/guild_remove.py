# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.guild import UnavailableGuild


async def guild_delete_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    guild = UnavailableGuild.from_dict(payload)

    self.guilds.pop(guild.id, None)

    await self.dispatch("on_guild_remove", guild)

    return


def export() -> Coro:
    return guild_delete_listener
