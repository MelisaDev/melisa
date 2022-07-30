# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import IntEnum
from typing import Optional, Dict, Union, Any, List

from .i18n import LocalizedField
from ..guild.channel import ChannelType
from ...utils.snowflake import Snowflake
from ...utils.conversion import try_enum
from ...utils.api_model import APIModelBase


class ApplicationCommandType(IntEnum):
    """Application Command Type

    Attributes
    ----------
    CHAT_INPUT:
        Slash commands; a text-based command that shows up when a user types /
    USER:
        A UI-based command that shows up when you right click or tap on a user
    MESSAGE:
        A UI-based command that shows up when you right click or tap on a message
    """

    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3

    def __int__(self):
        return self.value


class SlashCommandOptionType(IntEnum):
    """Application Command Option Type

    Attributes
    ----------
    SUB_COMMAND:
        Sub command
    SUB_COMMAND_GROUP:
        Sub command group
    STRING:
        :class:`str`
    INTEGER:
        :class:`int` between -2^53 and 2^53
    BOOLEAN:
        :class:`bool`
    USER:
        user
    CHANNEL:
        includes all channel types + categories
    ROLE:
        role
    MENTIONABLE:
        Includes users and roles
    NUMBER:
        Any :class:`float` between -2^53 and 2^53
    ATTACHMENT:
        Attachment object
    """

    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11

    def __int__(self):
        return self.value


class PartialApplicationCommand(APIModelBase):
    """Represents Partial Application Command

    Attributes
    ----------
    id: :class:`~melisa.utils.snowflake.Snowflake`
        Unique ID of command
    type: Optional[:class:`~melisa.interactions.commands.SlashCommandType`]
        Type of command, defaults to ``1``
    application_id: :class:`~melisa.utils.snowflake.Snowflake`
        ID of the parent application
    guild_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`]
        guild id of the command, if not global
    name: :class:`~melisa.models.interactions.i18n.LocalizedField`
        Name of the command
    default_member_permissions: str
        Set of permissions represented as a bit set
    dm_permission: bool
        Indicates whether the command is available
        in DMs with the app, only for globally-scoped commands.
        By default, commands are visible.
    version: :class:`~melisa.utils.snowflake.Snowflake`
        Autoincrementing version identifier updated during substantial record changes
    """

    # ToDo: Better Permissions

    id: Snowflake = None
    type: Optional[ApplicationCommandType] = 1
    application_id: Snowflake = None
    guild_id: Optional[Snowflake] = None
    name: LocalizedField = None
    default_member_permissions: str = None
    dm_permission: bool = True
    version: Snowflake = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a ApplicationCommand from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a PartialApplicationCommand.
        """
        self: PartialApplicationCommand = super().__new__(cls)

        self.id = Snowflake(data.get("id", 0))
        self.type = try_enum(ApplicationCommandType, data.get("type", 1))
        self.application_id = Snowflake(data.get("application_id"))
        self.guild_id = (
            Snowflake(data["guild_id"]) if data.get("guild_id") is not None else None
        )

        name = data.get("name")
        name_localizations = data.get("name_localizations")

        self.name = LocalizedField(name, name_localizations)

        self.default_member_permissions = data.get("default_member_permissions", "")
        self.dm_permission = data.get("dm_permission", True)
        self.version = Snowflake(data.get("version", 0))

        return self


class SlashCommand(PartialApplicationCommand):
    """Represents SlashCommand

    Attributes
    ----------
    description: :class:`~melisa.models.interactions.i18n.LocalizedField`
        Description of command
    """

    description: LocalizedField = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a SlashCommand from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a SlashCommand.
        """
        self: SlashCommand = super().__new__(cls)

        self.id = Snowflake(data.get("id", 0))
        self.type = try_enum(ApplicationCommandType, data.get("type", 1))
        self.application_id = Snowflake(data.get("application_id"))
        self.guild_id = (
            Snowflake(data["guild_id"]) if data.get("guild_id") is not None else None
        )
        self.name = data.get("name")
        self.name_localizations = data.get("name_localizations")

        description = data.get("description")
        description_localizations = data.get("description_localizations")

        self.description = LocalizedField(description, description_localizations)

        self.options = [
            SlashCommandOption.from_dict(x) for x in data.get("options", [])
        ]
        self.default_member_permissions = data.get("default_member_permissions", "")
        self.dm_permission = data.get("dm_permission", True)
        self.version = Snowflake(data.get("version", 0))

        return self


class SlashCommandOption(APIModelBase):
    """Application Command Option

    .. warning::

        Required ``options`` must be listed before optional options.

    Attributes
    ----------
    type: :class:`~melisa.models.interactions.commands.SlashCommandOptionType`
        Type of option
    name: str
        1-32 character name
    name_localizations: Dict[str, str]
        Localization dictionary for the ``name`` field.
        Values follow the same restrictions as ``name``
    description: str
        1-100 character description
    description_localizations: Dict[str, str]
        Localization dictionary for the ``description`` field.
        Values follow the same restrictions as ``description``
    required: Optional[bool]
        If the parameter is required or optional--default false
    choices: Optional[List[:class:`~melisa.models.interactions.commands.SlashCommandOptionChoice`]]
        Choices for ``STRING``, ``INTEGER``, and ``NUMBER``
         types for the user to pick from, max 25
    options: Optional[List[SlashCommandOption]]
        If the option is a subcommand or subcommand group type,
        these nested options will be the parameters
    channel_types: Optional[List[:class:`~melisa.models.guild.channel.ChannelType`]]
        If the option is a channel type,
        the channels shown will be restricted to these types
    min_value: Optional[int, float]
        If the option is an ``int`` or ``float`` type,
        the minimum value permitted
    max_value: Optional[int, float]
        If the option is an ``int`` or ``float`` type,
        the maximum value permitted
    autocomplete: Optional[bool]
        If autocomplete interactions are enabled for this ``str``,
        ``int``, or ``float`` type option
    """

    type: SlashCommandOptionType = None
    name: str = None
    name_localizations: Dict[str, str] = None
    description: str
    description_localizations: Dict[str, str] = None
    required: Optional[bool] = False
    choices: Optional[List[SlashCommandOptionChoice]] = None
    options: Optional[List[SlashCommandOption]] = None
    channel_types: Optional[List[ChannelType]] = None
    min_value: Optional[int, float] = None
    max_value: Optional[int, float] = None
    autocomplete: Optional[bool] = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a SlashCommandOption from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a SlashCommandOption.
        """
        self: SlashCommandOption = super().__new__(cls)

        self.type = try_enum(SlashCommandOptionType, data.get("type", 0))
        self.name = data.get("name")
        self.name_localizations = data.get("name_localizations")
        self.description = data.get("description")
        self.description_localizations = data.get("description_localizations")
        self.required = data.get("required", False)
        self.choices = [
            try_enum(SlashCommandOptionChoice, x) for x in data.get("choices", [])
        ]
        self.options = [
            SlashCommandOption.from_dict(x) for x in data.get("options", [])
        ]
        self.channel_types = [
            try_enum(ChannelType, x) for x in data.get("channel_types", [])
        ]
        self.min_value = data.get("min_value")
        self.max_value = data.get("max_value")
        self.autocomplete = data.get("autocomplete")

        return self


class SlashCommandOptionChoice(APIModelBase):
    """Application Command Option Choice

    If you specify ``choices`` for an option,
    they are the only valid values for a user to pick

    Attributes
    ----------
    name: :class:`str`
        1-100 character choice name
    name_localizations: Optional[Dict[:class:`str`, :class:`str`]]
        Dictionary with keys in
        `available locales <https://discord.com/developers/docs/reference#locales>`_

        Localization dictionary for the name field.
        Values follow the same restrictions as name

    value: Union[:class:`str`, :class:`int`, :class:`float`]
        Value for the choice, up to 100 characters if string
    """

    name: str = None
    name_localizations: Optional[Dict[str, str]] = None
    value: Union[str, int, float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a SlashCommandOptionChoice from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a SlashCommandOptionChoice.
        """
        self: SlashCommandOptionChoice = super().__new__(cls)

        self.name = data.get("name")
        self.name_localizations = data.get("name_localizations")
        self.value = data.get("value")

        return self


class SlashCommandInteractionDataOption(APIModelBase):
    """Slash Command Interaction Data Option

    All options have names, and an option can either be a parameter
    and input value--in which case ``value`` will be set--or it
    can denote a subcommand or group--in which case it will contain
    a top-level key and another array of ``options``.

    ``value`` and ``options`` are mutually exclusive.

    Attributes
    ----------
    name: :class:`str`
        Name of the parameter
    type: :class:`~melisa.models.interactions.commands.SlashCommandOptionType`
        Value of :class:`~melisa.models.interactions.commands.SlashCommandOptionType`
    value: Optional[Union[str, int, float]]
        Value of the option resulting from user input
    options: Optional[List[SlashCommandInteractionDataOption]]
        Present if this option is a group or subcommand
    focused: Optional[bool]
        ``true`` if this option is the currently focused option for autocomplete
    """

    name: str = None
    type: SlashCommandOptionType = None
    value: Optional[Union[str, int, float]] = None
    options: Optional[List[SlashCommandInteractionDataOption]] = None
    focused: bool = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a SlashCommandInteractionDataOption from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a SlashCommandInteractionDataOption.
        """
        self: SlashCommandInteractionDataOption = super().__new__(cls)

        self.name = data.get("name")
        self.type = try_enum(SlashCommandOptionType, data.get("type", 0))
        self.value = data.get("value")
        self.options = [
            SlashCommandInteractionDataOption.from_dict(x)
            for x in data.get("options", [])
        ]
        self.focused = data.get("focused", False)

        return self


# noinspection PyTypeChecker
command_types_for_converting: Dict[ApplicationCommandType, PartialApplicationCommand] = {
    ApplicationCommandType.CHAT_INPUT: SlashCommand
}


def _choose_command_type(data):
    data.update({"type": ApplicationCommandType(data.pop("type"))})

    command_cls = command_types_for_converting.get(data["type"], PartialApplicationCommand)
    return command_cls.from_dict(data)
