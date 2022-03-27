# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Any, Optional, AsyncIterator, Union, Dict

from ...utils import Snowflake
from ...utils import APIModelBase
from ...utils.types import APINullable


class ChannelType(IntEnum):
    """Channel Type
    NOTE: Type 10, 11 and 12 are only available in API v9 and older.

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

    @property
    def mention(self):
        return f"<#{self.id}>"


class TextChannel(Channel):
    """A subclass of ``Channel`` representing text channels with all the same attributes."""

    async def history(
        self,
        limit: int = 50,
        *,
        before: Optional[Union[int, str, Snowflake]] = None,
        after: Optional[Union[int, str, Snowflake]] = None,
        around: Optional[Union[int, str, Snowflake]] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        """|coro|
        Returns a list of messages in this channel.

        Examples
        ---------
        Flattening messages into a list: ::
            messages = [message async for message in channel.history(limit=111)]

        All parameters are optional.

        Parameters
        ----------
        limit : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Max number of messages to return (1-100).
        around : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Get messages around this message ID.
        before : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Get messages before this message ID.
        after : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Get messages after this message ID.

        Raises
        -------
        NotFoundError
            If channel is not found.
        ForbiddenError
            You do not have proper permissions to do the actions required.

        Returns
        -------
        AsyncIterator[Dict[:class:`str`, Any]]
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
                yield message_data

            before = raw_messages[-1]["id"]
            limit -= search_limit

    async def fetch_message(
        self,
        message_id: Optional[Snowflake, int, str],
    ) -> Dict[str, Any]:
        """|coro|
        Returns a specific message in the channel.

        Parameters
        ----------
        message_id : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Id of message to fetch.

        Raises
        -------
        NotFoundError
            If message is not found.
        ForbiddenError
            You do not have proper permissions to do the actions required.

        Returns
        -------
        Dict[:class:`str`, Any]
            Message object.
        """

        message = await self._http.get(
            f"/channels/{self.id}/messages/{message_id}",
        )

        return message

    async def bulk_delete_messages(
        self, messages: List[Snowflake], *, reason: Optional[str] = None
    ):
        """|coro|
        Delete multiple messages in a single request.
        This method will not delete messages older than 2 weeks.

        Parameters
        ----------
        messages: List[:class:`~.melisa.Snowflake`]
            The list of message IDs to delete (2-100).
        reason: Optional[:class:`str`]
            The reason of the bulk delete messages operation.

        Raises
        -------
        BadRequestError
            if any message provided is older than that or if any duplicate message IDs are provided.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have `MANAGE_MESSAGES` permission)
        """
        await self._http.post(
            f"channels/{self.id}/messages/bulk-delete",
            headers={"X-Audit-Log-Reason": reason},
            data={"messages": messages},
        )

    async def delete_message(
        self, message_id: Optional[Snowflake, str, int], *, reason: Optional[str] = None
    ):
        """|coro|
        Deletes only one specified message.

        Parameters
        ----------
        message_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]
            Id of message to delete.
        reason: Optional[:class:`str`]
            The reason of the message delete operation.

        Raises
        -------
        BadRequestError
            Something is wrong with request, maybe specified parameters.
        NotFoundError
            If message is not found.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have `MANAGE_MESSAGES` permission)
        """
        await self._http.delete(
            f"channels/{self.id}/messages/{message_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def purge(
        self,
        limit: int = 50,
        *,
        before: Optional[Union[int, str, Snowflake]] = None,
        after: Optional[Union[int, str, Snowflake]] = None,
        around: Optional[Union[int, str, Snowflake]] = None,
        reason: Optional[str] = None,
    ):
        """|coro|
        Purges a list of messages that meet the criteria specified in parameters.
        This method will not delete messages older than 2 weeks.

        Parameters
        ----------
        limit : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Max number of messages to purge.
        around : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Get messages around this message ID.
        before : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Get messages before this message ID.
        after : Optional[Union[:class:`int`, :class:`str`, :class:`~.melisa.Snowflake`]]
            Get messages after this message ID.
        reason: Optional[:class:`str`]
            The reason of the channel purge operation.

        Raises
        -------
        BadRequestError
            if any message provided is older than that or if any duplicate message IDs are provided.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have `MANAGE_MESSAGES` permission)
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
            message_ids.append(message["id"])
            count += 1

            if count == 100:
                print("abobatelecom")
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


# noinspection PyTypeChecker
channel_types_for_converting: Dict[ChannelType, Channel] = {
    ChannelType.GUILD_TEXT: TextChannel
}
