# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from asyncio import AbstractEventLoop, Event, wait_for as async_wait, TimeoutError as AsyncTimeOut
from typing import List, Callable, Optional

from ..exceptions import MelisaTimeoutError


class _Waiter:
    """
    Parameters
    ----------
    event_name : str
        The name of the event.
    check : Optional[Callable[[Any], :class:`bool`]]
        ``can_be_set`` only returns true if this function returns true.
        Will be ignored if set to None.

    Attributes
    ----------
    event: :class:`asyncio.Event`
        Even that is used to wait until the next valid discord event.
    return_value : Optional[str]
        Used to store the arguments from ``can_be_set`` so they can be
        returned later.
    """

    def __init__(self, event_name: str, check: Optional[Callable] = None):
        self.event_name = event_name
        self.check = check
        self.event = Event()
        self.return_value = None
        super().__init__()

    async def wait(self):
        """Waits until ``self.event`` is set."""
        await self.event.wait()

    def process(self, event_name: str, event_value):
        if self.event_name != event_name:
            return False

        if self.check:
            if event_value is not None:
                if not self.check(event_value):
                    return
            else:
                if not self.check():
                    return

        self.return_value = event_value
        self.event.set()


class WaiterMgr:
    """
    Attributes
    ----------
    waiter_list : List
        The List of events that need to be processed.
    """

    def __init__(self, loop: AbstractEventLoop):
        self.waiter_list: List[_Waiter] = []
        self.loop = loop

    def process_events(self, event_name, event_value):
        """
        Parameters
        ----------
        event_name : str
            The name of the event to be processed.
        event_value : Any
            The object returned from the middleware for this event.
        """
        for waiter in self.waiter_list:
            waiter.process(event_name, event_value)

    async def wait_for(
        self,
        event_name: str,
        check: Optional[Callable[..., bool]] = None,
        timeout: Optional[float] = None
    ):
        """
        Parameters
        ----------
        event_name: :class:`str`
            The type of event. It should start with `on_`.
        check: Optional[Callable[[Any], :class:`bool`]]
            This function only returns a value if this return true.
        timeout: Optional[float]
            Amount of seconds before timeout. Use None for no timeout.

        Returns
        ------
        Any
            What the Discord API returns for this event.
        """

        waiter = _Waiter(event_name, check)
        self.waiter_list.append(waiter)

        try:
            await async_wait(waiter.wait(), timeout=timeout)
            self.waiter_list.remove(waiter)
        except AsyncTimeOut:
            self.waiter_list.remove(waiter)
            raise MelisaTimeoutError(
                "wait_for() timed out while waiting for an event."
            )

        return waiter.return_value

