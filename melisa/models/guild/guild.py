# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Any, Optional, overload, Dict, TYPE_CHECKING, Union

from .channel import (
    ThreadsList,
    Thread,
    _choose_channel_type,
)


from .member import GuildMember
from ... import Role
from ...utils import Snowflake, Timestamp
from ...utils.api_model import APIModelBase
from ...utils.conversion import try_enum
from ...utils.types import APINullable

if TYPE_CHECKING:
    from .channel import ChannelType, Channel


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
    members: APINullable[:class:`~melisa.models.guild.member.GuildMember`]
        Users in the guild
    channels: APINullable[Dict[:class:`~melisa.models.guild.channel.Channel`]]
        Channels in the guild
    threads: APINullable[Dict[:class:`~melisa.models.guild.channel.Thread`]]
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

    id: Snowflake
    roles: APINullable[Dict]
    emojis: APINullable[Dict]
    members: APINullable[Dict]
    threads: APINullable[Dict]
    presences: APINullable[Dict]
    channels: APINullable[Dict]
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
    features: APINullable[List[str]] = None
    # TODO: Make a structures of emoji and role

    mfa_level: APINullable[MFALevel] = None
    application_id: APINullable[Snowflake] = None
    system_channel_id: APINullable[Snowflake] = None
    system_channel_flags: APINullable[SystemChannelFlags] = None
    rules_channel_id: APINullable[Snowflake] = None
    joined_at: APINullable[Timestamp] = None

    large: APINullable[bool] = None
    unavailable: APINullable[bool] = None
    member_count: APINullable[int] = None
    voice_states: APINullable[List] = None
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
    stage_instances: APINullable[List] = None
    stickers: APINullable[List] = None
    welcome_screen: APINullable = None
    guild_scheduled_events: APINullable[List] = None

    # TODO: Make a structure for welcome_screen, stage_instances,
    #  stickers and guild_scheduled_events

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Guild:
        """Generate a guild from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a guild.
        """
        self: Guild = super().__new__(cls)

        self.id = int(data["id"])
        self.member_count = data.get("member_count", 0)
        self.name = data.get("name", "")
        self.region = data.get("region")
        self.verification_level = try_enum(
            VerificationLevel, data.get("verification_level")
        )
        self.vanity_url_code = data.get("vanity_url_code")
        self.default_notifications = data.get("default_message_notifications")
        self.explicit_content_filter = data.get("explicit_content_filter", 0)
        self.afk_timeout = data.get("afk_timeout", 0)
        self.icon = data.get("icon")
        self.icon_hash = data.get("icon_hash")
        self.banner = data.get("banner")
        self.unavailable = data.get("unavailable", False)
        self.permissions = data.get("permissions")
        self.welcome_screen = data.get("welcome_screen")
        self.guild_scheduled_events = data.get("guild_scheduled_events")

        self.mfa_level = try_enum(MFALevel, data.get("mfa_level", 0))
        self.emojis = data.get("emojis", {})
        self.stickers = data.get("stickers", {})
        self.features = data.get("features", [])
        self.splash = data.get("splash")
        self.description = data.get("description")
        self.max_presences = data.get("max_presences")
        self.max_members = data.get("max_members")
        self.max_video_channel_users = data.get("max_video_channel_users")
        self.premium_tier = try_enum(PremiumTier, data.get("premium_tier", 0))
        self.premium_subscription_count = data.get("premium_subscription_count", 0)
        self.system_channel_flags = try_enum(
            SystemChannelFlags, data.get("system_channel_flags", 0)
        )
        self.preferred_locale = data.get("preferred_locale")
        self.discovery_splash = data.get("discovery_splash")
        self.nsfw_level = data.get("nsfw_level", 0)
        self.premium_progress_bar_enabled = data.get(
            "premium_progress_bar_enabled", False
        )
        self.approximate_presence_count = data.get("approximate_presence_count")
        self.approximate_member_count = data.get("approximate_member_count")
        self.widget_enabled = data.get("widget_enabled")

        if data.get("widget_channel_id") is not None:
            self.widget_channel_id = Snowflake(data["widget_channel_id"])
        else:
            self.widget_channel_id = None

        if data.get("system_channel_id") is not None:
            self.system_channel_id = Snowflake(data["system_channel_id"])
        else:
            self.system_channel_id = None

        if data.get("rules_channel_id") is not None:
            self.rules_channel_id = Snowflake(data["rules_channel_id"])
        else:
            self.rules_channel_id = None

        if data.get("public_updates_channel_id") is not None:
            self.public_updates_channel_id = Snowflake(
                data["public_updates_channel_id"]
            )
        else:
            self.public_updates_channel_id = None

        if data.get("owner_id") is not None:
            self.owner_id = Snowflake(data["owner_id"])
        else:
            self.owner_id = None

        if data.get("afk_channel_id") is not None:
            self.afk_channel_id = Snowflake(data["afk_channel_id"])
        else:
            self.afk_channel_id = None

        if data.get("joined_at") is not None:
            self.joined_at = Timestamp.parse(data["joined_at"])
        else:
            self.joined_at = None

        self.stage_instances = data.get("stage_instances")
        self.scheduled_events = data.get("guild_scheduled_events")
        self.owner = None if data.get("owner") is None else data["owner"]
        self.large = None if self.member_count == 0 else self.member_count >= 250
        self.voice_states = data.get("voice_states")
        self.presences = data.get("presences")

        self.threads = {}
        self.channels = {}
        self.members = {}

        for member in data.get("members", []):
            member = GuildMember.from_dict(member)
            self.members[member.user.id] = member

        for thread in data.get("threads", []):
            self.threads[thread["id"]] = Thread.from_dict(thread)

        for channel in data.get("channels", []):
            channel = _choose_channel_type(channel)
            self.channels[Snowflake(int(channel.id))] = channel

        for role in data.get("roles", []):
            role["guild_id"] = self.id
            self.roles[Snowflake(int(role.id))] = Role.from_dict(role)

        return self

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

        return _choose_channel_type(data)

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

    async def unban(
        self,
        user_id: Union[Snowflake, str, int],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        Remove the ban for a user.

        **Required permissions:** ``BAN_MEMBERS``

        Parameters
        ----------
        user_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of user to operate with.
        reason: Optional[:class:`str`]
            The reason of the action.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong guild, user or something else
            Or if the user is not banned
        """

        await self._client.rest.remove_guild_ban(self.id, user_id, reason=reason)


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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UnavailableGuild:
        """Generate a unavailable guild from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into an unavailable guild.
        """
        self: UnavailableGuild = super().__new__(cls)

        self.id = Snowflake(int(data["id"]))
        self.unavailable = data["unavailable"]

        return self
