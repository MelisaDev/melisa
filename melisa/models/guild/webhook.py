# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Optional, Dict

from ...utils import Snowflake
from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED

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
        Channel Follower Webhooks are internal webhooks used with Channel Following
        to post new messages into channels
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
        The guild of the channel that this webhook is following
        (returned for Channel Follower Webhooks)
    source_channel: :class:`~melisa.models.guild.channel.Channel`
        The channel that this webhook is following (returned for Channel Follower Webhooks)
    url: :class:`str`
        The url used for executing the webhook (returned by the webhooks OAuth2 flow)
    """

    id: APINullable[Snowflake] = UNDEFINED
    type: APINullable[int] = UNDEFINED
    guild_id: APINullable[Snowflake] = UNDEFINED
    channel_id: APINullable[Snowflake] = UNDEFINED
    user: APINullable[User] = UNDEFINED
    name: APINullable[str] = UNDEFINED
    avatar: APINullable[str] = UNDEFINED
    token: APINullable[str] = UNDEFINED
    application_id: APINullable[Snowflake] = UNDEFINED
    source_guild: APINullable[Guild] = UNDEFINED
    source_channel: APINullable[Channel] = UNDEFINED
    url: APINullable[str] = UNDEFINED

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> Webhook:
        """Generate a webhook from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into a webhook.
        """

        self: Webhook = super().__new__(cls)

        self.id = int(data["id"])
        self.type = data.get("type")
        self.guild_id = data.get("guild_id")
        self.channel_id = data.get("channel_id")
        self.user = data.get("user", {})
        self.avatar = data.get("avatar")
        self.token = data.get("token")
        self.application_id = data.get("application_id")

        if data.get("source_guild") is not None:
            self.source_guild = data.get("source_guild", {})
        else:
            self.source_guild = None
        
        if data.get("source_channel") is not None:
            self.source_channel = data.get("source_channel", {})
        else:
            self.source_channel = None
        
        self.url = data.get("url")

        return self

    async def delete(self, *, reason: Optional[str] = None):
        """|coro|
        Delete a webhook permanently. Requires the ``MANAGE_WEBHOOKS`` permission.
        Returns a ``204 No Content`` response on success.

        Parameters
        ----------
        reason: Optional[:class:`str`]
            The reason for delete the webhook. Shows up on the audit log.
        """
        await self._http.delete(
            f"/webhooks/{self.id}",
            headers={"X-Audit-Log-Reason": reason},
        )

    async def modify(
        self,
        *,
        name: Optional[str] = None,
        channel_id: Optional[Snowflake] = None,
        reason: Optional[str] = None,
    ):
        """|coro|
        Modify a webhook. Requires the ``MANAGE_WEBHOOKS permission``.
        Returns the updated webhook object on success.

        Parameters
        ----------
        name: Optional[:class:`str`]
            The default name of the webhook
        channel_id: Optional[:class:`~.melisa.utils.snowflake.Snowflake`]
            The new channel id this webhook should be moved to
        reason: Optional[:class:`str`]
            The reason for modify the webhook. Shows up on the audit log.
        """

        await self._http.patch(
            f"/webhooks/{self.id}",
            headers={
                "name": name,
                "channel_id": channel_id,
                "X-Audit-Log-Reason": reason,
            },
        )
