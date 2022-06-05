# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import IntEnum
from typing import Optional, Dict, Union, Any

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
        `avaliable locales <https://discord.com/developers/docs/reference#locales>`_

        Localization dictionary for the name field.
        Values follow the same restrictions as name

    value: Union[:class:`str`, :class:`int`, :class:`float`]
        Value for the choice, up to 100 characters if string
    """

    name: str
    name_localizations: Optional[Dict[str, str]]
    value: Union[str, int, float]

    @staticmethod
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




