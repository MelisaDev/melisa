# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import List, TYPE_CHECKING, Optional

from ...utils import Snowflake, Timestamp
from ...utils import APIModelBase
from ...utils.types import APINullable

if TYPE_CHECKING:
    from ..guild.channel import Thread


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
class Message(APIModelBase):
    """Represents a message sent in a channel within Discord.

    Attributes
    ----------
    id: :class:`~melisa.utils.types.snowflake.Snowflake`
        Id of the message
    channel_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        Id of the channel the message was sent in
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
    type: :class:`int`
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
    author: APINullable[List] = None
    member: APINullable[List] = None
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
    type: APINullable[int] = None
    activity: APINullable[List] = None
    application: APINullable[List] = None
    application_id: APINullable[Snowflake] = None
    message_reference: APINullable[List] = None
    flags: APINullable[int] = None
    interaction: APINullable[List] = None
    thread: APINullable[Thread] = None
    components: APINullable[List] = None
    sticker_items: APINullable[List] = None
    stickers: APINullable[List] = None

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
