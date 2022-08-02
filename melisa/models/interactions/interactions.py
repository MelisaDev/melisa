# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from typing import Dict, Any, Optional, List
from enum import IntEnum

from dataclasses import dataclass

from .commands import ApplicationCommandType
from .commands import SlashCommandInteractionDataOption
from ...models.message import Embed
from ...exceptions import EmbedFieldError
from ...utils.conversion import try_enum
from ...models.guild import Channel, Role, _choose_channel_type, GuildMember
from ...utils.api_model import APIModelBase
from ...models.message.message import Message, AllowedMentions, MessageFlags
from ...models.user.user import User
from ...utils.snowflake import Snowflake


class InteractionType(IntEnum):
    """Interaction Type

    Attributes
    ----------
    PING:
        Represents Discord pinging to see if the interaction response server is alive. (maybe shouldn't be there)
    APPLICATION_COMMAND:
        Represents an application command interaction.
    MESSAGE_COMPONENT:
        Represents a component based interaction (button or something like that)
    APPLICATION_COMMAND_AUTOCOMPLETE
        Represents an application command autocomplete interaction.
    MODAL_SUBMIT
        Represents a modal submit interaction.
    """

    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

    def __int__(self):
        return self.value


class InteractionCallbackType(IntEnum):
    """Interaction Callback Type

    Attributes
    ----------
    PONG:
        ACK a Ping
    CHANNEL_MESSAGE_WITH_SOURCE:
        Respond to an interaction with a message
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE:
        ACK an interaction and edit a response later, the user sees a loading state
    DEFERRED_UPDATE_MESSAGE:
        For components, ACK an interaction and edit the original message later; the user does not see a loading state
    UPDATE_MESSAGE:
        For components, edit the message the component was attached to
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT:
        Respond to an autocomplete interaction with suggested choices
    MODAL:
        Respond to an interaction with a popup modal
    """

    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9

    def __int__(self):
        return self.value


@dataclass(repr=False)
class InteractionResponse(APIModelBase):
    """Interaction Response

    Attributes
    ----------
    type: InteractionType
        The type of response
    data: Optional[Dict[str, Any]]
        An optional response message
    """

    type: InteractionCallbackType = None
    data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> InteractionResponse:
        """Generate a InteractionResponse from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a InteractionResponse.
        """
        self: InteractionResponse = super().__new__(cls)

        self.type = try_enum(InteractionCallbackType, data["type"])
        self.data = data.get("data", None)

        return self


@dataclass(repr=False)
class Interaction(APIModelBase):
    """Interaction

    Attributes
    ----------
    id: :class:`~melisa.utils.types.snowflake.Snowflake`
        ID of the interaction
    application_id:	:class:`~melisa.utils.types.snowflake.Snowflake`
        ID of the application this interaction is for
    type: :class:`~melisa.models.interactions.interactions.InteractionType`
        Type of interaction
    data: Optional[:class:`~melisa.models.interactions.interactions.ApplicationCommandData`]
        Interaction data payload
    guild_id: Optional[:class:`~melisa.utils.types.snowflake.Snowflake`]
        Guild that the interaction was sent from
    channel_id: Optional[:class:`~melisa.utils.types.snowflake.Snowflake`]
        Channel that the interaction was sent from
    member: Optional[:class:`~melisa.models.guild.member.GuildMember`]
        Guild member data for the invoking user, including permissions
    user: Optional[:class:`~melisa.models.user.user.User`]
        User object for the invoking user, if invoked in a DM
    token: str
        Continuation token for responding to the interaction
    version: int
        Read-only property, always 1
    message: Optional[:class:`~melisa.models.message.message.Message`]
        For components, the message they were attached to
    app_permissions: str
        Bitwise set of permissions the app or bot has within the channel the interaction was sent from
    locale: Optional[str]
        Selected language of the invoking user
    guild_locale: Optional[str]
        Guild's preferred locale, if invoked in a guild
    """

    id: Snowflake = None
    application_id: Snowflake = None
    type: InteractionType = None
    data: Optional[ApplicationCommandData] = None
    guild_id: Optional[Snowflake] = None
    channel_id: Optional[Snowflake] = None
    member: Optional[GuildMember] = None
    user: Optional[User] = None
    token: str = None
    version: int = None
    message: Optional[Message] = None
    app_permissions: str = None
    locale: Optional[str] = None
    guild_locale: Optional[str] = None
    _is_responded: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a Interaction from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a Interaction.
        """
        self: Interaction = super().__new__(cls)

        self.id = Snowflake(data.get("id", 0))
        self.application_id = Snowflake(data.get("application_id", 0))
        self.type = (
            try_enum(ApplicationCommandType, data["type"])
            if data.get("type", None) is not None
            else None
        )
        self.data = (
            ApplicationCommandData.from_dict(data["data"])
            if data.get("data", None) is not None
            else None
        )
        self.guild_id = (
            Snowflake(data["guild_id"])
            if data.get("guild_id", None) is not None
            else None
        )
        self.channel_id = (
            Snowflake(data["channel_id"])
            if data.get("channel_id", None) is not None
            else None
        )
        self.member = (
            GuildMember.from_dict(data["member"])
            if data.get("member", None) is not None
            else None
        )
        self.user = (
            User.from_dict(data["user"]) if data.get("user", None) is not None else None
        )
        self.token = data.get("token")
        self.version = data.get("version")
        self.message = (
            Message.from_dict(data["message"])
            if data.get("message", None) is not None
            else None
        )
        self.app_permissions = data.get("app_permissions")
        self.locale = data.get("locale", None)
        self.guild_locale = data.get("guild_locale", None)

        return self

    @property
    def is_responded(self) -> bool:
        """Whether an interaction has been responded before."""
        return self._is_responded

    async def respond(self, response: InteractionResponse):
        """
        Respond to an interaction.

        Parameters
        ----------
        response: :class:`~melisa.models.interactions.interactions.InteractionResponse`
            The response to send.
        """

        await self._client.rest.interaction_respond(self, response)

    async def defer(
        self,
        *,
        with_message: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:
        """|coro|

        Respond to an interaction with a message.

        The content must be a type that can convert to a string through str(content).

        Parameters
        ----------
        with_message: Optional[:class:`bool`]
            Whether the response will be a message with thinking state (bot is thinking…)
        ephemeral: Optional[:class:`bool`]
            Whether the message should be an ephemeral message. Defaults to False.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have the proper permissions to send the message.
        BadRequestError
            Some of specified parameters is invalid.
        """

        defer_callback_type = None
        data = {}

        if self.type not in (
            InteractionType.APPLICATION_COMMAND,
            InteractionType.MODAL_SUBMIT,
            InteractionType.MESSAGE_COMPONENT,
        ):
            raise TypeError(
                "This interaction must be of type 'APPLICATION_COMMAND', 'MESSAGE_COMPONENT' or 'MODAL_SUBMIT' to defer."
            )

        if with_message:
            defer_callback_type = (
                InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            )

            if ephemeral:
                data["flags"] = MessageFlags.EPHEMERAL.value
        else:
            defer_callback_type = InteractionCallbackType.DEFERRED_UPDATE_MESSAGE

        return await self.respond(
            InteractionResponse.from_dict(
                {
                    "type": defer_callback_type,
                    "data": data,
                }
            )
        )

    async def send_message(
        self,
        content: Optional[str] = None,
        *,
        tts: Optional[bool] = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions: Optional[AllowedMentions] = None,
        ephemeral: Optional[bool] = False,
    ) -> None:
        """|coro|

        Respond to an interaction with a message.

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
        allowed_mentions: Optional[:class:`~melisa.models.message.message.AllowedMentions`]
            Controls the mentions being processed in this message.
        ephemeral: Optional[:class:`bool`]
            Whether the message should be sent as an ephemeral message. Defaults to False.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have the proper permissions to send the message.
        BadRequestError
            Some of specified parameters is invalid.
        """

        # ToDo: Add delete_after parameter
        # ToDo: Add components parameter
        # ToDo: Add files parameter

        if embeds is None:
            embeds = [embed] if embed is not None else []

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
        elif self._client.allowed_mentions is not None:
            payload["allowed_mentions"] = self._client.allowed_mentions.to_dict()

        if ephemeral:
            payload["flags"] = MessageFlags.EPHEMERAL.value

        return await self.respond(
            InteractionResponse.from_dict(
                {
                    "type": InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                    "data": payload,
                }
            )
        )

    async def fetch_original_message(self) -> Message:
        """Fetch Original Interaction Response"""
        return await self._client.rest.get_original_interaction_response(
            self.application_id, self.token
        )

    async def delete_original_message(self):
        """Delete Original Interaction Response"""
        await self._client.rest.delete_original_interaction_response(
            self.application_id, self.token
        )


@dataclass(repr=False)
class ResolvedData(APIModelBase):
    """Resolved Data

    Attributes
    ----------
    attachments: Dict[:class:`~melisa.utils.types.snowflake.Snowflake`, :class:`Any`]
        The attachments of the interaction
    channels: Dict[:class:`~melisa.utils.types.snowflake.Snowflake`, :class:`~melisa.models.guild.channel.Channel`]
        The channels of the interaction
    members: Dict[:class:`~melisa.utils.types.snowflake.Snowflake`, :class:`~melisa.models.guild.member.GuildMember`]
        The members of the interaction
    messages: Dict[:class:`~melisa.utils.types.snowflake.Snowflake`, :class:`~melisa.models.message.message.Message`]
        The members of the interaction
    roles: Dict[:class:`~melisa.utils.types.snowflake.Snowflake`, :class:`~melisa.models.guild.role.Role`]
        The roles of the interaction
    users: Dict[:class:`~melisa.utils.types.snowflake.Snowflake`, :class:`~melisa.models.user.user.User`]
        The users of the interaction
    """

    attachments: Dict[Snowflake, Any] = None
    channels: Dict[Snowflake, Channel] = None
    members: Dict[Snowflake, GuildMember] = None
    messages: Dict[Snowflake, Message] = None
    roles: Dict[Snowflake, Role] = None
    users: Dict[Snowflake, User] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a ResolvedData from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a ResolvedData.
        """
        self: ResolvedData = super().__new__(cls)

        self.attachments = data.get("attachments", {})

        self.channels = {}
        self.members = {}
        self.messages = {}
        self.roles = {}
        self.users = {}

        for _id, value in data.get("channels", {}).items():
            self.channels[Snowflake(_id)] = _choose_channel_type(value)

        for _id, value in data.get("members", {}).items():
            self.members[Snowflake(_id)] = GuildMember.from_dict(value)

        for _id, value in data.get("messages", {}).items():
            self.messages[Snowflake(_id)] = Message.from_dict(value)

        for _id, value in data.get("members", {}).items():
            self.members[Snowflake(_id)] = GuildMember.from_dict(value)

        for _id, value in data.get("roles", {}).items():
            self.roles[Snowflake(_id)] = Role.from_dict(value)

        for _id, value in data.get("users", {}).items():
            self.users[Snowflake(_id)] = User.from_dict(value)

        return self


@dataclass(repr=False)
class ApplicationCommandData(APIModelBase):
    """Application Command Data

    Attributes
    ----------
    id:	:class:`~melisa.utils.types.snowflake.Snowflake`
        The ID of the invoked command
    name: str
        The name of the invoked command
    type: :class:`~melisa.models.interactions.commands.ApplicationCommandType`
        Type of the application command
    resolved: Optional[:class:`~melisa.models.interactions.interactions.ResolvedData`]
        Data resolved from the interaction
    options: Optional[List[:class:`~melisa.models.interactions.commands.SlashCommandInteractionDataOption`]]
        List of application command interaction data option	the params + values from the user
    guild_id: Optional[:class:`~melisa.utils.types.snowflake.Snowflake`]
        The id of the guild the command is registered to
    target_id: Optional[:class:`~melisa.utils.types.snowflake.Snowflake`]
        Id of the user or message targeted by a user or message command
    """

    id: Snowflake = None
    name: str = None
    type: ApplicationCommandType = None
    resolved: Optional[ResolvedData] = None
    options: Optional[List[SlashCommandInteractionDataOption]] = None
    guild_id: Optional[Snowflake] = None
    target_id: Optional[Snowflake] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a ApplicationCommandData from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a ApplicationCommandData.
        """
        self: ApplicationCommandData = super().__new__(cls)

        self.id = Snowflake(data.get("id", 0))
        self.name = data.get("name")
        self.type = try_enum(ApplicationCommandType, data.get("type"))
        self.resolved = ResolvedData.from_dict(data.get("resolved", {}))
        self.options = [
            SlashCommandInteractionDataOption.from_dict(option)
            for option in data.get("options", [])
        ]
        self.guild_id = Snowflake(data.get("guild_id", 0))
        self.target_id = Snowflake(data.get("target_id", 0))

        return self
