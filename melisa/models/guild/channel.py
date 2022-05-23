# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import IntEnum
from typing import (
    List,
    Any,
    Optional,
    AsyncIterator,
    Union,
    Dict,
    overload,
    TYPE_CHECKING,
)

from ..message.file import File, create_form
from ..message.message import Message, AllowedMentions
from ...exceptions import EmbedFieldError
from ...models.message.embed import Embed
from ...utils import Snowflake, Timestamp
from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED

if TYPE_CHECKING:
    from .thread import ThreadMember, ThreadMetadata


def _choose_channel_type(data):
    data.update({"type": ChannelType(data.pop("type"))})

    channel_cls = channel_types_for_converting.get(data["type"], NoneTypedChannel)
    return channel_cls.from_dict(data)


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
        A temporary sub-channel within a ``GUILD_NEWS`` channel
    GUILD_PUBLIC_THREAD:
        A temporary sub-channel within a ``GUILD_TEXT`` channel
    GUILD_PRIVATE_THREAD:
        A temporary sub-channel within a ``GUILD_TEXT`` channel that is only viewable
        by those invited and those with the MANAGE_THREADS permission
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
    """Represents a guild or DM channel within Discord

    **It will be never returned!**

    Attributes
    ----------
    id: :class:`~melisa.utils.types.Snowflake`
        The id of this channel
    type: :class:`int`
        The type of channel
    guild_id: :class:`~melisa.utils.types.Snowflake`
        The id of the guild
        (may be missing for some channel objects received over gateway guild dispatches)
    guild: Optional[:class:`~melisa.models.guild.Guild`]
        Object of guild where channel is
    position: :class:`int`
        Sorting position of the channel
    permission_overwrites: :class:`typing.Any`
        Explicit permission overwrites for members and roles
    name: :class:`str`
        The name of the channel (1-100 characters)
    topic: :class:`str`
        The channel topic (0-1024 characters)
    nsfw: :class:`bool`
        Whether the channel is nsfw
    last_message_id: :class:`~melisa.utils.types.Snowflake`
        The id of the last message sent in this channel
        (may not point to an existing or valid message)
    bitrate: :class:`int`
        The bitrate (in bits) of the voice channel
    user_limit: :class:`int`
        The user limit of the voice channel
    rate_limit_per_user: :class:`int`
        Amount of seconds a user has to wait before sending another message (0-21600);
        bots, as well as users with the permission
        ``MANAGE_MESSAGES`` and ``MANAGE_CHANNEL``, are unaffected
    recipients: :class:`typing.Any`
        The recipients of the DM
    icon: :class:`str`
        Icon hash of the group DM
    owner_id: :class:`~melisa.utils.types.Snowflake`
        Id of the creator of the group DM or thread
    application_id: :class:`~melisa.utils.types.Snowflake`
        Application id of the group DM creator if it is bot-created
    parent_id: :class:`~melisa.utils.types.Snowflake`
        For guild channels: id of the parent category for a channel
        (each parent category can contain up to 50 channels),
        for threads: id of the text channel this thread was created
    last_pin_timestamp: :class:`~melisa.utils.timestamp.Timestamp`
        When the last pinned message was pinned.
        This may be `null` in events such as `GUILD_CREATE` when a message is not pinned.
    rtc_region: :class:`str`
        Voice region id for the voice channel, automatic when set to null
    video_quality_mode: :class:`int`
        The camera video quality mode of the voice channel, 1 when not present
    message_count: :class:`int`
        An approximate count of messages in a thread, stops counting at 50
    thread_metadata: :class:`~melisa.models.guild.thread.ThreadMetadata`
        Thread-specific fields not needed by other channels
    member: :class:`typing.Any`
        Thread member object for the current user,
        if they have joined the thread, only included on certain API endpoints
    default_auto_archive_duration: :class:`int`
        default duration that the clients (not the API) will use for newly created threads,
        in minutes, to automatically archive the thread after recent activity,
        can be set to: 60, 1440, 4320, 10080
    permissions: :class:`str`
        Computed permissions for the invoking user in the channel, including overwrites,
        only included when part of the `resolved` data received on a slash command interaction
    """

    id: APINullable[Snowflake] = None
    type: APINullable[int] = None
    guild_id: APINullable[Snowflake] = None
    position: APINullable[int] = None
    permission_overwrites: APINullable[List] = None
    name: APINullable[str] = None
    topic: APINullable[str] = None
    nsfw: APINullable[bool] = None
    last_message_id: APINullable[Snowflake] = None
    bitrate: APINullable[int] = None
    user_limit: APINullable[int] = None
    rate_limit_per_user: APINullable[int] = None
    recipients: APINullable[List] = None
    icon: APINullable[str] = None
    owner_id: APINullable[Snowflake] = None
    application_id: APINullable[Snowflake] = None
    parent_id: APINullable[Snowflake] = None
    last_pin_timestamp: APINullable[Timestamp] = None
    rtc_region: APINullable[str] = None
    video_quality_mode: APINullable[int] = None
    message_count: APINullable[int] = None
    member_count: APINullable[int] = None
    thread_metadata: APINullable[ThreadMetadata] = None
    member: APINullable[List] = None
    default_auto_archive_duration: APINullable[int] = None
    permissions: APINullable[str] = None

    @property
    def mention(self):
        return f"<#{self.id}>"

    @property
    def guild(self):
        if self.guild_id is not None:
            return self._client.cache.get_guild(self.guild_id)
        return None

    async def edit(self, *, reason: Optional[str] = None, **kwargs):
        """|coro|
        Edit a channel with the specified keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~melisa.models.guild.channel.Channel`
            The updated channel object.
        """
        data = await self._http.patch(
            f"channels/{self.id}",
            data=kwargs,
            headers={"X-Audit-Log-Reason": reason},
        )

        return _choose_channel_type(data)

    async def delete(self, *, reason: Optional[str] = None):
        """|coro|

        Delete a channel, or close a private message.
        Deleting a category does not delete its child channels;
        they will have their parent_id removed.

        Parameters
        ----------
        reason: Optional[:class:`str`]
            The reason of the delete channel operation.

        Raises
        -------
        NotFoundError
            If channel is not found.
        ForbiddenError
            You do not have proper permissions to do the actions required.

        Returns
        -------
        Channel
            Channel object.
        """

        data = await self._http.delete(
            f"/channels/{self.id}", headers={"X-Audit-Log-Reason": reason}
        )

        return _choose_channel_type(data)


class MessageableChannel(Channel):
    """A subclass of ``Channel`` with methods that are only available for channels,
    where user can send messages."""

    async def start_thread_without_message(
        self,
        *,
        name: str,
        type: ChannelType,
        auto_archive_duration: Optional[int] = None,
        invitable: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Union[Channel, Any]:
        """|coro|

        Creates a new thread that is not connected to an existing message.
        The created thread defaults to a ``GUILD_PRIVATE_THREAD``.

        Creating a private thread requires the server to be boosted.
        The guild features will indicate if that is possible for the guild.
        The 3 day and 7 day archive durations require the server to be boosted.
        The guild features will indicate if that is possible for the guild.


        Parameters
        ----------
        name: Optional[:class:`str`]
            The name of the thread. 1-100 characters.
        auto_archive_duration: Optional[:class:`int`]
            The duration in minutes to automatically archive the thread after
            recent activity, can be set to: ``60``, ``1440``, ``4320``, ``10080``.
        type: Optional[:class:`~melisa.models.guild.channel.ChannelType`]
            The type of thread to create.
        invitable: Optional[:class:`bool`]
            Whether non-moderators can add other non-moderators to a thread;
            only available when creating a private thread.
        rate_limit_per_user: Optional[:class:`int`]
            Amount of seconds a user has to wait before sending another message.
            (0-21600)
        reason: Optional[:class:`str`]
            The reason of the thread creation.

        Raises
        -------
        ForbiddenError
            You do not have proper permissions to do the actions required.
        HTTPException
            The request to perform the action failed with other http exception.

        Returns
        -------
        Union[:class:`~melisa.models.guild.channel.Channel`,
        :class:`Any`]
            The created thread.
        """

        data = await self._http.post(
            f"channels/{self.id}/threads",
            headers={"X-Audit-Log-Reason": reason},
            data={
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "type": type,
                "invitable": invitable,
                "rate_limit_per_user": rate_limit_per_user,
            },
        )

        return Thread.from_dict(data)

    async def history(
        self,
        limit: int = 50,
        *,
        before: Optional[Snowflake] = None,
        after: Optional[Snowflake] = None,
        around: Optional[Snowflake] = None,
    ) -> AsyncIterator[Message]:
        """|coro|

        Returns a list of messages in this channel.

        Examples
        ---------
        Flattening messages into a list: ::

            messages = [message async for message in channel.history(limit=111)]


        All parameters are optional.

        Parameters
        ----------
        limit : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Max number of messages to return (1-100).
        around : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Get messages around this message ID.
        before : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Get messages before this message ID.
        after : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Get messages after this message ID.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.

        Returns
        -------
        AsyncIterator[:class:`~melisa.models.message.message.Message`]
            An iterator of messages.
        """

        # ToDo: Add check parameter

        if limit is None:
            limit = 100

        while limit > 0:
            search_limit = min(limit, 100)

            raw_messages = await self._http.get(
                f"/channels/{self.id}/messages",
                params={
                    "limit": search_limit,
                    "before": before,
                    "after": after,
                    "around": around,
                },
            )

            if not raw_messages:
                break

            for message_data in raw_messages:
                yield Message.from_dict(message_data)

            before = raw_messages[-1]["id"]
            limit -= search_limit

    async def fetch_message(
        self,
        message_id: Optional[Snowflake, int, str],
    ) -> Message:
        """|coro|

        Returns a specific message in the channel.

        Parameters
        ----------
        message_id : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Id of message to fetch.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.

        Returns
        -------
        :class:`~melisa.models.message.message.Message`
            Message object.
        """

        message = await self._http.get(
            f"/channels/{self.id}/messages/{message_id}",
        )

        return Message.from_dict(message)

    async def pins(self) -> AsyncIterator[Message]:
        """|coro|

        Retrieves all messages that are currently pinned in the channel.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.

        Returns
        -------
        AsyncIterator[:class:`~melisa.models.message.message.Message`]
            AsyncIterator of Message objects.
        """

        messages = await self._http.get(
            f"/channels/{self.id}/pins",
        )

        for message in messages:
            yield Message.from_dict(message)

    async def bulk_delete_messages(
        self, messages: List[Snowflake], *, reason: Optional[str] = None
    ):
        """|coro|

        Delete multiple messages in a single request.
        This method will not delete messages older than 2 weeks.

        Parameters
        ----------
        messages: List[:class:`~.melisa.utils.snowflake.Snowflake`]
            The list of message IDs to delete (2-100).
        reason: Optional[:class:`str`]
            The reason of the bulk delete messages operation.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have ``MANAGE_MESSAGES`` permission)
        """
        await self._http.post(
            f"channels/{self.id}/messages/bulk-delete",
            headers={"X-Audit-Log-Reason": reason},
            data={"messages": messages},
        )

    async def delete_message(
        self, message_id: Union[Snowflake, str, int], *, reason: Optional[str] = None
    ):
        """|coro|

        Deletes only one specified message.

        Parameters
        ----------
        message_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of message to delete.
        reason: Optional[:class:`str`]
            The reason of the message delete operation.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have ``MANAGE_MESSAGES`` permission)
        """
        await self._client.rest.delete_message(self.id, message_id, reason=reason)

    async def send(
        self,
        content: str = None,
        *,
        tts: bool = False,
        embed: Embed = None,
        embeds: List[Embed] = None,
        file: File = None,
        files: List[File] = None,
        allowed_mentions: AllowedMentions = None,
        delete_after: int = None,
    ) -> Message:
        """|coro|

        Sends a message to the destination with the content given.

        The content must be a type that can convert to a string through str(content).

        Parameters
        ----------
        content: Optional[:class:`str`]
            The content of the message to send.
        tts: Optional[:class:`bool`]
            Whether the message should be sent using text-to-speech.
        embed: Optional[:class:`~melisa.models.message.embed.Embed`]
            Embed
        embeds: Optional[List[:class:`~melisa.models.message.embed.Embed`]]
            List of embeds
        file: Optional[:class:`~melisa.models.message.file.File`]
            File
        files: Optional[List[:class:`~melisa.models.message.file.File`]]
            List of files
        allowed_mentions: Optional[:class:`~melisa.models.message.message.AllowedMentions`]
            Controls the mentions being processed in this message.
        delete_after: Optional[:class:`int`]
            Provided value must be an int.
            if provided, deletes message after some seconds.
            May raise ``ForbiddenError`` or ``NotFoundError``.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have the proper permissions to send the message.
        BadRequestError
            Some of specified parameters is invalid.
        """

        # ToDo: Add other parameters
        # ToDo: add file checks

        if embeds is None:
            embeds = [embed.to_dict()] if embed is not None else []
        if files is None:
            files = [file] if file is not None else []

        payload = {"content": str(content) if content is not None else None}

        for _embed in embeds:
            if embed.total_length() > 6000:
                raise EmbedFieldError.characters_from_desc(
                    "Embed", embed.total_length(), 6000
                )

        payload["embeds"] = embeds
        payload["tts"] = tts

        # ToDo: add auto allowed_mentions from client
        if allowed_mentions is not None:
            payload["allowed_mentions"] = allowed_mentions.to_dict()
        elif self._client.allowed_mentions is not None:
            payload["allowed_mentions"] = self._client.allowed_mentions.to_dict()

        content_type, data = create_form(payload, files)

        message_data = Message.from_dict(
            await self._http.post(
                f"/channels/{self.id}/messages",
                data=data,
                headers={"Content-Type": content_type},
            )
        )

        if delete_after:
            await message_data.delete(delay=delete_after)

        return message_data

    async def purge(
        self,
        limit: int = 50,
        *,
        before: Optional[Snowflake] = None,
        after: Optional[Snowflake] = None,
        around: Optional[Snowflake] = None,
        reason: Optional[str] = None,
    ):
        """|coro|

        Purges a list of messages that meet the criteria specified in parameters.
        This method will not delete messages older than 2 weeks.

        Parameters
        ----------
        limit : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Max number of messages to purge.
        around : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Get messages around this message ID.
        before : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Get messages before this message ID.
        after : Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Get messages after this message ID.
        reason: Optional[:class:`str`]
            The reason of the channel purge operation.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have ``MANAGE_MESSAGES`` permission)
        """

        iterator = self.history(
            limit,
            around=around,
            before=before,
            after=after,
        )

        message_ids = []
        count = 0

        async for message in iterator:
            message_ids.append(message.id)
            count += 1

            if count == 100:
                await self.bulk_delete_messages(message_ids, reason=reason)
                message_ids = []
                count = 0
                await asyncio.sleep(1)

        await asyncio.sleep(1)

        if count > 1:
            await self.bulk_delete_messages(message_ids, reason=reason)
            return
        if count == 0:
            await self.delete_message(message_ids[0], reason=reason)
        return

    async def archived_threads(
        self,
        *,
        private: bool = False,
        joined: bool = False,
        before: Optional[Union[Snowflake, Timestamp]] = None,
        limit: Optional[int] = 50,
    ) -> ThreadsList:
        """|coro|

        Returns archived threads in the channel.

        Requires the ``READ_MESSAGE_HISTORY`` permission.
        If iterating over private threads then ``MANAGE_THREADS`` permission is also required.

        Parameters
        ----------
        before: Optional[Union[:class:`~melisa.utils.snowflake.Snowflake`,
        :class:`~melisa.utils.snowflake.Timestamp`]]
            Retrieve archived channels before the given date or ID.
        limit: Optional[:class:`int`]
            The number of threads to retrieve.
            If None, retrieves every archived thread in the channel.
            Note, however, that this would make it a slow operation
        private: :class:`bool`
            Whether to retrieve private archived threads.
        joined: :class:`bool`
            Whether to retrieve private archived threads that you’ve joined.
            You cannot set ``joined`` to ``True`` and ``private`` to ``False``.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have permissions to get archived threads.

        Returns
        -------
        :class:`~melisa.models.channel.ThreadsList`
            The threads list object.
        """

        if joined:
            url = f"/channels/{self.id}/users/@me/threads/archived/private"
        elif private:
            url = f"/channels/{self.id}/threads/archived/private"
        else:
            url = f"/channels/{self.id}/threads/archived/public"

        return ThreadsList.from_dict(
            await self._http.get(
                url,
                params={"before": before, "limit": limit},
            )
        )


class NoneTypedChannel(Channel):
    """It represents a channel, that is unknown,
    so we don't know this type of the channel,
    And also we can't convert it to something, but it has
    every method, that Channel has.

    You can use ``raw`` attribute to access to the original data,
    returned from the discord.

    Attributes
    ----------
    id: :class:`~melisa.utils.snowflake.Snowflake`
        Id of the channel
    raw: Dict[:class:`str`, Any]
        Raw value channel data (returned from the discord)
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a channel with unknown type from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into an unknown channel.
        """
        self: NoneTypedChannel = super().__new__(cls)

        self.id = data["id"]
        self.raw = data

        return self


class TextChannel(MessageableChannel):
    """A subclass of ``Channel`` representing text channels with all the same attributes."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate an text channel from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a text channel.
        """
        self: TextChannel = super().__new__(cls)

        self.id = data["id"]
        self.type = ChannelType(data["type"])
        self.position = data.get("position")
        self.permission_overwrites = data.get("permission_overwrites")
        self.name = data.get("name")
        self.topic = data.get("topic")
        self.nsfw = data.get("nsfw")

        if data.get("last_message_id") is not None:
            self.last_message_id = Snowflake(data.get("last_message_id", 0))
        else:
            self.last_message_id = None

        if data.get("guild_id") is not None:
            self.guild_id = Snowflake(data["guild_id"])
        else:
            self.guild_id = None

        self.rate_limit_per_user = data.get("rate_limit_per_user")

        if data.get("parent_id") is not None:
            self.parent_id = Snowflake(data["parent_id"])
        else:
            self.parent_id = None

        if data.get("last_pin_timestamp") is not None:
            self.last_pin_timestamp = Timestamp.parse(data.get("last_pin_timestamp", 0))
        else:
            self.last_pin_timestamp = None

        self.default_auto_archive_duration = data.get("default_auto_archive_duration")

        return self

    @overload
    async def edit(
        self,
        *,
        name: Optional[str] = None,
        type: Optional[ChannelType] = None,
        position: Optional[int] = None,
        topic: Optional[str] = None,
        nsfw: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        permission_overwrite: Optional[List[Dict[str, Any]]] = None,
        parent_id: Optional[Union[str, int, Snowflake]] = None,
        rtc_region: Optional[str] = None,
        video_quality_mode: Optional[int] = None,
        default_auto_archive_duration: Optional[int] = None,
    ) -> TextChannel:
        ...

    async def edit(self, **kwargs):
        """|coro|
        Edit a text channel with the specified keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~melisa.models.guild.channel.TextChannel`
            The updated channel object.
        """
        return await super().edit(**kwargs)

    async def create_webhook(
        self,
        *,
        name: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        """|coro|
        Creates a new webhook and returns a webhook object on success.
        Requires the ``MANAGE_WEBHOOKS`` permission.

        An error will be returned if a webhook name (`name`) is not valid.
        A webhook name is valid if:

        * It does not contain the substring 'clyde' (case-insensitive)
        * It follows the nickname guidelines in the Usernames
        and Nicknames documentation, with an exception that
        webhook names can be up to 80 characters

        Parameters
        ----------
        name: Optional[:class:`str`]
            Name of the webhook (1-80 characters)
        reason: Optional[:class:`str`]
            The reason for create the webhook. Shows up on the audit log.
        """

        await self._http.post(
            f"/channels/{self.id}/webhooks",
            headers={"name": name, "X-Audit-Log-Reason": reason},
        )


class Thread(MessageableChannel):
    """A subclass of ``Channel`` for threads with all the same attributes."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate an thread from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a thread.
        """
        self: Thread = super().__new__(cls)
        self.id = int(data["id"])
        self.parent_id = int(data.get("parent_id"))
        self.owner_id = Snowflake(data.get("owner_id"))
        self.name = data["name"]
        self.type = ChannelType(data.pop("type"))

        if data.get("last_message_id") is not None:
            self.last_message_id = Snowflake(data["last_message_id"])
        else:
            self.last_message_id = None

        self.slowmode_delay = data.get("rate_limit_per_user", 0)
        self.message_count = data.get("message_count")
        self.member_count = data.get("member_count")

        if data.get("last_pin_timestamp") is not None:
            self.last_pin_timestamp = Timestamp.parse(data["last_pin_timestamp"])
        else:
            self.last_pin_timestamp = None

        self.flags = data.get("flags", 0)
        self.__unroll_metadata(data["thread_metadata"])

        self.me = data.get("member")

        return self

    def __unroll_metadata(self, data: Dict[str, Any]):
        """Unroll metadata method, yup yup, you should't see this"""
        self.archived = data["archived"]
        self.auto_archive_duration = data["auto_archive_duration"]
        self.locked = data.get("locked", False)

        if data.get("create_timestamp") is not None:
            self.create_timestamp = Timestamp(data["create_timestamp"])
        else:
            self.create_timestamp = None

        if data.get("archive_timestamp") is not None:
            self.archive_timestamp = Timestamp(data["archive_timestamp"])
        else:
            self.archive_timestamp = None

    async def add_user(self, user_id: Snowflake):
        """|coro|

        Adds a user to this thread.

        You must have ``SEND_MESSAGES`` permission to add a user to a public thread.
        If the thread is private then ``SEND_MESSAGES`` and either ``CREATE_PRIVATE_THREADS``
        or manage_messages permissions is required to add a user to the thread.

        Parameters
        ----------
        user_id: :class:`~melisa.utils.Snowflake`
            Id of user to add to the thread.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have permissions to add the user to the thread.
        """

        await self._http.put(f"channels/{self.id}/thread-members/{user_id}")

    async def remove_user(self, user_id: Snowflake):
        """|coro|

        Removes a user from this thread.

        You must have ``MANAGE_THREADS`` or be the creator of the thread to remove a user.

        Parameters
        ----------
        user_id: :class:`~melisa.utils.Snowflake`
            Id of user to add to the thread.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have permissions to remove the user to the thread.
        """

        await self._http.delete(f"channels/{self.id}/thread-members/{user_id}")

    async def join(self):
        """|coro|

        Joins this thread.

        You must have ``SEND_MESSAGES_IN_THREADS`` to join a thread.
        If the thread is private, ``MANAGE_THREADS`` is also needed.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have permissions to join the thread.
        """

        await self._http.put(f"/channels/{self.id}/thread-members/@me")

    async def leave(self):
        """|coro|

        Leaves this thread.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        """

        await self._http.delete(f"/channels/{self.id}/thread-members/@me")


@dataclass(repr=False)
class ThreadsList(APIModelBase):
    """A class representing a list of channel threads from the Discord API.

    Attributes
    ----------
    threads: List[:class:`~melisa.models.guild.channel.Thread`]
        Async iterator of threads. To get their type use them `.type` attribute.
    members: List[:class:`~melisa.models.guild.thread.ThreadMember`]
        Async iterator of thread members.
    has_more: Optional[:class:`bool`]
        Whether there are potentially additional threads that could be returned on a subsequent cal
    """

    threads: List[Thread]
    members: List[ThreadMember]
    has_more: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate an threads list from the given dict.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into an threads list.
        """
        self: ThreadsList = super().__new__(cls)
        self.threads = [Thread.from_dict(thread) for thread in data["threads"]]
        self.members = [ThreadMember.from_dict(member) for member in data["members"]]
        self.has_more = data.get("has_more", False)
        return self


# noinspection PyTypeChecker
channel_types_for_converting: Dict[ChannelType, Channel] = {
    ChannelType.GUILD_TEXT: TextChannel,
    ChannelType.GUILD_NEWS_THREAD: Thread,
    ChannelType.GUILD_PUBLIC_THREAD: Thread,
    ChannelType.GUILD_PRIVATE_THREAD: Thread,
}
