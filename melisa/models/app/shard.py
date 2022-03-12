from __future__ import annotations

from asyncio import create_task, Task, sleep
from typing import Optional

from ...core.gateway import Gateway
from ..user import BotActivity


class Shard:
    def __init__(self,
                 client,
                 shard_id: int,
                 num_shards: int):
        self._client = client

        self._shard_id: int = shard_id
        self._num_shards: num_shards = num_shards
        self._gateway: Gateway

        self.disconnected = None

    @property
    def id(self) -> int:
        """Id of Shard"""
        return self._gateway.shard_id

    # @property
    # def

    async def launch(self, **kwargs) -> Shard:
        """Launches new shard"""
        self._gateway = Gateway(self._client,
                                self._shard_id,
                                self._num_shards,
                                start_activity=kwargs.get("activity"),
                                start_status=kwargs.get("status"))

        self._client.shards[self._shard_id] = self

        self.disconnected = False

        create_task(self._gateway.start_loop())

        return self

    async def _try_close(self) -> None:
        if self._gateway.connected:
            self._gateway.connected = False
            await self._gateway.close(code=1000)

    async def update_presence(self, activity: BotActivity = None, status: str = None) -> Shard:
        """
        Update Presence for the shard

        Parameters
        ----------
        activity: :class:`Activity`
            Activity to set
        status: :class:`str`
            Status to set (You can use :class:`~melisa.models.users.StatusType` to generate it)
        """
        data = self._gateway.generate_presence(activity, status)
        await self._gateway.update_presence(data)

        return self

    async def disconnect(self) -> None:
        """Disconnect current shard"""
        await self._try_close()

    async def reconnect(self, wait_time: int = 3) -> None:
        """Reconnect current shard

        Parameters
        ----------
        wait_time: :class:`int`
            Reconnect after
        """
        await self._try_close()
        await sleep(wait_time)
        await self.launch()
