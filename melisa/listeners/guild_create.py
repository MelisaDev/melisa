# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro


async def guild_create_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    self.guilds[payload["id"]] = payload

    custom_listener = self._events.get("on_guild_create")

    if custom_listener is not None:
        await custom_listener(payload)  # ToDo: Guild Model

    return


def export() -> Coro:
    return guild_create_listener
