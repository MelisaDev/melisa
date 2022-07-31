# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from typing import Dict, Any, Optional, List
from enum import IntEnum

from dataclasses import dataclass

from .commands import ApplicationCommandType
from .commands import SlashCommandInteractionDataOption
from ...utils.conversion import try_enum
from ...models.guild import Channel, Role, _choose_channel_type, GuildMember
from ...utils.api_model import APIModelBase
from ...models.message.message import Message
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