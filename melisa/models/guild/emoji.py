# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict

from ...utils import Snowflake
from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED

if TYPE_CHECKING:
    from ..user.user import User
    from .role import Role


@dataclass(repr=False)
class Emoji(APIModelBase):
    """Emoji Structure
    
    Attributes
    ----------
    id: :class:`~melisa.utils.types.Snowflake`
        Emoji id
    name: :class:`str`
        Emoji name
    roles: :class:`Any`
        Roles allowed to use this emoji
    user: :class:`Any`
        User that created this emoji
    require_colons: :class:`bool`
        Whether this emoji must be wrapped in colons
    managed: :class:`bool`
        Whether this emoji is managed
    animated: :class:`bool`
        Whether this emoji is animated
    available: :class:`bool`
        Whether this emoji can be used, may be false due to loss of Server Boosts
    """

    id: APINullable[Snowflake] = UNDEFINED
    name: APINullable[str] = UNDEFINED
    roles: APINullable[Role] = UNDEFINED
    user: APINullable[User] = UNDEFINED
    require_colons: APINullable[bool] = UNDEFINED
    managed: APINullable[bool] = UNDEFINED
    animated: APINullable[bool] = UNDEFINED
    available: APINullable[bool] = UNDEFINED

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Emoji:
        """Generate an emoji from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into an emoji.
        """

        self: Emoji = super().__new__(cls)

        self.id = int(data["id"])
        self.name = data.get("name")
        self.roles = data.get("roles")
        self.user = data.get("user", {})
        self.require_colons = data.get("require_colons", False)
        self.managed = data.get("managed", False)
        self.animated = data.get("animated", False)
        self.available = data.get("available", False)

        return self
