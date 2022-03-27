# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import List, Any

from ...utils import Snowflake
from ...utils import APIModelBase
from ...utils.types import APINullable


class ChannelType(IntEnum):
    """Channel Type
    NOTE: Type 10, 11 and 12 are only available in Discord API v9.

    Attributes
    ----------
    GUILD_TEXT:
        A text channel within a server
    DM:
        A direct message between users
    GUILD_VOICE:
        A voice channel within a server
    GROUP_DM:
        A direct message between multiple users
    GUILD_CATEGORY:
        An organizational category that contains up to 50 channels
    GUILD_NEWS:
        A channel that users can follow and crosspost into their own server
    GUILD_STORE:
        A channel in which game developers can sell their game on Discord
    GUILD_NEWS_THREAD:
        A temporary sub-channel within a `GUILD_NEWS` channel
    GUILD_PUBLIC_THREAD:
        A temporary sub-channel within a GUILD_TEXT channel
    GUILD_PRIVATE_THREAD:
        A temporary sub-channel within a GUILD_TEXT channel that is only viewable by those invited
        and those with the MANAGE_THREADS permission
    GUILD_STAGE_VOICE:
        A voice channel for hosting events with an audience
    """

    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13

    def __int__(self):
        return self.value


class VideoQualityModes(IntEnum):
    """Video Quality Modes

    Attributes
    ----------
    AUTO:
        Discord chooses the quality for optimal performance
    FULL:
        720p
    """

    AUTO = 1
    FULL = 2

    def __int__(self):
        return self.value


@dataclass(repr=False)
class Channel(APIModelBase):
    """Represents a guild or DM channel within Discord"""

    # TODO: Add a description for Channel

    id: APINullable[Snowflake] = None
    type: APINullable[int] = None
    guild_id: APINullable[Snowflake] = None
    position: APINullable[int] = None
    permission_overwrites: APINullable[List[Any]] = None
    name: APINullable[str] = None
    topic: APINullable[str] = None
    nsfw: APINullable[bool] = None
    last_message_id: APINullable[Snowflake] = None
    bitrate: APINullable[int] = None
    user_limit: APINullable[int] = None
    rate_limit_per_user: APINullable[int] = None
    recipients: APINullable[List[Any]] = None
    icon: APINullable[str] = None
    owner_id: APINullable[Snowflake] = None
    application_id: APINullable[Snowflake] = None
    parent_id: APINullable[Snowflake] = None
    last_pin_timestamp: APINullable[int] = None
    rtc_region: APINullable[str] = None
    video_quality_mode: APINullable[int] = None
    message_count: APINullable[int] = None
    member_count: APINullable[int] = None
    thread_metadata: APINullable[List[Any]] = None
    member: APINullable[List[Any]] = None
    default_auto_archive_duration: APINullable[int] = None
    permissions: APINullable[str] = None
