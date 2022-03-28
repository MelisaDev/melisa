# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio

from ..utils.types import Coro
from ..models.guild import Channel, ChannelType, channel_types_for_converting


async def channel_create_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    payload.update({"type": ChannelType(payload.pop("type"))})

    channel_cls = channel_types_for_converting.get(payload["type"], Channel)

    channel = channel_cls.from_dict(payload)

    custom_listener = self._events.get("on_channel_create")

    if custom_listener is not None:
        asyncio.ensure_future(custom_listener(channel))

    return


def export() -> Coro:
    return channel_create_listener
