from .models import User
from .models.app import Shard
from .utils import Snowflake
from .utils.types import Coro

from .core.http import HTTPClient
from .core.gateway import GatewayBotInfo

import asyncio
from typing import Dict, List, Union


class Client:
    """
    This is the main instance which is between the programmer and the Discord API.

    This Client represents your bot.

    Parameters
    ----------
    token : :class:`str`
        The token to login (you can found it in the developer portal)
    intents : :class:`~objects.app.intents.Intents`
        The Discord Intents values.
    activity : :class:`~models.user.presence.BotActivity`
        The Activity to set (on connecting)
    status : :class:`str`
        The Status to set (on connecting). Can be generated using :class:`~models.user.presence.StatusType`

    Attributes
    ----------
    user: :class:`~models.user.user.User`
        The user object of the client
    http: :class:`~core.http.HTTPClient`
        HTTP client for the http-requests to the Discord API
    shards: :class:`Dict[int, Shard]`
        Bot's shards.
    """

    def __init__(self, token, intents, *, activity=None, status: str = None):
        self.shards: Dict[int, Shard] = {}
        self.http = HTTPClient(token)
        self._events = {}

        self.guilds = []
        self.user = None

        self._loop = asyncio.get_event_loop()

        self._gateway_info = self._loop.run_until_complete(self._get_gateway())

        self.intents = intents
        self._token = token

        self._activity = activity
        self._status = status

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
        return self

    def run(self) -> None:
        """
            Run Bot without shards (only 0 shard)
        """
        inited_shard = Shard(self, 0, 1)

        asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self._loop)
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

            asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self._loop)
        self._loop.run_forever()

    def run_autosharded(self):
        """
            Runs the bot with the amount of shards specified by the Discord gateway.
        """
        num_shards = self._gateway_info.shards
        shard_ids = range(num_shards)

        for shard_id in shard_ids:
            inited_shard = Shard(self, shard_id, num_shards)

            asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self._loop)
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
