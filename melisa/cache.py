# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import Enum
from typing import List, Dict, Optional, Any, Union

from .utils.types import UNDEFINED
from .models.guild.guild import Guild, UnavailableGuild
from .models.guild.channel import ChannelType, Channel
from .utils.snowflake import Snowflake


class ChannelsCachingPolicy(Enum):
    """ "Channels caching policy"""

    ALL = "all"
    NONE = "none"
    GUILD_TEXT = 0
    GUILD_VOICE = 2


class CacheManager:
    """ """

    def __init__(
        self,
        *,
        disabled: bool = False,
        policies: Dict[str, List[ChannelsCachingPolicy]] = None,
        auto_unused_attributes: Optional[Dict[Any, List[str]]] = None,
    ):
        self.auto_unused_attributes: Dict[Any, List[str]] = (
            {} if auto_unused_attributes is not None else auto_unused_attributes
        )

        self._raw_guilds: Dict[str, Any] = {}
        self._raw_users: Dict[str, Any] = {}
        self._raw_dm_channels: Dict[str, Any] = {}

        self._disabled = disabled

        # Some default values
        if policies is None:
            policies = {"channels": [ChannelsCachingPolicy.GUILD_TEXT]}

        self._policies = policies

        # We use symlinks to cache guild channels
        # like we save channel in Guild and save it here
        # and if you need channel, and you don't know its guild
        # you can use special method, and it will find it in guild
        self._channel_symlinks: Dict[str, str] = {}

    def guilds_count(self) -> int:
        """Cached Guilds Count"""
        return len(self._raw_guilds)

    def users_count(self) -> int:
        """Cached Users Count"""
        return len(self._raw_users)

    def guild_channels_count(self) -> int:
        """Cached Guild Channels Count"""
        return len(self._channel_symlinks)

    def total_channels_count(self) -> int:
        """Total Cached Channel Count"""
        return len(self._raw_dm_channels) + len(self._channel_symlinks)

    def __remove_unused_attributes(self, model, _type):
        if self.auto_unused_attributes is None:
            self.auto_unused_attributes = {}

        unused_attributes = self.auto_unused_attributes.get(_type)

        if unused_attributes and unused_attributes is not None:
            unused_attributes = unused_attributes.__dict__.keys()

            for attr in unused_attributes:
                model.__delattr__(attr)

        return model

    def set_guild(self, guild: Optional[Guild] = None):
        """
        Save Guild into cache

        Parameters
        ----------
        guild: Optional[`~melisa.models.guild.Guild`]
            Guild to save into cache
        """

        if self._disabled:
            return

        if guild is None:
            return None

        guild = self.__remove_unused_attributes(guild, Guild)

        policy = self._policies["channels"]

        if hasattr(guild, "channels") and ChannelsCachingPolicy.NONE not in policy:
            channels = guild.channels.values()

            if ChannelsCachingPolicy.ALL not in policy:
                policy = [int(x.value) for x in policy]

                channels = filter(
                    lambda channel: channel.type is not None
                    and int(channel.type) in policy,
                    channels,
                )

            for sym in channels:
                sym_id = str(sym.id)
                if self._channel_symlinks.get(sym_id, UNDEFINED) is not UNDEFINED:
                    self._channel_symlinks.pop(sym_id)

                self._channel_symlinks[sym_id] = str(guild.id)
        else:
            if hasattr(guild, "channels"):
                guild.channels = {}

        self._raw_guilds.update({str(guild.id): guild})

        return guild

    def set_guild_channel(self, channel: Optional[Channel] = None):
        """
        Save Guild into cache

        Parameters
        ----------
        channel: Optional[`~melisa.models.guild.Channel`]
            Guild Channel to save into cache
        """

        if self._disabled:
            return

        if channel is None:
            return None

        channel = self.__remove_unused_attributes(
            channel, Channel
        )  # ToDo: add channel type

        guild = self._raw_guilds.get(str(channel.guild_id), UNDEFINED)

        channel_id = str(channel.id)

        if guild != UNDEFINED:
            if hasattr(guild, "channels"):
                self._raw_guilds[str(guild.id)].channels.update({channel_id: channel})

        self._channel_symlinks.update({channel_id: str(channel.guild_id)})

        return channel

    def get_guild_channel(self, channel_id: Union[Snowflake, str, int]):
        """
        Get guild channel from cache

        Parameters
        ----------
        channel_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of guild channel to get from cache.
        """

        if self._disabled:
            return None

        channel_id = str(channel_id)
        guild_id = self._channel_symlinks.get(channel_id, UNDEFINED)

        if guild_id == UNDEFINED:
            return None

        guild = self.get_guild(guild_id)

        if guild is None:
            return None

        if hasattr(guild, "channels") is False:
            return None

        return guild.channels.get(channel_id)

    def get_guild(self, guild_id: Union[Snowflake, str, int]):
        """
        Get guild from cache

        Parameters
        ----------
        guild_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of guild to get from cache.
        """

        if self._disabled:
            return None

        if not isinstance(guild_id, str):
            guild_id = str(guild_id)
        return self._raw_guilds.get(guild_id, None)

    def _set_none_guilds(self, guilds: List[Dict[str, Any]]) -> None:
        """
        Insert None-Guilds to cache

        Parameters
        ----------
        guilds: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            Data of guilds tso insert to the cache
        """

        if self._disabled:
            return

        guilds_dict = dict(
            map(
                lambda i: (str(i["id"]), UnavailableGuild.from_dict(i)),
                guilds,
            )
        )

        self._raw_guilds.update(guilds_dict)
        return None

    def remove_guild(self, guild_id: Union[Snowflake, str, int]):
        """
        Remove guild from cache

        Parameters
        ----------
        guild_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of guild to remove from cache.
        """

        if self._disabled:
            return

        if not isinstance(guild_id, str):
            guild_id = str(guild_id)

        return self._raw_guilds.pop(guild_id, None)

    def remove_guild_channel(self, channel_id: Union[Snowflake, str, int]):
        """
        Remove guild channel from cache

        Parameters
        ----------
        channel_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of guild channel to remove from cache.
        """

        if self._disabled:
            return

        if not isinstance(channel_id, str):
            channel_id = str(channel_id)

        guild_id = str(self._channel_symlinks.pop(channel_id, None))

        if guild_id is None:
            return None

        guild = self.get_guild(guild_id)

        if guild is None:
            return None

        if hasattr(guild, "channels") is False:
            return None

        return guild.channels.pop(channel_id, None)

    def set_guild_channel_last_message_id(
        self,
        channel_id: Union[Snowflake, str, int],
        guild_id: Union[Snowflake, str, int],
        message_id: Union[Snowflake, str, int],
    ):
        """
        Set guild channel last message id

        Parameters
        ----------
        channel_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of channel to set.
        guild_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of guild to set.
        message_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of message to set.
        """
        if not isinstance(channel_id, str):
            channel_id = str(channel_id)

        if not isinstance(guild_id, str):
            guild_id = str(guild_id)

        if not isinstance(message_id, Snowflake):
            message_id = Snowflake(int(message_id))

        guild = self.get_guild(guild_id)

        if guild is None:
            return None

        if hasattr(guild, "channels") is False:
            return None

        if guild.channels.get(channel_id) is None:
            return None

        channel = self._raw_guilds[guild_id].channels[channel_id]

        channel.last_message_id = message_id

        self._raw_guilds[guild_id].channels[channel_id] = channel
