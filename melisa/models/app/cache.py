# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import Enum
from typing import List, Dict, Optional, Any, Union

from melisa.utils.types import UNDEFINED
from melisa.models.guild import Guild, ChannelType, UnavailableGuild
from melisa.utils.snowflake import Snowflake


class AutoCacheModels(Enum):
    # ToDo: Add FULL_GUILD auto cache model

    """ """

    GUILD_ROLES = "GUILD_ROLES"
    GUILD_THREADS = "GUILD_THREADS"
    GUILD_EMOJIS = "GUILD_EMOJIS"
    GUILD_WEBHOOKS = "GUILD_WEBHOOKS"
    GUILD_MEMBERS = "GUILD_MEMBERS"
    TEXT_CHANNELS = "TEXT_CHANNELS"


class CacheManager:
    """ """

    def __init__(
        self,
        *,
        auto_models: Optional[List[AutoCacheModels]] = None,
        auto_unused_attributes: Optional[Dict[Any, List[str]]] = None
    ):
        self._auto_models: List[AutoCacheModels] = (
            [] if auto_models is None else auto_models
        )
        self.auto_unused_attributes: Dict[Any, List[str]] = (
            {} if auto_unused_attributes is not None else auto_unused_attributes
        )

        self._raw_guilds: Dict[Snowflake, Any] = {}
        self._raw_users: Dict[Snowflake, Any] = {}
        self._raw_dm_channels: Dict[Snowflake, Any] = {}

        # We use symlinks to cache guild channels
        # like we save channel in Guild and save it here
        # and if you need channel, and you don't know its guild
        # you can use special method, and it will find it in guild
        self._channel_symlinks: Dict[Snowflake, Snowflake] = {}

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

        if guild is None:
            return None

        guild = self.__remove_unused_attributes(guild, Guild)

        if hasattr(guild, "channels"):
            channels = guild.channels.values()

            if not AutoCacheModels.TEXT_CHANNELS in self._auto_models:
                channels = filter(
                    lambda channel: channel.type != ChannelType.GUILD_TEXT, channels
                )

            for sym in channels:
                if self._channel_symlinks.get(sym.id, UNDEFINED) is not UNDEFINED:
                    self._channel_symlinks.pop(sym.id)

                self._channel_symlinks[sym.id] = guild.id

        self._raw_guilds.update({guild.id: guild})

        return guild

    def get_guild(self, guild_id: Union[Snowflake, str, int]):
        """
        Get guild from cache

        Parameters
        ----------
        guild_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            ID of guild to get from cache.
        """

        if not isinstance(guild_id, Snowflake):
            guild_id = Snowflake(int(guild_id))
        return self._raw_guilds.get(guild_id, None)

    def _set_none_guilds(self, guilds: List[Dict[str, Any]]) -> None:
        """
        Insert None-Guilds to cache

        Parameters
        ----------
        guilds: Optional[:class:`~melisa.utils.snowflake.Snowflake`, `str`, `int`]
            Data of guilds tso insert to the cache
        """

        guilds_dict = dict(map(lambda i: (i["id"], UnavailableGuild.from_dict(i)), guilds))

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

        if not isinstance(guild_id, Snowflake):
            guild_id = Snowflake(int(guild_id))

        return self._raw_guilds.pop(guild_id, None)
