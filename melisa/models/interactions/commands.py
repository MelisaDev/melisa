# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import IntEnum
from typing import Optional, Dict, Union, Any, List

from ...utils.conversion import try_enum
from ...utils.api_model import APIModelBase


class ApplicationCommandTypes(IntEnum):
    """Application Command Types

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


class ApplicationCommandOptionTypes(IntEnum):
    """Application Command Option Types

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


class ApplicationCommandOptionChoice(APIModelBase):
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
        """Generate a ApplicationCommandOptionChoice from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a ApplicationCommandOptionChoice.
        """
        self: ApplicationCommandOptionChoice = super().__new__(cls)

        self.name = data.get("name")
        self.name_localizations = data.get("name_localizations")
        self.value = data.get("value")

        return self


class ApplicationCommandInteractionDataOption(APIModelBase):
    """Application Command Interaction Data Option

    All options have names, and an option can either be a parameter
    and input value--in which case ``value`` will be set--or it
    can denote a subcommand or group--in which case it will contain
    a top-level key and another array of ``options``.

    ``value`` and ``options`` are mutually exclusive.

    Attributes
    ----------
    name: :class:`str`
        Name of the parameter
    type: :class:`~melisa.models.interactions.commands.ApplicationCommandOptionTypes`
        Value of :class:`~melisa.models.interactions.commands.ApplicationCommandOptionTypes`
    value: Optional[Union[str, int, float]]
        Value of the option resulting from user input
    options: Optional[List[ApplicationCommandInteractionDataOption]]
        Present if this option is a group or subcommand
    focused: Optional[bool]
        ``true`` if this option is the currently focused option for autocomplete
    """

    name: str = None
    type: ApplicationCommandOptionTypes = None
    value: Optional[Union[str, int, float]] = None
    options: Optional[List[ApplicationCommandInteractionDataOption]] = None
    focused: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a ApplicationCommandInteractionDataOption from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a ApplicationCommandInteractionDataOption.
        """
        self: ApplicationCommandInteractionDataOption = super().__new__(cls)

        self.name = data.get("name")
        self.type = try_enum(ApplicationCommandOptionTypes, data.get("type", 0))
        self.value = data.get("value")
        self.options = [
            ApplicationCommandInteractionDataOption.from_dict(x)
            for x in data.get("options", [])
        ]
        self.focused = data.get("focused")

        return self
