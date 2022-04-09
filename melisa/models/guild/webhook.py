# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from ...utils import Snowflake
from ...utils import APIModelBase
from ...utils.types import APINullable

if TYPE_CHECKING:
    from ..user.user import User
    from .guild import Guild
    from .channel import Channel


class WebhookType(IntEnum):
    """Webhook Type

    Attributes
    ----------
    Incoming:
        Incoming Webhooks can post messages to channels with a generated token
    Channel_Follower:
        Channel Follower Webhooks are internal webhooks used with Channel Following to post new messages into channels
    Application:
        Application webhooks are webhooks used with Interactions
    """

    Incoming = 1
    Channel_Follower = 2
    Application = 3

    def __int__(self):
        return self.value


@dataclass(repr=False)
class Webhook(APIModelBase):
    """Webhooks are a low-effort way to post messages to channels in Discord.
    They do not require a bot user or authentication to use.

    Attributes
    ----------
    id: :class:`~melisa.utils.types.snowflake.Snowflake`
        The id of the webhook
    type: :class:`int`
        The type of the webhook
    guild_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        The guild id this webhook is for, if any
    channel_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        The channel id this webhook is for, if any
    user: :class:`~melisa.models.user.user.User`
        The user this webhook was created by (not returned when getting a webhook with its token)
    name: :class:`str`
        The default name of the webhook
    avatar: :class:`str`
        The default user avatar hash of the webhook
    token: :class:`str`
        The secure token of the webhook (returned for Incoming Webhooks)
    application_id: :class:`~melisa.utils.types.snowflake.Snowflake`
        The bot/OAuth2 application that created this webhook
    source_guild: :class:`~melisa.models.guild.guild.Guild`
        The guild of the channel that this webhook is following (returned for Channel Follower Webhooks)
    source_channel: :class:`~melisa.models.guild.channel.Channel`
        The channel that this webhook is following (returned for Channel Follower Webhooks)
    url: :class:`str`
        The url used for executing the webhook (returned by the webhooks OAuth2 flow)
    """

    id: APINullable[Snowflake] = None
    type: APINullable[int] = None
    guild_id: APINullable[Snowflake] = None
    channel_id: APINullable[Snowflake] = None
    user: APINullable[User] = None
    name: APINullable[str] = None
    avatar: APINullable[str] = None
    token: APINullable[str] = None
    application_id: APINullable[Snowflake] = None
    source_guild: APINullable[Guild] = None
    source_channel: APINullable[Channel] = None
    url: APINullable[str] = None
