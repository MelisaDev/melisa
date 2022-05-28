# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import datetime
from typing import Union, Optional, List, Dict, Any, AsyncIterator

from aiohttp import FormData

from .models.message import Embed, File, AllowedMentions, Message
from .exceptions import EmbedFieldError
from .core.http import HTTPClient
from .utils import json, UNDEFINED
from .utils.snowflake import Snowflake
from .models.guild.guild import Guild
from .models.user.user import User
from .models.guild.channel import _choose_channel_type, Channel


def create_form(payload: Dict[str, Any], files: List[File]):
    """
    Creates an aiohttp payload from an array of File objects.
    """
    form = FormData()
    form.add_field("payload_json", json.dumps(payload))

    for index, file in enumerate(files):
        form.add_field(
            "file",
            file.filepath,
            filename=file.filename,
            content_type="application/octet-stream",
        )

    payload = form()
    return payload.headers["Content-Type"], payload


class RESTApp:
    """
    This instance may be used to send http requests to the Discord REST API.

    **It will not cache anything.**

    Parameters
    ----------
    token: :class:`str`
        The token to authorize (you can found it in the developer portal)
    """

    def __init__(self, token: str):
        self._http: HTTPClient = HTTPClient(token)

    async def fetch_user(self, user_id: Union[Snowflake, int, str]) -> User:
        """|coro|

        [**REST API**] Fetch User from the Discord API (by id).

        Parameters
        ----------
        user_id: Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of user to fetch
        """

        data = await self._http.get(f"users/{user_id}")

        return User.from_dict(data)

    async def fetch_guild(self, guild_id: Union[Snowflake, int, str]) -> Guild:
        """|coro|

        [**REST API**] Fetch Guild from the Discord API (by id).

        Parameters
        ----------
        guild_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of guild to fetch
        """

        data = await self._http.get(f"guilds/{guild_id}")

        return Guild.from_dict(data)

    async def fetch_channel(self, channel_id: Union[Snowflake, str, int]) -> Channel:
        """|coro|

        [**REST API**] Fetch Channel from the Discord API (by id).

        Parameters
        ----------
        channel_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of channel to fetch
        """

        data = await self._http.get(f"channels/{channel_id}")

        return _choose_channel_type(data)

    async def delete_message(
        self,
        channel_id: Union[Snowflake, str, int],
        message_id: Union[Snowflake, str, int],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Deletes only one specified message.

        Parameters
        ----------
        channel_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel, where message should be deleted
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
        await self._http.delete(
            f"channels/{channel_id}/messages/{message_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def create_message(
        self,
        channel_id: Union[Snowflake, str, int],
        content: str = None,
        *,
        tts: bool = False,
        embed: Embed = None,
        embeds: List[Embed] = None,
        file: File = None,
        files: List[File] = None,
        allowed_mentions: AllowedMentions = None,
        delete_after: int = None,
        _client_allowed_mentions: AllowedMentions = None,
    ) -> Message:
        """|coro|

        [**REST API**] Create message.

        Sends a message to the destination with the content given.

        The content must be a type that can convert to a string through str(content).

        Parameters
        ----------
        channel_id:  Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel where message should be sent
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
        elif _client_allowed_mentions is not None:
            payload["allowed_mentions"] = _client_allowed_mentions.to_dict()

        content_type, data = create_form(payload, files)

        message_data = Message.from_dict(
            await self._http.post(
                f"/channels/{channel_id}/messages",
                data=data,
                headers={"Content-Type": content_type},
            )
        )

        if delete_after:
            await message_data.delete(delay=delete_after)

        return message_data

    async def get_channel_messages_history(
        self,
        channel_id: Union[Snowflake, str, int],
        limit: int = 50,
        *,
        before: Optional[Snowflake] = None,
        after: Optional[Snowflake] = None,
        around: Optional[Snowflake] = None,
    ) -> AsyncIterator[Message]:
        """|coro|

        [**REST API**] Fetch messages history.

        Returns a list of messages in this channel.

        Examples
        ---------
        Flattening messages into a list: ::

            messages = [message async for message in channel.history(limit=111)]


        All parameters are optional.

        Parameters
        ----------
        channel_id:  Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel where messages should be fetched.
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
                f"/channels/{channel_id}/messages",
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
        channel_id: Union[Snowflake, int, str],
        message_id: Union[Snowflake, int, str],
    ) -> Message:
        """|coro|

        [**REST API**] Fetch message.

        Returns a specific message in the channel.

        Parameters
        ----------
        message_id : Union[:class:`~.melisa.utils.snowflake.Snowflake`]
            Id of message to fetch.
        channel_id:  Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel where message should be fetched.

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
            f"/channels/{channel_id}/messages/{message_id}",
        )

        return Message.from_dict(message)

    async def fetch_channel_pins(
        self, channel_id: Union[Snowflake, int, str]
    ) -> AsyncIterator[Message]:
        """|coro|

        Retrieves all messages that are currently pinned in the channel.

        Parameters
        ----------
        channel_id:  Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel where messages should be fetched.

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
            f"/channels/{channel_id}/pins",
        )

        for message in messages:
            yield Message.from_dict(message)

    async def modify_guild_member(
        self,
        guild_id: Union[Snowflake, str, int],
        user_id: Union[Snowflake, str, int],
        *,
        nick: Optional[str] = UNDEFINED,
        roles: Optional[List[Snowflake]] = UNDEFINED,
        is_mute: Optional[bool] = UNDEFINED,
        is_deaf: Optional[bool] = UNDEFINED,
        voice_channel_id: Optional[Snowflake] = UNDEFINED,
        communication_disabled_until: Optional[datetime.datetime] = UNDEFINED,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Modify attributes of a guild member.

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of guild where we will modify member
        user_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of user to operate with.
        nick: Optional[:class:`str`]
            Value to set user's nickname to.

            **Required permissions:** ``MANAGE_NICKNAMES``
        roles: Optional[List[:class:`~.melisa.utils.snowflake.Snowflake`]]
            List of role ids the member is assigned

            **Required permissions:** ``MANAGE_ROLES``
        is_mute
            Whether the user is muted in voice channels.

            **Required permissions:** ``MUTE_MEMBERS``
        is_deaf
            Whether the user is deafened in voice channels.

            **Required permissions:** ``DEAFEN_MEMBERS``
        voice_channel_id: Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel to move user to (if they are connected to voice)

            **Required permissions:** ``MOVE_MEMBERS``
        communication_disabled_until: Optional[:class:`~melisa.utils.timestamp.Timestamp`]
            When the user's timeout will expire and the user will be able to communicate
            in the guild again (up to 28 days in the future),
            set to ``None`` to remove timeout.

            Will throw a 403 error if the user has the ``ADMINISTRATOR`` permission
            or is the owner of the guild

            **Required permissions:** ``MODERATE_MEMBERS``
        reason: Optional[:class:`str`]
            The reason of the action.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong type of argument, or you set ``is_deaf``,
            ``is_mute`` when user is not in the channel
        """

        data = {}

        if nick is not UNDEFINED:
            data["nick"] = nick
        if roles is not UNDEFINED:
            data["roles"] = roles
        if is_mute is not UNDEFINED:
            data["mute"] = is_mute
        if is_deaf is not UNDEFINED:
            data["deaf"] = is_deaf
        if voice_channel_id is not UNDEFINED:
            data["channel_id"] = voice_channel_id
        if communication_disabled_until is not UNDEFINED:
            data[
                "communication_disabled_until"
            ] = communication_disabled_until.isoformat()

        await self._http.patch(
            f"guilds/{guild_id}/members/{user_id}",
            data=data,
            headers={"X-Audit-Log-Reason": reason},
        )

    async def remove_guild_member(
        self,
        guild_id: Union[Snowflake, str, int],
        user_id: Union[Snowflake, str, int],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Remove a member from a guild.

        **Required permissions:** ``KICK_MEMBERS``

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of guild where we will remove member
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
            You provided a wrong guild, user or something else.
        """

        await self._http.delete(
            f"guilds/{guild_id}/members/{user_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def create_guild_ban(
        self,
        guild_id: Union[Snowflake, str, int],
        user_id: Union[Snowflake, str, int],
        *,
        delete_message_days: Optional[int] = 0,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Create a guild ban, and optionally
        delete previous messages sent by the banned user.

        **Required permissions:** ``BAN_MEMBERS``

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of guild where we will ban member
        user_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of user to operate with.
        delete_message_days: Optional[:class:`int`]
            Number of days to delete messages for (0-7)
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
        """

        await self._http.put(
            f"guilds/{guild_id}/bans/{user_id}",
            data={"delete_message_days": delete_message_days},
            headers={"X-Audit-Log-Reason": reason},
        )
