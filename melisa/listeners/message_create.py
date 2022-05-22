# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..models.message.message import Message
from ..utils.types import Coro


async def message_create_listener(self, gateway, payload: dict):
    message = Message.from_dict(payload)

    self.cache.set_guild_channel_last_message_id(
        message.channel_id, message.guild_id, message.id
    )

    await self.dispatch("on_message_create", (message,))

    return


def export() -> Coro:
    return message_create_listener
