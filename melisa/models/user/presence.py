# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from dataclasses import dataclass
from enum import IntEnum, Enum, Flag
from typing import Optional, Tuple, List, Literal

from ...utils import Snowflake
from ...utils import APIModelBase
from ...utils.types import APINullable, UNDEFINED


class BasePresence:
    """
    All the information about activities here is from the Discord API docs.
    Read more here: https://discord.com/developers/docs/topics/gateway#activity-object

    Unknown data will be returned as None.
    """


class ActivityType(IntEnum):
    """Represents the enum of the type of activity.

    Attributes
    ----------
    GAME:
        Playing {name} (Playing Rocket League)
    STREAMING:
        Streaming {details} (Streaming Rocket League)
        It supports only YouTube and Twitch
    LISTENING:
        Listening to {name} (Listening to Spotify)
    WATCHING:
        Watching {name} (Watching YouTube Together)
    CUSTOM:
        {emoji} {name} (":smiley: I am cool")
        (THIS ACTIVITY IS NOT SUPPORTED FOR BOTS)
    COMPETING:
        Competing in {name} (Competing in Arena World Champions)
    """

    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5

    def __int__(self):
        return self.value


@dataclass(repr=False)
class ActivityTimestamp(BasePresence, APIModelBase):
    """Represents the timestamp of an activity.

    Attributes
    ----------
    start: Optional[:class:`int`]
        Unix time (in milliseconds) of when the activity started
    end: Optional[:class:`int`]
        Unix time (in milliseconds) of when the activity ends
    """

    start: APINullable[int] = None
    end: APINullable[int] = None


@dataclass(repr=False)
class ActivityEmoji(BasePresence, APIModelBase):
    """Represents an emoji in an activity.

    Attributes
    ----------
    name: :class:`str`
        The name of the emoji
    id: Optional[:class:`Snowflake`]
        The id of the emoji
    animated: Optional[:class:`bool`]
        Whether this emoji is animated
    """

    name: str
    id: APINullable[Snowflake] = None
    animated: APINullable[bool] = None


@dataclass(repr=False)
class ActivityParty(BasePresence, APIModelBase):
    """Represents a party in an activity.

    Attributes
    ----------
    id: Optional[:class:`str`]
        The id of the party
    size: Optional[Tuple[:class:`int`, :class:`int`]]
        Array of two integers (current_size, max_size)
    """

    id: APINullable[str] = None
    size: APINullable[Tuple[int, int]] = None


@dataclass(repr=False)
class ActivityAssets(BasePresence, APIModelBase):
    """Represents an asset of an activity.

    Attributes
    ----------
    large_image: Optional[:class:`str`]
        (Large Image) Activity asset images are arbitrary strings
        which usually contain snowflake IDs
    large_text: Optional[:class:`str`]
        text displayed when hovering over the large image of the activity
    small_image: Optional[:class:`str`]
        (Small Image) Activity asset images are arbitrary strings
         which usually contain snowflake IDs
    small_text: Optional[:class:`str`]
        text displayed when hovering over the small image of the activity
    """

    large_image: APINullable[str] = None
    large_text: APINullable[str] = None
    small_image: APINullable[str] = None
    small_text: APINullable[str] = None


@dataclass(repr=False)
class ActivitySecrets(BasePresence, APIModelBase):
    """Represents a secret of an activity.

    Attributes
    ----------
    join: Optional[:class:`str`]
        The secret for joining a party
    spectate: Optional[:class:`str`]
        The secret for spectating a game
    match: Optional[:class:`str`]
        The secret for a specific instanced match
    """

    join: APINullable[str] = None
    spectate: APINullable[str] = None
    match_: APINullable[str] = None


class ActivityFlags(BasePresence, APIModelBase):
    """
    Just Activity Flags (From Discord API).

    Everything returns :class:`bool` value.
    """

    def __init__(self, flags) -> None:
        self.INSTANCE = bool(flags >> 0 & 1)
        self.JOIN = bool(flags >> 1 & 1)
        self.SPECTATE = bool(flags >> 2 & 1)
        self.JOIN_REQUEST = bool(flags >> 3 & 1)
        self.SYNC = bool(flags >> 4 & 1)
        self.PLAY = bool(flags >> 5 & 1)
        self.PARTY_PRIVACY_FRIENDS = bool(flags >> 6 & 1)
        self.PARTY_PRIVACY_VOICE_CHANNEL = bool(flags >> 7 & 1)
        self.EMBEDDED = bool(flags >> 8 & 1)


@dataclass(repr=False)
class ActivityButton(BasePresence, APIModelBase):
    """When received over the gateway, the buttons field is an array of strings,
     which are the button labels. Bots
    cannot access a user's activity button URLs.
    When sending, the buttons field must be an array of the below
    object:
    Attributes
    ----------
    label: :class:`str`
        The text shown on the button (1-32 characters)
    url: :class:`str`
        The url opened when clicking the button (1-512 characters)
    """

    label: str
    url: str


@dataclass(repr=False)
class Activity(BasePresence, APIModelBase):
    """Bots are only able to send ``name``, ``type``, and optionally ``url``.

    Attributes
    ----------
    name: :class:`str`
        The activity's name
    type: :class:`~melisa.models.user.activity.ActivityType`
        Activity type
    url: Optional[:class:`str`]
        Stream url, is validated when type is 1
    created_at:  Optional[:class:`int`]
        Unix timestamp (in milliseconds) of when the activity was added to the user's session
    timestamps: Optional[:class:`~melisa.models.user.activity.ActivityTimestamp`]
        Unix timestamps for start and/or end of the game
    application_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`]
        Application id for the game
    details: Optional[:class:`str`]
        What the player is currently doing
    state: Optional[:class:`str`]
        The user's current party status
    emoji: Optional[:class:`~melisa.models.user.activity.ActivityEmoji`]
        The emoji used for a custom status
    party: Optional[:class:`~melisa.models.user.activity.ActivityParty`]
        Information for the current party of the player
    assets: Optional[:class:`~melisa.models.user.activity.ActivityAssets`]
        Images for the presence and their hover texts
    secrets: Optional[:class:`~melisa.models.user.activity.ActivitySecrets`]
        Secrets for Rich Presence joining and spectating
    instance: Optional[:class:`bool`]
        Whether or not the activity is an instanced game session
    flags: Optional[:class:`~melisa.models.user.activity.ActivityFlags`]
        Activity flags ORd together, describes what the payload includes
    buttons: Optional[List[:class:`~melisa.models.user.activity.ActivityButton`]]
        The url button on an activity.
    """

    name: str
    type: ActivityType
    created_at: APINullable[int] = UNDEFINED
    url: APINullable[str] = UNDEFINED
    timestamps: APINullable[ActivityTimestamp] = UNDEFINED
    application_id: APINullable[Snowflake] = UNDEFINED
    details: APINullable[str] = UNDEFINED
    state: APINullable[str] = UNDEFINED
    emoji: APINullable[ActivityEmoji] = UNDEFINED
    party: APINullable[ActivityParty] = UNDEFINED
    assets: APINullable[ActivityAssets] = UNDEFINED
    secrets: APINullable[ActivitySecrets] = UNDEFINED
    instance: APINullable[bool] = UNDEFINED
    flags: APINullable[ActivityFlags] = UNDEFINED
    buttons: APINullable[List[ActivityButton]] = UNDEFINED


class StatusType(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    IDLE = "idle"
    DND = "dnd"
    INVISIBLE = "invisible"

    def __str__(self):
        return self.value
