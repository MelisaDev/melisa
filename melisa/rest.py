# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import datetime
from typing import Union, Optional, List, Dict, Any, AsyncIterator

from aiohttp import FormData

from .models.interactions import ApplicationCommandType
from .models.interactions.commands import (
    SlashCommandOption,
    SlashCommand,
    PartialApplicationCommand,
    _choose_command_type,
)
from .models.interactions.i18n import LocalizedField
from .models.interactions.interactions import Interaction, InteractionResponse
from .models.message import Embed, File, AllowedMentions, Message
from .exceptions import EmbedFieldError
from .core.http import HTTPClient
from .utils import json, UNDEFINED
from .utils.snowflake import Snowflake
from .models.guild.guild import Guild
from .models.user.user import User
from .models.guild.emoji import Emoji
from .models.guild.channel import _choose_channel_type, Channel


def create_form(files: List[File]):
    """
    Creates an aiohttp payload from an array of File objects.
    """
    form = FormData()

    for index, file in enumerate(files):
        form.add_field(
            "file",
            file.filepath,
            filename=file.filename,
            content_type="application/octet-stream",
        )

    return form


def _build_message_data(
    *,
    content: str = None,
    tts: bool = False,
    embed: Embed = None,
    embeds: List[Embed] = None,
    file: File = None,
    files: List[File] = None,
    allowed_mentions: AllowedMentions = None,
    _client_allowed_mentions: AllowedMentions = None,
):
    if embeds is None:
        embeds = [embed] if embed is not None else []
    if files is None:
        files = [file] if file is not None else []

    payload = {
        "content": str(content) if content is not None else None,
        "embeds": [],
    }

    for _embed in embeds:
        if _embed.total_length() > 6000:
            raise EmbedFieldError.characters_from_desc(
                "Embed", embed.total_length(), 6000
            )
        payload["embeds"].append(_embed.to_dict())

    payload["tts"] = tts

    if allowed_mentions is not None:
        payload["allowed_mentions"] = allowed_mentions.to_dict()
    elif _client_allowed_mentions is not None:
        payload["allowed_mentions"] = _client_allowed_mentions.to_dict()

    if len(files) > 0:
        form_builder = create_form(files)
        return payload, form_builder

    return payload, None


class RESTApp:
    """
    This instance may be used to send http requests to the Discord REST API.

    **It will not cache anything.**

    Parameters
    ----------
    token: :class:`str`
        The token to authorize (you can found it in the developer portal)
    default_image_format: :class:`str`
        Default image format

    Attributes
    -----------
    cdn: :class:`~melisa.rest.CDNBuilder`
        CDN Builder to build images
    """

    def __init__(self, token: str, default_image_format: str = None):
        self._http: HTTPClient = HTTPClient(token)
        self.cdn = CDNBuilder(default_image_format)

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

    async def get_original_interaction_response(
        self, application_id: Union[Snowflake, str, int], interaction_token: str
    ) -> Message:
        """|coro|

        [**REST API**] Fetch Original Interaction Response from the Discord API.

        Parameters
        ----------
        application_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of interaction to fetch
        interaction_token: str
            Interaction token
        """

        data = await self._http.get(
            f"/webhooks/{application_id}/{interaction_token}/messages/@original"
        )

        return Message.from_dict(data)

    async def delete_original_interaction_response(
        self, application_id: Union[Snowflake, str, int], interaction_token: str
    ) -> Message:
        """|coro|

        [**REST API**] Delete Original Interaction Response.

        Parameters
        ----------
        application_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of interaction to fetch
        interaction_token: str
            Interaction token
        """

        await self._http.delete(
            f"/webhooks/{application_id}/{interaction_token}/messages/@original"
        )

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

        body, form_builder = _build_message_data(
            content=content,
            file=file,
            files=files,
            embed=embed,
            embeds=embeds,
            tts=tts,
            allowed_mentions=allowed_mentions,
            _client_allowed_mentions=_client_allowed_mentions,
        )

        if form_builder is not None:
            form_builder.add_field("payload_json", json.dumps(body))

            form = form_builder()

            message_data = Message.from_dict(
                await self._http.post(
                    f"/channels/{channel_id}/messages",
                    data=form,
                    headers={"Content-Type": form.headers["Content-Type"]},
                )
            )
        else:
            message_data = Message.from_dict(
                await self._http.post(
                    f"/channels/{channel_id}/messages",
                    json=body,
                    headers={"Content-Type": "application/json"},
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

    async def remove_guild_ban(
        self,
        guild_id: Union[Snowflake, str, int],
        user_id: Union[Snowflake, str, int],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Remove the ban for a user.

        **Required permissions:** ``BAN_MEMBERS``

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of guild where we will remove ban for member
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

        await self._http.delete(
            f"guilds/{guild_id}/bans/{user_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def add_guild_member_role(
        self,
        guild_id: Union[Snowflake, str, int],
        user_id: Union[Snowflake, str, int],
        role_id: Union[Snowflake, str, int],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Adds a role to a guild member.

        **Required permissions:** ``MANAGE_ROLES``

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of guild where we will give member role
        user_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of user to operate with.
        role_id: Optional[:class:`int`]
            Id of role to give.
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
            f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def remove_guild_member_role(
        self,
        guild_id: Union[Snowflake, str, int],
        user_id: Union[Snowflake, str, int],
        role_id: Union[Snowflake, str, int],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Removes a role from a guild member.

        **Required permissions:** ``MANAGE_ROLES``

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of guild where we will remove member role
        user_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of user to operate with.
        role_id: Optional[:class:`int`]
            Id of role to remove.
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

        await self._http.delete(
            f"guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def list_guild_emojis(
        self,
        guild_id: Union[Snowflake, str, int],
    ):
        """|coro|

        [**REST API**] Getting all emojis from guild

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            ID of the guild in which we will get the list of emojis

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong guild
        """
        return [
            Emoji.from_dict(emoji)
            for emoji in await self._http.get(f"/guilds/{guild_id}/emojis")
        ]

    async def get_guild_emoji(
        self, guild_id: Union[Snowflake, str, int], emoji_id: Union[Snowflake, str, int]
    ):
        """|coro|

        [**REST API**] Get emoji from guild

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
           The ID of the guild in which we will receive emoji
        emoji_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            The ID of the emoji that we will get

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong guild and emoji
        """

        await self._http.get(f"/guilds/{guild_id}/emojis/{emoji_id}")

    async def create_guild_emoji(
        self,
        guild_id: Union[int, str, Snowflake],
        emoji_name: str,
        emoji_image: Any,
        *,
        reason: Optional[str] = None,
        role_id: Union[int, str, Snowflake] = None,
    ):
        # FIXME: emoji_image != str, it works another way
        """|coro|

        [**REST API**] Create a new emoji for the guild.
        **Required permissions:** ``MANAGE_EMOJIS_AND_STICKERS``.

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
           ID of the guild in which we will create emoji
        emoji_name: Optional[:class:`str`]
            Name of the emoji
        emoji_image: Optional[:class:`str`]
            The 128x128 emoji image
        reason: Optional[:class:`str`]
            The reason of the action
        role_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Roles allowed to use this emoji

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong guild
        """

        data = {"name": emoji_name, "image": emoji_image, "roles": role_id}

        return Emoji.from_dict(
            await self._http.post(
                f"/guilds/{guild_id}/emojis",
                json=data,
                headers={"X-Audit-Log-Reason": reason},
            )
        )

    async def modify_guild_emoji(
        self,
        guild_id: Union[int, str, Snowflake],
        emoji_id: Union[int, str, Snowflake],
        emoji_name: Optional[str],
        *,
        reason: Optional[str] = None,
        role_id: Union[int, str, Snowflake] = None,
    ):
        """|coro|

        [**REST API**] Modify the given emoji.
        **Required permissions:** ``MANAGE_EMOJIS_AND_STICKERS``.

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
           ID of the guild in which we will modify emoji
        emoji_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            The ID of the emoji that we will modify
        emoji_name: Optional[:class:`str`]
            Name of the emoji
        reason: Optional[:class:`str`]
            The reason of the action
        role_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Roles allowed to use this emoji

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong guild and emoji
        """

        data = {"name": emoji_name, "roles": role_id}

        return Emoji.from_dict(
            await self._http.patch(
                f"/guilds/{guild_id}/emojis/{emoji_id}",
                json=data,
                headers={"X-Audit-Log-Reason": reason},
            )
        )

    async def delete_guild_emoji(
        self,
        guild_id: Union[int, str, Snowflake],
        emoji_id: Union[int, str, Snowflake],
        *,
        reason: Optional[str] = None,
    ):
        """|coro|

        [**REST API**] Delete the given emoji
        **Required permissions:** ``MANAGE_EMOJIS_AND_STICKERS``.

        Parameters
        ----------
        guild_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
           ID of the guild in which we will delete emoji
        emoji_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            The ID of the emoji that we will delete
        reason: Optional[:class:`str`]
            The reason of the action

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong guild and emoji
        """

        await self._http.delete(
            f"/guilds/{guild_id}/emojis/{emoji_id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def get_global_application_commands(
        self,
        application_id: Union[int, str, Snowflake],
        *,
        with_localizations: Optional[bool] = False,
    ) -> List[PartialApplicationCommand]:
        """|coro|

        [**REST API**] Fetch all of the global commands for your application.

        Parameters
        ----------
        application_id: :class:`~melisa.utils.snowflake.Snowflake`
            ID of the parent application
        with_localizations: Optional[bool]
            Whether to include full localization dictionaries
            (``name_localizations`` and ``description_localizations``) in
            the returned objects, instead of the ``name_localized`
            and ``description_localized fields``. Default ``False``.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        return [
            _choose_command_type(x)
            for x in await self._http.get(
                f"/applications/{application_id}/commands?with_localizations={with_localizations}"
            )
        ]

    async def create_global_application_command(
        self,
        application_id: Union[int, str, Snowflake],
        command_type: ApplicationCommandType,
        name: LocalizedField,
        description: LocalizedField = None,
        *,
        options: Optional[List[SlashCommandOption]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = None,
        default_permission: Optional[bool] = None,
    ) -> PartialApplicationCommand:
        """|coro|

        [**REST API**] Create a new global command.

        Parameters
        ----------
        application_id: :class:`~melisa.utils.snowflake.Snowflake`
            ID of the parent application
        command_type: Optional[:class:`~melisa.interactions.commands.ApplicationCommandType`]
            Type of command, defaults to ``1``
        name: :class:`~melisa.models.interactions.i18n.LocalizedField`
            Name of command, 1-32 characters
        description: Optional[:class:`~melisa.models.interactions.i18n.LocalizedField`]
            Description for ``CHAT_INPUT`` commands, 1-100 characters.
            Empty string for ``USER`` and ``MESSAGE`` commands
        options: Optional[List[:class:`~melisa.models.interactions.commands.SlashCommandOption`]]
            Parameters for the command, max of 25.
            Only available for ``CHAT_INPUT`` command type.
        default_member_permissions: Optional[str]
            Set of permissions represented as a bit set
        dm_permission: Optional[bool]
            Indicates whether the command is available
            in DMs with the app, only for globally-scoped commands.
            By default, commands are visible.
        default_permission: Optional[bool]
            Not recommended for use as field will soon be deprecated.
            Indicates whether the command is enabled by default
            when the app is added to a guild, defaults to ``True``

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        data = {
            "name": name.original,
            "type": int(command_type),
        }

        if name.localizations is not None:
            data["name_localizations"] = name.localizations

        if description.original is not None:
            data["description"] = description.original

        if description.localizations is not None:
            data["description_localizations"] = description.localizations

        if default_member_permissions is not None:
            data["default_member_permissions"] = default_member_permissions

        if options is not None:
            for option in options:
                option_data = option.to_dict()

                option_data["name"] = option.name.original
                option_data["description"] = option.description.original

                if option.name.localizations is not None:
                    option_data["name_localizations"] = option.name.localizations
                if option.description.localizations is not None:
                    option_data[
                        "description_localizations"
                    ] = option.description.localizations

        if dm_permission is not None:
            data["dm_permission"] = dm_permission

        if default_permission is not None:
            data["default_permission"] = default_permission

        return _choose_command_type(
            await self._http.post(f"/applications/{application_id}/commands", json=data)
        )

    async def get_global_application_command(
        self,
        application_id: Union[int, str, Snowflake],
        command_id: Union[int, str, Snowflake],
    ) -> PartialApplicationCommand:
        """|coro|

        [**REST API**] Fetch a global command for your application.

        Parameters
        ----------
        application_id: :class:`~melisa.utils.snowflake.Snowflake`
            ID of the parent application
        command_id: Optional[bool]
            ID of command to fetch.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        return _choose_command_type(
            await self._http.get(
                f"/applications/{application_id}/commands/{command_id}"
            )
        )

    async def edit_global_application_command(
        self,
        application_id: Union[int, str, Snowflake],
        command_id: Union[int, str, Snowflake],
        *,
        name: Optional[LocalizedField] = None,
        description: Optional[LocalizedField] = None,
        options: Optional[List[SlashCommandOption]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = None,
        default_permission: Optional[bool] = None,
    ) -> PartialApplicationCommand:
        """|coro|

        All parameters are optional, but any parameters
        provided will entirely overwrite the existing values of those parameters.

        [**REST API**] Edit a global command.

        Parameters
        ----------
        application_id: :class:`~melisa.utils.snowflake.Snowflake`
            ID of the parent application
        command_id: Optional[bool]
            ID of command to edit.
        name: Optional[:class:`~melisa.models.interactions.i18n.LocalizedField`]
            Name of command, 1-32 characters
        description: Optional[:class:`~melisa.models.interactions.i18n.LocalizedField`]
            Description for ``CHAT_INPUT`` commands, 1-100 characters.
            Empty string for ``USER`` and ``MESSAGE`` commands
        options: Optional[List[:class:`~melisa.models.interactions.commands.ApplicationCommandOption`]]
            Parameters for the command, max of 25.
            Only available for ``CHAT_INPUT`` command type.
        default_member_permissions: Optional[str]
            Set of permissions represented as a bit set
        dm_permission: Optional[bool]
            Indicates whether the command is available
            in DMs with the app, only for globally-scoped commands.
            By default, commands are visible.
        default_permission: Optional[bool]
            Not recommended for use as field will soon be deprecated.
            Indicates whether the command is enabled by default
            when the app is added to a guild, defaults to true

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        data = {}

        if name.original is not None:
            data["name"] = name.original

        if description.original is not None:
            data["description"] = description.original

        if name.localizations is not None:
            data["name_localizations"] = name.localizations

        if description.localizations is not None:
            data["description_localizations"] = description.localizations

        if default_member_permissions is not None:
            data["default_member_permissions"] = default_member_permissions

        data["options"] = []

        if options is not None:
            for option in options:
                option_data = option.to_dict()

                option_data["name"] = option.name.original
                option_data["description"] = option.description.original

                if option.name.localizations is not None:
                    option_data["name_localizations"] = option.name.localizations
                if option.description.localizations is not None:
                    option_data[
                        "description_localizations"
                    ] = option.description.localizations

                data["options"].append(option_data)

        if dm_permission is not None:
            data["dm_permission"] = dm_permission

        if default_permission is not None:
            data["default_permission"] = default_permission

        return _choose_command_type(
            await self._http.patch(
                f"/applications/{application_id}/commands/{command_id}", json=data
            )
        )

    async def delete_global_application_command(
        self,
        application_id: Union[int, str, Snowflake],
        command_id: Union[int, str, Snowflake],
    ) -> None:
        """|coro|

        [**REST API**] Delete a global command.

        Parameters
        ----------
        application_id: :class:`~melisa.utils.snowflake.Snowflake`
            ID of the parent application
        command_id: Optional[bool]
            ID of command to delete.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        await self._http.delete(f"/applications/{application_id}/commands/{command_id}")

        return None

    async def bulk_overwrite_global_application_commands(
        self,
        application_id: Union[int, str, Snowflake],
        commands: List[Union[SlashCommand, PartialApplicationCommand]],
    ) -> List[Union[SlashCommand, PartialApplicationCommand]]:
        """|coro|

        [**REST API**] Overwrites all existing global commands.

        Parameters
        ----------
        application_id: :class:`~melisa.utils.snowflake.Snowflake`
            ID of the parent application
        commands: List[Union[:class:`~melisa.models.interactions.commands.SlashCommand`,
        :class:`~melisa.models.interactions.commands.PartialApplicationCommand`]]

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        better_commands = []

        for command in commands:
            command_data = {
                "name": command.name.original,
                "type": int(command.type),
            }

            if command.name.localizations is not None:
                command_data["name_localizations"] = command.name.localizations

            if command.default_member_permissions is not None:
                command_data[
                    "default_member_permissions"
                ] = command.default_member_permissions

            if command.dm_permission is not None:
                command_data["dm_permission"] = command.dm_permission

            if isinstance(command, SlashCommand):
                if command.description is not None:
                    command_data["description"] = command.description.original

                if command.description.localizations is not None:
                    command_data[
                        "description_localizations"
                    ] = command.description.localizations

                command_data["options"] = []

                if command.options is not None:
                    for option in command.options:
                        option_data = option.to_dict()

                        option_data["name"] = option.name.original
                        option_data["description"] = option.description.original

                        if option.name.localizations is not None:
                            option_data[
                                "name_localizations"
                            ] = option.name.localizations
                        if option.description.localizations is not None:
                            option_data[
                                "description_localizations"
                            ] = option.description.localizations

                        command_data["options"].append(option_data)

                better_commands.append(command_data)

        return [
            _choose_command_type(x)
            for x in await self._http.put(
                f"/applications/{application_id}/commands", json=better_commands
            )
        ]

    async def interaction_respond(
        self,
        interaction: Interaction,
        interaction_response: InteractionResponse,
    ):
        """|coro|

        [**REST API**] Respond to an interaciton

        Parameters
        ----------
        interaction: :class:`~melisa.models.interactions.interactions.Interaction`
            Interaction to respond to
        interaction_response: :class:`~melisa.models.interactions.interactions.InteractionResponse`
            InteractionResponse`e``

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
        BadRequestError
            You provided a wrong arguments
        """

        return await self._http.post(
            f"/interactions/{interaction.id}/{interaction.token}/callback",
            json=interaction_response.to_dict(),
        )


class CDNBuilder:
    """Can be used to build images

    Parameters
    ----------
    default_image_format: :class:`str`
        Default image format
    """

    # ToDo: Add docstrings

    BASE_URL = "https://cdn.discordapp.com"

    def __init__(self, default_image_format: str = None):
        self.dif = default_image_format if default_image_format is not None else "png"

    def avatar_url(
        self, user_id: str, _hash: str, *, size: int = 1024, image_format: str = None
    ):
        return "{}/avatars/{}/{}.{}?size={}".format(
            self.BASE_URL,
            user_id,
            _hash,
            image_format if image_format is not None else self.dif,
            size,
        )

    def guild_icon_url(
        self, guild_id: str, _hash: str, *, size: int = 1024, image_format: str = None
    ):
        return "{}/icons/{}/{}.{}?size={}".format(
            self.BASE_URL,
            guild_id,
            _hash,
            image_format if image_format is not None else self.dif,
            size,
        )

    def default_avatar_url(self, discriminator: str):
        return "{}/embed/avatars/{}.png".format(self.BASE_URL, int(discriminator) % 5)

    def guild_member_avatar_url(
        self,
        guild_id: str,
        user_id: str,
        _hash: str,
        *,
        size: int = 1024,
        image_format: str = None,
    ):
        return "{}/guilds/{}/users/{}/avatars/{}.{}?size={}".format(
            self.BASE_URL,
            guild_id,
            user_id,
            _hash,
            image_format if image_format is not None else self.dif,
            size,
        )

    def role_icon_url(
        self,
        role_id: str,
        _hash: str,
        *,
        size: int = 1024,
        image_format: str = None,
    ):
        return "{}/role-icons/{}/{}.{}?size={}".format(
            self.BASE_URL,
            role_id,
            _hash,
            image_format if image_format is not None else self.dif,
            size,
        )
