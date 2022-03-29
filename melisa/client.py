# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import logging
import asyncio
import signal
from typing import Dict, List, Union, Any

from .models import User, Guild, Activity
from .models.app import Shard
from .utils import Snowflake, APIModelBase
from .utils.types import Coro
from .core.http import HTTPClient
from .core.gateway import GatewayBotInfo
from .models.guild.channel import Channel, ChannelType, channel_types_for_converting
from .utils.logging import init_logging

_logger = logging.getLogger("melisa")


class Client:
    """
    This is the main instance which is between the programmer and the Discord API.

    This Client represents your bot.

    Parameters
    ----------
    token: :class:`str`
        The token to login (you can found it in the developer portal)
    intents: :class:`~melisa.Intents`
        The Discord Intents values.
    activity: :class:`~models.user.presence.BotActivity`
        The Activity to set (on connecting)
    status: :class:`str`
        The Status to set (on connecting).
        Can be generated using :class:`~models.user.presence.StatusType`
    mobile: :class:`bool`
        Set user device as mobile?
    logs: :class:`Optional[None, str, Dict[str, Any]]`
        The hint for configuring logging.
        This can be `None` to disable logging automatically.
        If you pass a :class:`str` or a :class:`int`, it is interpreted as
        the global logging level to use, and should match one of **DEBUG**,
        **INFO**, **WARNING**, **ERROR** or **CRITICAL**, if :class:`str`.

    Attributes
    ----------
    user: :class:`~models.user.user.User`
        The user object of the client
    http: :class:`~core.http.HTTPClient`
        HTTP client for the http-requests to the Discord API
    shards: :class:`Dict[int, Shard]`
        Bot's shards.
    """

    def __init__(
            self,
            token: str,
            intents,
            *,
            activity: Activity = None,
            status: str = None,
            mobile: bool = False,
            logs: Union[None, int, str, Dict[str, Any]] = "INFO",
    ):
        self.shards: Dict[int, Shard] = {}
        self.http: HTTPClient = HTTPClient(token)
        self._events: Dict[str, Coro] = {}

        # ToDo: Transfer guilds in to the cache manager
        self.guilds = {}
        self.user = None

        self._loop = asyncio.get_event_loop()

        self._gateway_info = self._loop.run_until_complete(self._get_gateway())

        self.intents = intents
        self._token = token

        self._activity = activity
        self._status = status
        self._mobile = mobile
        self._none_guilds_cached = False

        APIModelBase.set_client(self)

        init_logging(logs)

    async def _get_gateway(self):
        """Get Gateway information"""
        return GatewayBotInfo.from_dict(await self.http.get("gateway/bot"))

    def listen(self, callback: Coro):
        """Method or Decorator to set the listener.

        Parameters
        ----------
        callback : :class:`melisa.utils.types.Coro`
            Coroutine Callback Function
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError(f"<{callback.__qualname__}> must be a coroutine function")

        self._events[callback.__qualname__] = callback
        _logger.debug(f"Listener {callback.__qualname__} added successfully!")
        return self

    def run(self) -> None:
        """
        Run Bot without shards (only 0 shard)
        """
        inited_shard = Shard(self, 0, 1)

        asyncio.ensure_future(
            inited_shard.launch(activity=self._activity,
                                status=self._status,
                                mobile=self._mobile,
                                loop=self._loop,
                                )
        )
        self._loop.run_forever()

    def run_shards(self, num_shards: int, *, shard_ids: List[int] = None):
        """
        Run Bot with shards specified by the user.

        Parameters
        ----------
        num_shards : :class:`int`
            The endpoint to send the request to.
        shard_ids: Optional[:class:`List[int]`]
            List of Ids of shards to start.
        """
        if not shard_ids:
            shard_ids = range(num_shards)

        for shard_id in shard_ids:
            inited_shard = Shard(self, shard_id, num_shards)

            asyncio.ensure_future(
                inited_shard.launch(activity=self._activity,
                                    status=self._status,
                                    mobile=self._mobile),
                loop=self._loop,
            )
        self._loop.run_forever()

    def run_autosharded(self):
        """
        Runs the bot with the amount of shards specified by the Discord gateway.
        """
        num_shards = self._gateway_info.shards
        shard_ids = range(num_shards)

        for shard_id in shard_ids:
            inited_shard = Shard(self, shard_id, num_shards)

            asyncio.ensure_future(
                inited_shard.launch(activity=self._activity,
                                    status=self._status,
                                    mobile=self._mobile),
                loop=self._loop,
            )
        self._loop.run_forever()

    async def fetch_user(self, user_id: Union[Snowflake, str, int]):
        """
        Fetch User from the Discord API (by id).

        Parameters
        ----------
        user_id : :class:`Union[Snowflake, str, int]`
            Id of user to fetch
        """

        # ToDo: Update cache if USER_CACHING enabled.

        data = await self.http.get(f"users/{user_id}")

        return User.from_dict(data)

    async def fetch_guild(self, guild_id: Union[Snowflake, str, int]):
        """
        Fetch Guild from the Discord API (by id).

        Parameters
        ----------
        guild_id : :class:`Union[Snowflake, str, int]`
            Id of guild to fetch
        """

        # ToDo: Update cache if GUILD_CACHE enabled.

        data = await self.http.get(f"guilds/{guild_id}")

        return Guild.from_dict(data)

    async def fetch_channel(
            self, channel_id: Union[Snowflake, str, int]
    ) -> Union[Channel, Any]:
        """
        Fetch Channel from the Discord API (by id).
        If type of channel is unknown:
        it will return just :class:`melisa.models.guild.channel.Channel` object.

        Parameters
        ----------
        channel_id : :class:`Union[Snowflake, str, int]`
            Id of channel to fetch
        """

        # ToDo: Update cache if CHANNEL_CACHE enabled.

        data = (await self.http.get(f"channels/{channel_id}")) or {}

        data.update({"type": ChannelType(data.pop("type"))})

        channel_cls = channel_types_for_converting.get(data["type"], Channel)
        return channel_cls.from_dict(data)
