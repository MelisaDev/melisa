# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..models.guild.channel import ChannelType, _choose_channel_type
from ..utils.types import Coro


async def channel_update_listener(self, gateway, payload: dict):
    # ToDo: Replace None to the old channel object (so it requires cache manager)
    channel = _choose_channel_type(payload)
    old_channel = self.cache.get_guild_channel(channel.id)

    # i am not sure that it is needed, but why not
    if channel.type not in [ChannelType.DM, ChannelType.GROUP_DM]:
        self.cache.set_guild_channel(channel)

    await self.dispatch("on_channel_update", (old_channel, channel))

    return


def export() -> Coro:
    return channel_update_listener
