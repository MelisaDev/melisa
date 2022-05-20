# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.guild.channel import ChannelType, _choose_channel_type


async def channel_delete_listener(self, gateway, payload: dict):
    payload.update({"type": ChannelType(payload.pop("type"))})

    channel = _choose_channel_type(payload)

    await self.dispatch("on_channel_delete", (channel,))

    return


def export() -> Coro:
    return channel_delete_listener
