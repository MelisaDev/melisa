# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict

from ...utils import Snowflake
from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED


@dataclass(repr=False)
class Role(APIModelBase):
    """Roles represent a set of permissions attached to a group of users.

    Attributes
    ----------
    id: :class:`~melisa.utils.types.Snowflake`
        Role id
    name: :class:`str`
        Role name
    color: :class:`int`
        Integer representation of hexadecimal color code
    hoist: :class:`bool`
        If this role is pinned in the user listing
    icon: :class:`str`
        Role icon hash
    unicode_emoji: :class:`str`
        Role unicode emoji
    position: :class:`str`
        Position of this role
    permission: :class:`str`
        Permission bit set
    managed: :class:`bool`
        Whether this role is managed by an integration
    mentionable: :class:`bool`
        Whether this role is mentionable
    """

    id: APINullable[Snowflake] = UNDEFINED
    name: APINullable[str] = UNDEFINED
    color: APINullable[int] = UNDEFINED
    hoist: APINullable[bool] = UNDEFINED
    icon: APINullable[str] = UNDEFINED
    unicode_emoji: APINullable[str] = UNDEFINED
    position: APINullable[int] = UNDEFINED
    permission: APINullable[str] = UNDEFINED
    managed: APINullable[bool] = UNDEFINED
    mentionable: APINullable[bool] = UNDEFINED

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Role:
        """Generate a role from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a role.
        """

        self: Role = super().__new__(cls)

        self.id = int(data["id"])
        self.name = data.get("name")
        self.color = data.get("color")
        self.hoist = data.get("hoist", False)
        self.icon = data.get("icon")
        self.unicode_emoji = data.get("unicode_emoji")
        self.position = data.get("position")
        self.permission = data.get("permission")
        self.managed = data.get("managed", False)
        self.mentionable = data.get("mentionable", False)

        return self
