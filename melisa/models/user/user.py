# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional

from ...utils.api_model import APIModelBase
from ...utils.types import APINullable
from ...utils.snowflake import Snowflake


class PremiumTypes(IntEnum):
    """Premium types denote the level of premium a user has.

    Attributes
    ----------
    NITRO:
        Full nitro
    NITRO_CLASSIC:
        Nitro (not boost)
    NONE:
        There is no subscription Discord Nitro(Full or classic)
    """

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2

    def __int__(self):
        return self.value


class UserFlags(IntEnum):
    """Profile Icons

    Attributes
    ----------
    NONE:
        None
    STAFF:
        Discord Employee
    PARTNER:
        Partnered Server Owner
    HYPESQUAD:
        HypeSquad Events Coordinator
    BUG_HUNTER_LEVEL_1:
        Bug Hunter Level 1
    HYPESQUAD_ONLINE_HOUSE_1:
        House Bravery Member
    HYPESQUAD_ONLINE_HOUSE_2:
        House Brilliance Member
    HYPESQUAD_ONLINE_HOUSE_3:
        House Balance Member
    PREMIUM_EARLY_SUPPORTER:
        Early Nitro Supporter
    TEAM_PSEUDO_USER:
        User is a team
    BUG_HUNTER_LEVEL_2:
        Bug Hunter Level 2
    VERIFIED_BOT:
        Verified Bot
    VERIFIED_DEVELOPER:
        Early Verified Bot Developer
    CERTIFIED_MODERATOR:
        Discord Certified Moderator
    BOT_HTTP_INTERACTIONS:
        Bot uses only HTTP interactions and is shown in the online member list
    """

    NONE = 0
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19

    def __int__(self):
        return self.value


class VisibilityTypes(IntEnum):
    """The type of connection visibility.

    Attributes
    ----------
    None:
        invisible to everyone except the user themselves
    Everyone:
        visible to everyone
    """

    NONE = 0
    EVERYONE = 1

    def __int__(self):
        return self.value


@dataclass(repr=False)
class User(APIModelBase):
    # ToDo: Update Docstrings
    """User Structure

    Attributes
    ----------
    id: :class:`~melisa.utils.types.Snowflake`
        the user's id
    username: :class:`str`
        the user's username, not unique across the platform
    discriminator: :class:`int`
        the user's 4-digit discord-tag
    avatar: Optional[:class:`str`]
        the user's avatar hash
    bot: APINullable[:class:`bool`]
        whether the user belongs to an OAuth2 application
    system: APINullable[:class:`bool`]
        whether the user is an Official Discord System user (part of the urgent message system)
    mfa_enabled: APINullable[:class:`bool`]
        whether the user has two factor enabled on their account
    banner: APINullable[:class:`str`]
        the user's banner hash
    accent_color: APINullable[:class:`int`]
        the user's banner color encoded as an integer representation of hexadecimal color code
    locale: APINullable[:class:`str`]
        the user's chosen language option
    verified: APINullable[:class:`bool`]
        whether the email on this account has been verified
    email: APINullable[:class:`str`]
        the user's email
    flags: APINullable[:class:`~models.user.user.UserFlags`]
        the flags on a user's account
    premium_type: APINullable[:class:`int`]
        the type of Nitro subscription on a user's account
    public_flags: APINullable[:class:`int`]
        the public flags on a user's account
    premium: APINullable[:class:`PremiumTypes`]
        The user their premium type in a usable enum.
    """

    id: APINullable[Snowflake] = None
    username: APINullable[str] = None
    discriminator: APINullable[str] = None
    avatar: APINullable[str] = None
    bot: APINullable[bool] = None
    system: APINullable[bool] = None
    mfa_enabled: APINullable[bool] = None
    banner: APINullable[str] = None
    accent_color: APINullable[int] = None
    local: APINullable[str] = None
    verified: APINullable[bool] = None
    email: APINullable[str] = None
    premium_type: APINullable[int] = None
    public_flags: APINullable[int] = None

    @property
    def premium(self) -> Optional[PremiumTypes]:
        """APINullable[:class:`~melisa.models.user.user.PremiumTypes`]: The
        user their premium type in a usable enum.
        """
        return (
            None
            if self.premium_type is None
            else PremiumTypes(self.premium_type)
        )

    @property
    def flags(self) -> Optional[UserFlags]:
        """Flags of user"""
        return(
            None
            if self.flags is None
            else UserFlags(self.flags)
        )

    def __str__(self):
        """String representation of the User object"""
        return self.username + "#" + self.discriminator

    @property
    def mention(self):
        """:class:`str`: The user's mention string. (<@id>)"""
        return "<@{}>".format(self.id)

    def avatar_url(self) -> str:
        """Avatar url (from the Discord CDN server)"""
        return "https://cdn.discordapp.com/avatars/{}/{}.png?size=1024".format(self.id, self.avatar)

    async def create_dm_channel(self):
        # ToDo: Add docstrings
        # ToDo: Add checking this channel in cache
        return await self._http.post(
            "/users/@me/channels", data={"recipient_id": self.id})
