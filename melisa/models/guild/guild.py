# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import List, Any

from ...utils import Snowflake
from ...utils import APIModelBase
from ...utils.types import APINullable


class DefaultMessageNotificationLevel(IntEnum):
    """Message notification level

    Attributes
    ----------
    ALL_MESSAGES:
        Members will receive notifications for all messages by default
    ONLY_MENTIONS:
        Members will receive notifications only for messages that @mention them by default
    """

    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1

    def __int__(self):
        return self.value


class ExplicitContentFilterLevel(IntEnum):
    """Explicit Content Filter Level

    Attributes
    ----------
    DISABLED:
        Media content will not be scanned
    MEMBERS_WITHOUT_ROLES:
        Media content sent by members without roles will be scanned
    ALL_MEMBERS:
        Media content sent by all members will be scanned
    """

    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2

    def __int__(self):
        return self.value


class MFALevel(IntEnum):
    """MFA Level

    Attributes
    ----------
    NONE:
        Guild has no MFA/2FA requirement for moderation actions
    ELEVATED:
        Guild has a 2FA requirement for moderation actions
    """

    NONE = 0
    ELEVATED = 1

    def __int__(self):
        return self.value


class VerificationLevel(IntEnum):
    """Verification level on the server

    Attributes
    ----------
    NONE:
        Unrestricted
    LOW:
        Must have verified email on account
    MEDIUM:
        Must be registered on Discord for longer than 5 minutes
    HIGH:
        Must be a member of the server for longer than 10 minutes
    VERY_HIGH:
        Must have a verified phone number
    """

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

    def __int__(self):
        return self.value


class GuildNSFWLevel(IntEnum):
    """NSFW level on the server

    Attributes
    ----------
    DEFAULT:
        Default value on server
    EXPLICIT:
        Explicit value on server
    SAFE:
        Safe value on server
    AGE_RESTRICTED:
        Age restricted on server
    """

    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

    def __int__(self):
        return self.value


class PremiumTier(IntEnum):
    """Boost the server with boosters and nitro

    Attributes
    ----------
    NONE:
        Guild has not unlocked any Server Boost perks
    TIER_1:
        Guild has unlocked Server Boost level 1 perks
    TIER_2:
        Guild has unlocked Server Boost level 2 perks
    TIER_3:
        Guild has unlocked Server Boost level 3 perks
    """

    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3

    def __int__(self):
        return self.value


class SystemChannelFlags(IntEnum):
    """System channel flags

    Attributes
    ----------
    SUPPRESS_JOIN_NOTIFICATIONS:
        Suppress member join notifications
    SUPPRESS_PREMIUM_SUBSCRIPTIONS:
        Suppress server boost notifications
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS:
        Suppress server setup tips
    SUPPRESS_JOIN_NOTIFICATION_REPLIES:
        Hide member join sticker reply buttons
    """

    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3

    def __int__(self):
        return self.value


class GuildFeatures(Enum):
    """Guild Features

    Attributes
    ----------
    ANIMATED_ICON:
        Guild has access to set an animated guild icon
    BANNER:
        Guild has access to set a guild banner image
    COMMERCE:
        Guild has access to use commerce features (i.e. create store channels)
    COMMUNITY:
        Guild can enable welcome screen, Membership Screening,
        stage channels and discovery, and receives community updates
    DISCOVERABLE:
        Guild is able to be discovered in the directory
    FEATURABLE:
        Guild is able to be featured in the directory
    INVITE_SPLASH:
        Guild has access to set an invite splash background
    MEMBER_VERIFICATION_GATE_ENABLED:
        Guild has enabled Membership Screening
    MONETIZATION_ENABLED:
        Guild has enabled monetization
    MORE_STICKERS:
        Guild has increased custom sticker slots
    NEWS:
        Guild has access to create news channels
    PARTNERED:
        Guild is partnered
    PREVIEW_ENABLED:
        Guild can be previewed before joining via Membership Screening or the directory
    PRIVATE_THREADS:
        Guild has access to create private threads
    ROLE_ICONS:
        Guild is able to set role icons
    SEVEN_DAY_THREAD_ARCHIVE:
        Guild has access to the seven day archive time for threads
    THREE_DAY_THREAD_ARCHIVE:
        Guild has access to the three day archive time for threads
    TICKETED_EVENTS_ENABLED:
        Guild has enabled ticketed events
    VANITY_URL:
        Guild has access to set a vanity URL
    VERIFIED:
        Guild is verified
    VIP_REGIONS:
        Guild has access to set 384kbps bitrate in voice (previously VIP voice servers)
    WELCOME_SCREEN_ENABLED:
        Guild has enabled the welcome screen
    """

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
    """Guilds in Discord represent an isolated collection of users and channels,
     and are often referred to as "servers" in the UI.

    Attributes
    ----------
    id: :class:`~melisa.utils.types.Snowflake`
        Guild id
    name: :class:`str`
        Guild name (2-100 characters, excluding trailing and leading whitespace)
    icon: :class:`str`
        Icon hash
    icon_hash: Optional[:class:`str`]
        Icon hash, returned when in the template object
    splash: Optional[:class:`str`]
        Splash hash
    discovery_splash: Optional[:class:`str`]
        Discovery splash hash; only present for guilds with the "DISCOVERABLE" feature
    owner: :class:`bool`
        True if the user is the owner of the guild
    owner_id: Optional[:class:`~melisa.utils.types.Snowflake`]
        Id of owner
    permissions: Optional[:class:`str`]
        Total permissions for the user in the guild (excludes overwrites)
    region: Optional[:class:`str`]
        Voice region id for the guild (deprecated)
    afk_channel_id: Optional[:class:`~melisa.utils.types.Snowflake`]
        Id of afk channel
    afk_timeout: :class:`int`
        Afk timeout in seconds
    widget_enabled: :class:`bool`
        True if the server widget is enabled
    widget_channel_id: :class:`~melisa.utils.types.Snowflake`
        The channel id that the widget will generate an invite to, or `null` if set to no invite
    verification_level: :class:`int`
        Verification level required for the guild
    default_message_notifications: Optional[:class:`int`]
        Default message notifications level
    explicit_content_filter: :class:`int`
        Explicit content filter level
    features: Optional[:class:`typing.Any`]
        Enabled guild features
    roles: Optional[:class:`typing.Any`]
        Roles in the guild
    emojis: Optional[:class:`typing.Any`]
        Custom guild emojis
    mfa_level: :class:`int`
        Required MFA level for the guild
    application_id: Optional[:class:`~melisa.utils.types.Snowflake`]
        Application id of the guild creator if it is bot-created
    system_channel_id: Optional[:class:`~melisa.utils.types.Snowflake`]
        The id of the channel where guild notices
        such as welcome messages and boost events are posted
    system_channel_flags: :class:`int`
        System channel flags
    rules_channel_id: Optional[:class:`~melisa.utils.types.Snowflake`]
        The id of the channel where Community guilds can display rules and/or guidelines
    joined_at: Optional[:class:`int`]
        When this guild was joined at
    large: Optional[:class:`bool`]
        True if this is considered a large guild
    unavailable: :class:`bool`
        True if this guild is unavailable due to an outage
    member_count: Optional[:class:`int`]
        Total number of members in this guild
    voice_states:
        States of members currently in voice channels; lacks the `guild_id` key
    members: Optional[:class:`typing.Any`]
        Users in the guild
    channels: Optional[:class:`typing.Any`]
        Channels in the guild
    threads: Optional[:class:`typing.Any`]
        All active threads in the guild that current user has permission to view
    presences: Optional[:class:`typing.Any`]
        Presences of the members in the guild, will only include non-offline members
        if the size is greater than `large threshold`
    max_presences: Optional[:class:`int`]
        The maximum number of presences for the guild
        (`null` is always returned, apart from the largest of guilds)
    max_members: Optional[:class:`int`]
        The maximum number of members for the guild
    vanity_url_code: Optional[:class:`str`]
        The vanity url code for the guild
    description: Optional[:class:`str`]
        The description of a Community guild
    banner: Optional[:class:`str`]
        Banner hash
    premium_tier: Optional[:class:`str`]
        Premium tier (Server Boost level)
    premium_subscription_count: Optional[:class:`int`]
        The number of boosts this guild currently has
    preferred_locale: Optional[:class:`str`]
        The preferred locale of a Community guild;
        used in server discovery and notices from Discord,
        and sent in interactions; defaults to "en-US"
    public_updates_channel_id: Optional[:class:`~melisa.utils.types.Snowflake`]
        The id of the channel where admins and moderators of
        Community guilds receive notices from Discord
    max_video_channel_users: Optional[:class:`int`]
        The maximum amount of users in a video channel
    approximate_member_count: Optional[:class:`int`]
        Approximate number of members in this guild,
        returned from the `GET /guilds/<id>` endpoint when `with_counts` is `true`
    approximate_presence_count: Optional[:class:`int`]
        Approximate number of non-offline members in this guild,
        returned from the `GET /guilds/<id>`
        endpoint when `with_counts` is `true`
    nsfw_level: Optional[:class:`int`]
        Guild NSFW level
    premium_progress_bar_enabled: Optional[:class:`bool`]
        Whether the guild has the boost progress bar enabled
    stage_instances: Optional[:class:`typing.Any`]
        Stage instances in the guild
    stickers: Optional[:class:`typing.Any`]
        Custom guild stickers
    welcome_screen: Optional[:class:`typing.Any`]
        The welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    guild_scheduled_events: Optional[:class:`typing.Any`]
        The scheduled events in the guild
    """

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
    roles: APINullable[List[Any]] = None
    emojis: APINullable[List[Any]] = None
    # TODO: Make a structures of emoji and role

    mfa_level: APINullable[int] = None
    application_id: APINullable[Snowflake] = None
    system_channel_id: APINullable[Snowflake] = None
    system_channel_flags: APINullable[int] = None
    rules_channel_id: APINullable[Snowflake] = None
    joined_at: APINullable[int] = None
    # TODO: Deal with joined_at

    large: APINullable[bool] = None
    unavailable: APINullable[bool] = None
    member_count: APINullable[int] = None
    voice_states: APINullable[List[Any]] = None
    members: APINullable[List[Any]] = None
    channels: APINullable[List[Any]] = None
    threads: APINullable[List[Any]] = None
    presences: APINullable[List[Any]] = None
    # TODO: Make a structure for voice_states, members, channels, threads, presences(?)

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
    stage_instances: APINullable[List[Any]] = None
    stickers: APINullable[List[Any]] = None
    welcome_screen: APINullable[Any] = None
    guild_scheduled_events: APINullable[List[Any]] = None

    # TODO: Make a structure for welcome_screen, stage_instances,
    #  stickers and guild_scheduled_events


@dataclass(repr=False)
class UnavailableGuild(APIModelBase):
    """A partial guild object.
    Represents an Offline Guild, or a Guild whose information has not been provided
    through Guild Create events during the Gateway connect.

    Attributes
    ----------
    id: :class:`~melisa.utils.types.Snowflake`
        Guild id
    unavailable: :class:`bool`
        True if this guild is unavailable due to an outage
    """

    id: APINullable[Snowflake] = None
    unavailable: APINullable[bool] = True
