# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import asyncio
import logging
import signal
import sys
import traceback
from typing import Dict, List, Union, Any, Iterable, Optional, Callable

from .rest import RESTApp
from .core.gateway import GatewayBotInfo
from .models.guild.channel import Channel
from .models import Activity
from .models.app.shard import Shard
from .models.app.intents import Intents
from .utils.snowflake import Snowflake
from .utils.api_model import APIModelBase
from .utils.logging import init_logging
from .utils.types import Coro
from .utils.waiters import WaiterMgr

_logger = logging.getLogger("melisa")


class Client:
    """
    This is the main instance which is between the programmer and the Discord API.
    This Client represents your bot.
    Parameters
    ----------
    token: :class:`str`
        The token to login (you can found it in the developer portal)
    asyncio_debug: :class:`bool`
        If ``True``, then debugging is enabled for the asyncio event loop in use.
    intents: :class:`Union[~melisa.Intents, Iterable[~melisa.Intents]]`
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
        *,
        asyncio_debug: bool = False,
        intents: Union[Intents, Iterable[Intents]] = None,
        activity: Optional[Activity] = None,
        status: str = None,
        mobile: bool = False,
        logs: Union[None, int, str, Dict[str, Any]] = "INFO",
    ):
        self._loop = asyncio.get_event_loop()

        self.shards: Dict[int, Shard] = {}
        self.rest: RESTApp = RESTApp(token)
        self.http = self.rest.http
        self._events: Dict[str, Coro] = {}
        self._waiter_mgr = WaiterMgr(self._loop)

        # ToDo: Transfer guilds in to the cache manager
        self.guilds = {}
        self.user = None

        self._gateway_info = self._loop.run_until_complete(self._get_gateway())

        if isinstance(intents, Iterable):
            self.intents = sum(intents)
        elif intents is None:
            self.intents = (
                Intents.all() - Intents.GUILD_PRESENCES - Intents.GUILD_MEMBERS
            )
        else:
            self.intents = intents

        self._token = token

        self._activity = activity
        self._status = status
        self._mobile = mobile
        self._none_guilds_cached = False

        APIModelBase.set_client(self)

        init_logging(logs)

        def sigint_handler(_signal, _frame):
            _logger.info("SIGINT received, shutting down...")

            asyncio.create_task(self.http.close())

            if self._loop.is_running():
                self._loop.stop()

            print("(SIGINT received some seconds ago) Successfully stopped client loop")

        if asyncio_debug:
            self._loop.set_debug(True)

        signal.signal(signal.SIGINT, sigint_handler)

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

    async def dispatch(self, name: str, *args):
        """
        Dispatches an event
        Parameters
        ----------
        name: :class:`str`
            Name of the event to dispatch.
        """
        coro = self._events.get(name)

        if coro is not None:
            try:
                await coro(*args)
            except Exception as exc:
                custom_error = self._events.get("on_error")

                if custom_error is not None:
                    asyncio.ensure_future(custom_error(exc))
                else:
                    print(f"Ignoring exception in {name}", file=sys.stderr)
                    traceback.print_exc()

        self._waiter_mgr.process_events(name, *args)

    def run(self):
        """
        Run Bot without shards (only 0 shard)
        """
        inited_shard = Shard(self, 0, 1)

        asyncio.ensure_future(
            inited_shard.launch(
                activity=self._activity,
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
                inited_shard.launch(
                    activity=self._activity, status=self._status, mobile=self._mobile
                ),
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
                inited_shard.launch(
                    activity=self._activity, status=self._status, mobile=self._mobile
                ),
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

        return await self.rest.fetch_user(user_id)

    async def fetch_guild(self, guild_id: Union[Snowflake, str, int]):
        """
        Fetch Guild from the Discord API (by id).

        Parameters
        ----------
        guild_id : :class:`Union[Snowflake, str, int]`
            Id of guild to fetch
        """

        # ToDo: Update cache if GUILD_CACHE enabled.

        return await self.rest.fetch_guild(guild_id)

    async def fetch_channel(
        self, channel_id: Union[Snowflake, str, int]
    ) -> Union[Channel, Any]:
        """
        Fetch Channel from the Discord API (by id).

        Parameters
        ----------
        channel_id : :class:`Union[Snowflake, str, int]`
            Id of channel to fetch
        """

        # ToDo: Update cache if CHANNEL_CACHE enabled.

        return await self.rest.fetch_channel(channel_id)

    async def wait_for(
        self,
        event_name: str,
        *,
        check: Optional[Callable[..., bool]] = None,
        timeout: Optional[float] = None,
    ):
        """|coro|
        Waits for a WebSocket event to be dispatched.
        This could be used to wait for a user to reply to a message,
        or to react to a message.
        The ``timeout`` parameter is passed onto :func:`asyncio.wait_for`. By default,
        it does not timeout. Note that this does propagate the
        :exc:`asyncio.TimeoutError` for you in case of timeout and is provided for
        ease of use.
        In case the event returns multiple arguments, a :class:`tuple` containing those
        arguments is returned instead.
        This function returns the **first event that meets the requirements**.

        Examples
        --------
        Waiting for a user reply: ::

            @client.listen
            async def on_message_create(message):
                if message.content.startswith('$greet'):
                    channel = await client.fetch_channel(message.channel_id)
                    await channel.send('Say hello!')
                    def check(m):
                        return m.content == "hello" and channel.id == message.channel_id
                    msg = await client.wait_for('on_message_create', check=check, timeout=10.0)
                    await channel.send(f'Hello man!')

        Parameters
        ----------
        event_name: :class:`str`
            The type of event. It should starts with `on_`.
        check: Optional[Callable[[Any], :class:`bool`]]
            A predicate to check what to wait for. The arguments must meet the
            parameters of the event being waited for.
        timeout: Optional[:class:`float`]
            The number of seconds to wait before timing out and raising
            :exc:`asyncio.TimeoutError`.

        Returns
        ------
        Any
            Returns no arguments, a single argument, or a :class:`tuple` of multiple
            arguments that mirrors the parameters passed in the event.
        """
        return await self._waiter_mgr.wait_for(event_name, check, timeout)


Bot = Client
