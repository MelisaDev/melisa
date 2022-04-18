# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..models.guild.channel import _choose_channel_type
from ..utils.types import Coro


async def channel_create_listener(self, gateway, payload: dict):
    channel = _choose_channel_type(payload)

    await self.dispatch("on_channel_create", channel)

    return


def export() -> Coro:
    return channel_create_listener
