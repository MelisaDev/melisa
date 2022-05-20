# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import IntEnum
from typing import List, TYPE_CHECKING, Optional, Dict, Any, Union

from .embed import Embed
from ...utils import Snowflake, Timestamp, try_enum, APIModelBase
from ...utils.types import APINullable, UNDEFINED

if TYPE_CHECKING:
    from ..guild.channel import Thread, _choose_channel_type


class MessageType(IntEnum):
    """Message Type
    NOTE: Type `19` and `20` are only in API v8.
    In v6, they are still type `0`. Type `21` is only in API v9.
    """

    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23

    def __int__(self):
        return self.value


class MessageActivityType(IntEnum):
    """Message Activity Type"""

    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5

    def __int__(self):
        return self.value


class MessageFlags(IntEnum):
    """Message Flags

    Attributes
    ----------
    CROSSPOSTED:
        This message has been published to subscribed channels (via Channel Following)
    IS_CROSSPOST:
        This message originated from a message in another channel (via Channel Following)
    SUPPRESS_EMBEDS:
        Do not include any embeds when serializing this message
    SOURCE_MESSAGE_DELETED:
        The source message for this crosspost has been deleted (via Channel Following)
    URGENT:
        This message came from the urgent message system
    HAS_THREAD:
        This message has an associated thread, with the same id as the message
    EPHEMERAL:
        This message is only visible to the user who invoked the Interaction
    LOADING:
        This message is an Interaction Response and the bot is "thinking"
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD:
        This message failed to mention some roles and add their members to the thread
    """

    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8

    def __int__(self):
        return self.value


@dataclass(repr=False)
class AllowedMentions:
    """A class that represents what mentions are allowed in a message.

    Attributes
    ----------
    everyone: :class:`bool`
        Whether to allow everyone and here mentions. Defaults to ``True``.
    users: Union[:class:`bool`, List[:class:`~melisa.utils.snowflake.Snowflake`]]
        Controls the users being mentioned. If ``True`` (the default) then
        users are mentioned based on the message content. If ``False`` then
        users are not mentioned at all. Or you can specify list of ids.
    roles: Union[:class:`bool`, List[:class:`~melisa.utils.snowflake.Snowflake`]]
        Controls the roles being mentioned. If ``True`` then
        roles are mentioned based on the message content. If ``False`` then
        roles are not mentioned at all.
    replied_user: :class:`bool`
        Whether to mention the author of the message being replied to.
    """

    __slots__ = ("everyone", "users", "roles", "replied_user")

    def __init__(
        self,
        *,
        everyone: bool = True,
        users: Union[bool, List[Union[Snowflake, int, str]]] = True,
        roles: Union[bool, List[Union[Snowflake, int, str]]] = True,
        replied_user: bool = True,
    ):
        self.everyone = everyone
        self.users = users
        self.roles = roles
        self.replied_user = replied_user

    @classmethod
    def enabled(cls):
        """A factory method that returns a :class:`AllowedMentions`
        with all fields explicitly set to ``True``"""
        return cls(everyone=True, users=True, roles=True, replied_user=True)

    @classmethod
    def disabled(cls):
        """A factory method that returns a :class:`AllowedMentions`
        with all fields set to ``False``"""
        return cls(everyone=False, users=False, roles=False, replied_user=False)

    def to_dict(self):
        to_parse = []
        data = {}

        if self.everyone:
            to_parse.append("everyone")

        # `None` cannot be specified by the default
        if self.users is True:
            to_parse.append("users")
        elif self.users is not False:
            data["users"] = [str(user) for user in self.users]

        if self.roles is True:
            to_parse.append("roles")
        elif self.roles is not False:
            data["roles"] = [str(role) for role in self.roles]

        if self.replied_user:
            data["replied_user"] = True

        data["parse"] = to_parse

        return data


@dataclass(repr=False)
class Message(APIModelBase):
    """Represents a message sent in a channel within Discord.

    Attributes
    ----------
    id: :class:`~melisa.utils.types.snowflake.Snowflake`
        Id of the message
    channel_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        Id of the channel the message was sent in
    channel: :class:`~melisa.models.guild.Channel`
        Object of channel where message was sent in
    guild: :class:`~melisa.models.guild.Guild`
        Object of guild where message was sent in
    guild_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        Id of the guild the message was sent in
    author: :class:`typing.Any`
        The author of this message (not guaranteed to be a valid user, see below)
    member: :class:`typing.Any`
        Member properties for this message's author
    content: :class:`str`
        Contents of the message
    timestamp: :class:`~melisa.utils.timestamp.Timestamp`
        When this message was sent
    edited_timestamp: :class:`~melisa.utils.timestamp.Timestamp`
        When this message was edited (or null if never)
    tts: :class:`bool`
        Whether this was a TTS message
    mention_everyone: :class:`bool`
        Whether this message mentions everyone
    mentions: :class:`typing.Any`
        Users specifically mentioned in the message
    mention_roles: :class:`typing.Any`
        Roles specifically mentioned in this message
    mention_channels: :class:`typing.Any`
        Channels specifically mentioned in this message
    attachments: :class:`typing.Any`
        Any attached files
    embeds: :class:`typing.Any`
        Any embedded content
    reactions: :class:`typing.Any`
        Reactions to the message
    nonce: :class:`int` or `str`
        Used for validating a message was sent
    pinned: :class:`bool`
        Whether this message is pinned
    webhook_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        If the message is generated by a webhook, this is the webhook's id
    type: :class:`MessageType`
        Type of message
    activity: :class:`typing.Any`
        Sent with Rich Presence-related chat embeds
    application: :class:`typing.Any`
        Sent with Rich Presence-related chat embeds
    application_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        If the message is an Interaction or application-owned webhook,
        this is the id of the application
    message_reference: :class:`typing.Any`
        Data showing the source of a crosspost, channel follow add, pin, or reply message
    flags: :class:`int`
        Message flags combined as a bitfield
    interaction: :class:`typing.Any`
        Sent if the message is a response to an Interaction
    thread: :class:`typing.Any`
        The thread that was started from this message, includes thread member object
    components: :class:`typing.Any`
        Sent if the message contains components like buttons,
        action rows, or other interactive components
    sticker_items: :class:`typing.Any`
        Sent if the message contains stickers
    stickers: :class:`typing.Any`
        Deprecated the stickers sent with the message
    """

    id: APINullable[Snowflake] = None
    channel_id: APINullable[Snowflake] = None
    guild_id: APINullable[Snowflake] = None
    author: APINullable[Dict] = None
    member: APINullable[Dict] = None
    content: APINullable[str] = None
    timestamp: APINullable[Timestamp] = None
    edited_timestamp: APINullable[Timestamp] = None
    tts: APINullable[bool] = None
    mention_everyone: APINullable[bool] = None
    mentions: APINullable[List] = None
    mention_roles: APINullable[List] = None
    mention_channels: APINullable[List] = None
    attachments: APINullable[List] = None
    embeds: APINullable[List] = None
    reactions: APINullable[List] = None
    nonce: APINullable[int] or APINullable[str] = None
    pinned: APINullable[bool] = None
    webhook_id: APINullable[Snowflake] = None
    type: APINullable[MessageType] = None
    activity: APINullable[Dict] = None  # ToDo Set model here
    application: APINullable[Dict] = None
    application_id: APINullable[Snowflake] = None
    message_reference: APINullable[Dict] = None
    flags: APINullable[int] = None
    referenced_message: APINullable[Message] = None
    interaction: APINullable[Dict] = None
    thread: APINullable[Thread] = None
    components: APINullable[List] = None
    sticker_items: APINullable[List] = None
    stickers: APINullable[List] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a message from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into an unknown channel.
        """
        self: Message = super().__new__(cls)

        self.id = data["id"]
        self.channel_id = Snowflake(data["channel_id"])
        self.guild_id = (
            Snowflake(data["guild_id"]) if data.get("guild_id") is not None else None
        )
        self.author = data.get("author")  # ToDo: User object
        self.member = data.get("member")
        self.content = data.get("content", "")
        self.timestamp = Timestamp.parse(data["timestamp"])
        self.edited_timestamp = (
            Timestamp.parse(data["edited_timestamp"])
            if data.get("edited_timestamp") is not None
            else None
        )
        self.tts = data["tts"]
        self.mention_everyone = data["mention_everyone"]
        self.mentions = data["mentions"]  # ToDo: Convert to models
        self.mention_roles = data.get("mention_roles")
        self.attachments = data.get("attachments", [])
        self.reactions = data.get("reactions", [])
        self.nonce = data.get("nonce")
        self.pinned = data.get("pinned", False)
        self.webhook_id = (
            Snowflake(data["webhook_id"])
            if data.get("webhook_id") is not None
            else None
        )
        self.type = try_enum(MessageType, data.get("type", 0))
        self.activity = data.get("activity")
        self.application = data.get("application")
        self.application_id = (
            Snowflake(data["application_id"])
            if data.get("application_id") is not None
            else None
        )
        self.message_reference = data.get(
            "message_reference"
        )  # ToDo: message reference object
        self.flags = try_enum(MessageFlags, data.get("flags", 0))
        self.referenced_message = (
            Message.from_dict(data["referenced_message"])
            if data.get("referenced_message") is not None
            else None
        )
        self.interaction = data.get("interaction")
        self.thread = (
            Thread.from_dict(data["thread"]) if data.get("thread") is not None else None
        )
        self.components = data.get("components")
        self.sticker_items = data.get("sticker_items")
        self.stickers = data.get("stickers")

        self.mention_channels = []
        self.embeds = []

        for channel in data.get("mention_channels", []):
            channel = _choose_channel_type(channel)
            self.mention_channels.append(channel)

        for embed in data.get("embeds", []):
            self.embeds.append(Embed.from_dict(embed))

        return self

    @property
    def guild(self):
        if self.guild_id is not None:
            return self._client.cache.get_guild(self.guild_id)
        return None

    @property
    def channel(self):
        print(self.channel_id)
        print(self._client.cache._channel_symlinks)
        if self.channel_id is not None:
            return self._client.cache.get_guild_channel(self.channel_id)

        return None

    async def pin(self, *, reason: Optional[str] = None):
        """|coro|

        Pins the message.

        You must have the ``MANAGE_MESSAGES`` permission to do this in a non-private channel context.

        Parameters
        ----------
        reason: Optional[:class:`str`]
            The reason for pinning the message. Shows up on the audit log.

        Raises
        -------
        HTTPException
            Pinning the message failed,
            probably due to the channel having more than 50 pinned messages.
        ForbiddenError
            You do not have permissions to pin the message.
        NotFound
            The message or channel was not found or deleted.
        """

        await self._http.put(
            f"channels/{self.channel_id}/pins/{self.id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def unpin(self, *, reason: Optional[str] = None):
        """|coro|

        Unpins the message.

        You must have the ``MANAGE_MESSAGES`` permission to do this in a non-private channel context.

        Parameters
        ----------
        reason: Optional[:class:`str`]
            The reason for unpinning the message. Shows up on the audit log.

        Raises
        -------
        HTTPException
            Pinning the message failed,
            probably due to the channel having more than 50 pinned messages.
        ForbiddenError
            You do not have permissions to unpin the message.
        NotFound
            The message or channel was not found or deleted.
        """

        await self._http.delete(
            f"channels/{self.channel_id}/pins/{self.id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def delete(self, *, delay: Optional[float] = None) -> None:
        """|coro|

        Deletes the message.

        Parameters
        ----------
        delay: Optional[:class:`float`]
            If provided, the number of seconds to wait in the background
            before deleting the message.

        Raises
        ------
        Forbidden
            You do not have proper permissions to delete the message.
        NotFound
            The message was deleted already
        HTTPException
            Deleting the message failed.
        """

        if delay is not None:

            async def delete(delete_after: float):
                await asyncio.sleep(delete_after)
                await self._client.rest.delete_message(self.channel_id, self.id)

            asyncio.create_task(delete(delay))
        else:
            await self._client.rest.delete_message(self.channel_id, self.id)
