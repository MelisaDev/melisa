# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import List, Any, Optional, overload

from .channel import Channel, ChannelType, channel_types_for_converting, ThreadsList
from ...utils import Snowflake, Timestamp
from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED


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
    icon_hash: APINullable[:class:`str`]
        Icon hash, returned when in the template object
    splash: Optional[:class:`str`]
        Splash hash
    discovery_splash: APINullable[:class:`str`]
        Discovery splash hash; only present for guilds with the "DISCOVERABLE" feature
    owner: :class:`bool`
        True if the user is the owner of the guild
    owner_id: APINullable[:class:`~melisa.utils.types.Snowflake`]
        Id of owner
    permissions: APINullable[:class:`str`]
        Total permissions for the user in the guild (excludes overwrites)
    region: APINullable[:class:`str`]
        Voice region id for the guild (deprecated)
    afk_channel_id: APINullable[:class:`~melisa.utils.types.Snowflake`]
        Id of afk channel
    afk_timeout: :class:`int`
        Afk timeout in seconds
    widget_enabled: :class:`bool`
        True if the server widget is enabled
    widget_channel_id: :class:`~melisa.utils.types.Snowflake`
        The channel id that the widget will generate an invite to, or `null` if set to no invite
    verification_level: :class:`int`
        Verification level required for the guild
    default_message_notifications: APINullable[:class:`int`]
        Default message notifications level
    explicit_content_filter: :class:`int`
        Explicit content filter level
    features: APINullable[List[:class:`str`]]
        Enabled guild features
    roles: APINullable[:class:`typing.Any`]
        Roles in the guild
    emojis: APINullable[:class:`typing.Any`]
        Custom guild emojis
    mfa_level: :class:`int`
        Required MFA level for the guild
    application_id: APINullable[:class:`~melisa.utils.types.Snowflake`]
        Application id of the guild creator if it is bot-created
    system_channel_id: APINullable[:class:`~melisa.utils.types.Snowflake`]
        The id of the channel where guild notices
        such as welcome messages and boost events are posted
    system_channel_flags: :class:`int`
        System channel flags
    rules_channel_id: APINullable[:class:`~melisa.utils.types.Snowflake`]
        The id of the channel where Community guilds can display rules and/or guidelines
    joined_at: APINullable[:class:`~melisa.utils.Timestamp`]
        When this guild was joined at
    large: APINullable[:class:`bool`]
        True if this is considered a large guild
    unavailable: :class:`bool`
        True if this guild is unavailable due to an outage
    member_count: APINullable[:class:`int`]
        Total number of members in this guild
    voice_states:
        States of members currently in voice channels; lacks the `guild_id` key
    members: APINullable[:class:`typing.Any`]
        Users in the guild
    channels: APINullable[:class:`typing.Any`]
        Channels in the guild
    threads: APINullable[:class:`typing.Any`]
        All active threads in the guild that current user has permission to view
    presences: APINullable[:class:`typing.Any`]
        Presences of the members in the guild, will only include non-offline members
        if the size is greater than `large threshold`
    max_presences: APINullable[:class:`int`]
        The maximum number of presences for the guild
        (`null` is always returned, apart from the largest of guilds)
    max_members: APINullable[:class:`int`]
        The maximum number of members for the guild
    vanity_url_code: APINullable[:class:`str`]
        The vanity url code for the guild
    description: APINullable[:class:`str`]
        The description of a Community guild
    banner: Optional[:class:`str`]
        Banner hash
    premium_tier: APINullable[:class:`str`]
        Premium tier (Server Boost level)
    premium_subscription_count: APINullable[:class:`int`]
        The number of boosts this guild currently has
    preferred_locale: APINullable[:class:`str`]
        The preferred locale of a Community guild;
        used in server discovery and notices from Discord,
        and sent in interactions; defaults to "en-US"
    public_updates_channel_id: APINullable[:class:`~melisa.utils.types.Snowflake`]
        The id of the channel where admins and moderators of
        Community guilds receive notices from Discord
    max_video_channel_users: APINullable[:class:`int`]
        The maximum amount of users in a video channel
    approximate_member_count: APINullable[:class:`int`]
        Approximate number of members in this guild,
        returned from the `GET /guilds/<id>` endpoint when `with_counts` is `true`
    approximate_presence_count: APINullable[:class:`int`]
        Approximate number of non-offline members in this guild,
        returned from the `GET /guilds/<id>`
        endpoint when `with_counts` is `true`
    nsfw_level: APINullable[:class:`int`]
        Guild NSFW level
    premium_progress_bar_enabled: APINullable[:class:`bool`]
        Whether the guild has the boost progress bar enabled
    stage_instances: APINullable[:class:`typing.Any`]
        Stage instances in the guild
    stickers: APINullable[:class:`typing.Any`]
        Custom guild stickers
    welcome_screen: APINullable[:class:`typing.Any`]
        The welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    guild_scheduled_events: APINullable[:class:`typing.Any`]
        The scheduled events in the guild
    """

    id: APINullable[Snowflake] = UNDEFINED
    name: APINullable[str] = UNDEFINED
    icon: APINullable[str] = UNDEFINED
    icon_hash: APINullable[str] = UNDEFINED
    splash: APINullable[str] = UNDEFINED
    discovery_splash: APINullable[str] = UNDEFINED
    owner: APINullable[bool] = UNDEFINED
    owner_id: APINullable[Snowflake] = UNDEFINED
    permissions: APINullable[str] = UNDEFINED
    region: APINullable[str] = UNDEFINED
    afk_channel_id: APINullable[Snowflake] = UNDEFINED
    afk_timeout: APINullable[int] = UNDEFINED
    widget_enabled: APINullable[bool] = UNDEFINED
    widget_channel_id: APINullable[Snowflake] = UNDEFINED
    verification_level: APINullable[int] = UNDEFINED
    default_message_notifications: APINullable[int] = UNDEFINED
    explicit_content_filter: APINullable[int] = UNDEFINED
    features: APINullable[List[str]] = UNDEFINED
    roles: APINullable[List] = UNDEFINED
    emojis: APINullable[List] = UNDEFINED
    # TODO: Make a structures of emoji and role

    mfa_level: APINullable[int] = UNDEFINED
    application_id: APINullable[Snowflake] = UNDEFINED
    system_channel_id: APINullable[Snowflake] = UNDEFINED
    system_channel_flags: APINullable[int] = UNDEFINED
    rules_channel_id: APINullable[Snowflake] = UNDEFINED
    joined_at: APINullable[Timestamp] = UNDEFINED

    large: APINullable[bool] = UNDEFINED
    unavailable: APINullable[bool] = UNDEFINED
    member_count: APINullable[int] = UNDEFINED
    voice_states: APINullable[List] = UNDEFINED
    members: APINullable[List] = UNDEFINED
    threads: APINullable[List] = UNDEFINED
    presences: APINullable[List] = UNDEFINED
    # TODO: Make a structure for voice_states, members, channels, threads, presences(?)

    max_presences: APINullable[int] = UNDEFINED
    max_members: APINullable[int] = UNDEFINED
    vanity_url_code: APINullable[str] = UNDEFINED
    description: APINullable[str] = UNDEFINED
    banner: APINullable[str] = UNDEFINED
    premium_tier: APINullable[str] = UNDEFINED
    premium_subscription_count: APINullable[int] = UNDEFINED
    preferred_locale: APINullable[str] = UNDEFINED
    public_updates_channel_id: APINullable[Snowflake] = UNDEFINED
    max_video_channel_users: APINullable[int] = UNDEFINED
    approximate_member_count: APINullable[int] = UNDEFINED
    approximate_presence_count: APINullable[int] = UNDEFINED
    nsfw_level: APINullable[int] = UNDEFINED
    premium_progress_bar_enabled: APINullable[bool] = UNDEFINED
    stage_instances: APINullable[List] = UNDEFINED
    stickers: APINullable[List] = UNDEFINED
    welcome_screen: APINullable = UNDEFINED
    guild_scheduled_events: APINullable[List] = UNDEFINED

    # TODO: Make a structure for welcome_screen, stage_instances,
    #  stickers and guild_scheduled_events

    @property
    def channels(self):
        return []

    @overload
    async def create_channel(
        self,
        *,
        name: str,
        type: Optional[ChannelType] = None,
        topic: Optional[str] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        position: Optional[int] = None,
        permission_overwrites: Optional[List[Any]] = None,
        parent_id: Optional[Snowflake] = None,
        nsfw: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> Channel:
        ...

    async def create_channel(self, *, reason: Optional[str] = None, **kwargs):
        """|coro|

        Create a new channel object for the guild.

        Parameters
        ----------
        name: str
            channel name (1-100 characters)
        type: Optional[:class:`int`]
            the type of channel
        topic: Optional[:class:`str`]
            channel topic (0-1024 characters)
        bitrate: Optional[:class:`int`]
            the bitrate (in bits) of the voice channel (voice only)
        user_limit: Optional[:class:`int`]
            the user limit of the voice channel (voice only)
        rate_limit_per_user: Optional[:class:`int`]
            amount of seconds a user has to wait
            before sending another message (0-21600)
            bots, as well as users with the permission
            ``MANAGE_MESSAGES`` or ``MANAGE_CHANNEL``, are unaffected
        position: Optional[:class:`int`]
            sorting position of the channel
        permission_overwrites: Optional[List[Any]]
            the channel's permission overwrites
        parent_id: Optional[:class:`~melisa.Snowflake`]
            id of the parent category for a channel
        nsfw: Optional[:class:`bool`]
            whether the channel is nsfw
        reason: Optional[:class:`str`]
            audit log reason |default| :data:`None`

        Raises
        -------
        BadRequestError
            If some specified parameters are wrong.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            This method requires `MANAGE_CHANNELS` permission.
            Setting `MANAGE_ROLES` permission in channels is only possible for guild administrators.

        Returns
        -------
        :class:`~melisa.models.guild.channel.Channel`
            New channel object.
        """
        data = await self._http.post(
            f"guilds/{self.id}/channels",
            data=kwargs,
            headers={"X-Audit-Log-Reason": reason},
        )

        data.update({"type": ChannelType(data.pop("type"))})

        channel_cls = channel_types_for_converting.get(data["type"], Channel)
        return channel_cls.from_dict(data)

    async def active_threads(self) -> ThreadsList:
        """|coro|

        Returns a Threadslist of active ``Thread`` that the client can access.

        This includes both private and public threads.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.

        Returns
        -------
        :class:`~melisa.models.channel.ThreadsList`
            The active threads.
        """

        return ThreadsList.from_dict(
            await self._http.get(f"/guilds/{self.id}/threads/active")
        )


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
