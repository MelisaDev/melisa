from __future__ import annotations

from enum import IntEnum
from dataclasses import dataclass

from ...utils.api_object import APIObjectBase
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING
from ...utils.types import APINullable


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


@dataclass(repr=False)
class User(APIObjectBase):
    """User Structure
    
    Attributes
    ----------
    id:
        the user's id
    username:
        the user's username, not unique across the platform
    discriminator:
        the user's 4-digit discord-tag
    avatar:
        the user's avatar hash
    bot:
        whether the user belongs to an OAuth2 application
    system:
        whether the user is an Official Discord System user (part of the urgent message system)
    mfa_enabled:
        whether the user has two factor enabled on their account
    banner:
        the user's banner hash
    accent_color:
        the user's banner color encoded as an integer representation of hexadecimal color code
    locale:
        the user's chosen language option
    verified:
        whether the email on this account has been verified
    email:
        the user's email
    flags:
        the flags on a user's account
    premium_type:
        the type of Nitro subscription on a user's account
    public_flags:
        the public flags on a user's account
    """

    id: APINullable[Snowflake] = MISSING
    username: APINullable[str] = MISSING
    discriminator: APINullable[str] = MISSING
    avatar: APINullable[str] = MISSING
    bot: APINullable[bool] = MISSING
    system: APINullable[bool] = MISSING
    mfa_enabled: APINullable[bool] = MISSING
    banner: APINullable[str] = MISSING
    accent_color = APINullable[int] = MISSING
    local = APINullable[str] = MISSING
    verified = APINullable[bool] = MISSING
    email = APINullable[str] = MISSING
    flags = APINullable[int] = MISSING
    premium_type = APINullable[int] = MISSING
    public_flags = APINullable[int] = MISSING


    @property
    def premium(self) -> APINullable[PremiumTypes]:
        return (
            MISSING
            if self.premium_type is MISSING
            else PremiumTypes(self.premium_type)
        )

    @property
    def flags(self) -> APINullable[UserFlags]:
        return(
            MISSING
            if self.flags is MISSING
            else UserFlags(self.flags)
        )

    @property
    def mention(self):
        return "<@!{}>".format(self.id)

    @property
    def get_avatar_url(self):
        return (
            "https://cdn.discordapp.com/avatars/{}/{}.png".format(self.id, self.avatar),
            "?size=1024"
        )