# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..utils.types import Coro
from ..models.guild import Channel, ChannelType, channel_types_for_converting


async def channel_create_listener(self, gateway, payload: dict):
    payload.update({"type": ChannelType(payload.pop("type"))})

    channel_cls = channel_types_for_converting.get(payload["type"], Channel)

    channel = channel_cls.from_dict(payload)

    await self.dispatch("on_channel_create", channel)

    return


def export() -> Coro:
    return channel_create_listener
