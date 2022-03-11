from .models.app import Shard
from .utils.types import Coro

from .core.http import HTTPClient

import asyncio
from typing import Dict


class Client:
    def __init__(self, token, intents, **kwargs):
        self.shards: Dict[int, Shard] = {}
        self.http = HTTPClient(token)
        self._events = {}

        self.guilds = []

        self.loop = asyncio.get_event_loop()

        self.intents = intents
        self._token = token

        self._activity = kwargs.get("activity")
        self._status = kwargs.get("status")

    def listen(self, callback: Coro):
        """Method to set the listener.
        Args:
            callback (:obj:`function`)
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

        asyncio.ensure_future(inited_shard.launch(activity=self._activity, status=self._status), loop=self.loop)
        self.loop.run_forever()
