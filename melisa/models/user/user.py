from __future__ import annotations

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional

from ...utils.api_object import APIObjectBase
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

    id: Optional[Snowflake] = None
    username: Optional[str] = None
    discriminator: Optional[str] = None
    avatar: Optional[str] = None
    bot: Optional[bool] = None
    system: Optional[bool] = None
    mfa_enabled: Optional[bool] = None
    banner: Optional[str] = None
    accent_color: Optional[int] = None
    local: Optional[str] = None
    verified: Optional[bool] = None
    email: Optional[str] = None
    flags: Optional[int] = None
    premium_type: Optional[int] = None
    public_flags: Optional[int] = None


    @property
    def premium(self) -> Optional[PremiumTypes]:
        return (
            None
            if self.premium_type is None
            else PremiumTypes(self.premium_type)
        )

    @property
    def flags(self) -> Optional[UserFlags]:
        return(
            None
            if self.flags is None
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