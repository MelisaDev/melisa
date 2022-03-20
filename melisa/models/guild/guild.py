# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum, Flag
from typing import Optional, Tuple, List, Literal

from ...utils import Snowflake
from ...utils import APIModelBase
from ...utils.types import APINullable


class DefaultMessageNotificationLevel(IntEnum):
    """"""

    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1

    def __int__(self):
        return self.value


class ExplicitContentFilterLevel(IntEnum):
    """"""

    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS	= 2

    def __int__(self):
        return self.value


class MFALevel(IntEnum):
    """"""

    NONE = 0
    ELEVATED = 1

    def __int__(self):
        return self.value


class VerificationLevel(IntEnum):
    """"""

    NONE = 0	
    LOW	= 1	
    MEDIUM = 2	
    HIGH = 3	
    VERY_HIGH = 4

    def __int__(self):
        return self.value


class GuildNSFWLevel(IntEnum):
    """"""

    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

    def __int__(self):
        return self.value


class PremiumTier(IntEnum):
    """"""

    NONE = 0	
    TIER_1 = 1	
    TIER_2 = 2	
    TIER_3 = 3	

    def __int__(self):
        return self.value


class SystemChannelFlags(IntEnum):
    """"""

    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1	
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2	
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3	

    def __int__(self):
        return self.value


class GuildFeatures(Enum):
    """"""

    ANIMATED_ICON = "ANIMATED_ICON"
    BANNER = "BANNER"
    COMMERCE = "COMMERCE"
    COMMUNITY = "COMMUNITY"
    DISCOVERABLE = "DISCOVERABLE"
    FEATURABLE = "FEATURABLE"
    INVITE_SPLASH = "INVITE_SPLASH"
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"
    MORE_STICKERS = "MORE_STICKERS"
    NEWS = "NEWS"
    PARTNERED = "PARTNERED"
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    PRIVATE_THREADS = "PRIVATE_THREADS"
    ROLE_ICONS = "ROLE_ICONS"
    SEVEN_DAY_THREAD_ARCHIVE = "SEVEN_DAY_THREAD_ARCHIVE"
    THREE_DAY_THREAD_ARCHIVE = "THREE_DAY_THREAD_ARCHIVE"
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    VANITY_URL = "VANITY_URL"
    VERIFIED = "VERIFIED"
    VIP_REGIONS = "VIP_REGIONS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"


@dataclass(repr=False)
class Guild(APIModelBase):
    """"""

    id: APINullable[Snowflake] = None
    name: APINullable[str] = None
    icon: APINullable[str] = None
    icon_hash: APINullable[str] = None
    splash: APINullable[str] = None
    discovery_splash: APINullable[str] = None
    owner: APINullable[bool] = None
    owner_id: APINullable[Snowflake] = None
    permissions: APINullable[str] = None
    region: APINullable[str] = None
    afk_channel_id: APINullable[Snowflake] = None
    afk_timeout: APINullable[int] = None
    widget_enabled: APINullable[bool] = None
    widget_channel_id: APINullable[Snowflake] = None
    verification_level: APINullable[int] = None
    default_message_notifications: APINullable[int] = None
    explicit_content_filter: APINullable[int] = None
    features: APINullable[List[GuildFeatures]] = None
    #TODO: Make a structure for emoji and role 

    mfa_level: APINullable[int] = None
    application_id: APINullable[Snowflake] = None
    system_channel_id: APINullable[Snowflake] = None
    system_channel_flags: APINullable[int] = None
    rules_channel_id: APINullable[Snowflake] = None
    #TODO: Deal with joined_at

    large: APINullable[bool] = None
    unavailable: APINullable[bool] = None
    member_count: APINullable[int] = None
    #TODO: Make a structure for voice_states, members, channels, threads, presences(?)

    max_presences: APINullable[int] = None
    max_members: APINullable[int] = None
    vanity_url_code: APINullable[str] = None
    description: APINullable[str] = None
    banner: APINullable[str] = None
    premium_tier: APINullable[str] = None
    premium_subscription_count: APINullable[int] = None
    preferred_locale: APINullable[str] = None
    public_updates_channel_id: APINullable[Snowflake] = None
    max_video_channel_users: APINullable[int] = None
    approximate_member_count: APINullable[int] = None
    approximate_presence_count: APINullable[int] = None
    nsfw_level: APINullable[int] = None
    premium_progress_bar_enabled: APINullable[bool] = None
    #TODO: Make a structure for welcome_screen, stage_instances, stickers and guild_scheduled_events


    async def get_guild(self, _id: id, with_counts: bool = False ):
        """"""

        return await self._http.get(
            f"/guild/{_id}", params = {"with_counts": "true" if with_counts else None})
    
    

    @property
    def default_message_notifications(self) -> Optional[DefaultMessageNotificationLevel]:
        """"""

        return(
            None
            if self.default_message_notifications is None
            else DefaultMessageNotificationLevel(self.default_message_notifications)
        )
    
    @property
    def explicit_content_filter(self) -> Optional[ExplicitContentFilterLevel]:
        """"""

        return(
            None
            if self.explicit_content_filter is None
            else ExplicitContentFilterLevel(self.explicit_content_filter)
        )
    
    @property
    def mfa_level(self) -> Optional[MFALevel]:
        """"""

        return(
            None
            if self.mfa_level is None
            else MFALevel(self.mfa_level)
        )

    @property
    def verification_level(self) -> Optional[VerificationLevel]:
        """"""

        return(
            None
            if self.verification_level is None
            else VerificationLevel(self.verification_level)
        )

    @property
    def nsfw_level(self) -> Optional[GuildNSFWLevel]:
        """"""

        return(
            None
            if self.nsfw_level is None
            else GuildNSFWLevel(self.nsfw_level)
        )

    @property 
    def premium_tier(self) -> Optional(PremiumTier):
        """"""

        return(
            None
            if self.premium_tier is None
            else PremiumTier(self.premium_tier)
        )
    
    @property
    def system_channel_flags(self) -> Optional[SystemChannelFlags]:
        """"""

        return(
            None
            if self.system_channel_flags is None
            else SystemChannelFlags(self.system_channel_flags)
        )


@dataclass(repr=False)
class UnavailableGuild(APIModelBase):

    id: APINullable[Snowflake] = None
    unavailable: APINullable[bool] = True 
