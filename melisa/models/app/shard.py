# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from asyncio import create_task, sleep

from ...core.gateway import Gateway
from ..user import Activity


class Shard:
    def __init__(self, client, shard_id: int, num_shards: int):
        self._client = client

        self._shard_id: int = shard_id
        self._num_shards: num_shards = num_shards
        self._gateway: Gateway

        self.disconnected = None

    @property
    def id(self) -> int:
        """Id of Shard"""
        return self._gateway.shard_id

    @property
    def latency(self) -> float:
        """:class:`float`:
        Measures latency between a HEARTBEAT command
        and a HEARTBEAT_ACK event in seconds for this shard"""
        return self._gateway.latency

    async def launch(self, **kwargs) -> Shard:
        """|coro|

        Launches new shard"""
        self._gateway = Gateway(
            self._client,
            self._shard_id,
            self._num_shards,
            start_activity=kwargs.get("activity"),
            start_status=kwargs.get("status"),
            mobile=kwargs.get("mobile"),
        )

        self._client.shards[self._shard_id] = self

        self.disconnected = False

        create_task(self._gateway.connect())

        return self

    async def close(self):
        """|coro|
        Disconnect shard
        """
        create_task(self._gateway.close())

    async def update_presence(
        self, activity: Activity = None, status: str = None
    ) -> Shard:
        """
        |coro|

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

    async def reconnect(self, wait_time: int = 3) -> None:
        """|coro|

        Reconnect current shard

        Parameters
        ----------
        wait_time: :class:`int`
            Reconnect after
        """
        await self.close()
        await sleep(wait_time)
        await self.launch()
