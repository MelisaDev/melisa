# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from datetime import datetime
from typing import Optional, TypeVar, Union

DISCORD_EPOCH = 1420070400
TS = TypeVar("TS", str, datetime, float, int)


class Timestamp:
    """Contains a lot of useful methods for working with unix timestamps.

    Attributes
    ----------
    date: :class:`str`
        The time of the timestamp.
    time: :class:`str`
        Alias for date.

    Parameters
    ----------
    time: Union[:class:`str`, :class:`int`, :class:`float`, :class:`datetime.datetime`]
    """

    def __init__(self, time: Optional[TS] = None):
        self.__time = Timestamp.parse(time)
        self.__epoch = int(time.timestamp() * 1000)
        self.date, self.time = str(self).split()

    @classmethod
    def __factory__(cls, time: Optional[TS] = None) -> datetime:
        return cls.parse(time)

    @staticmethod
    def parse(time: Optional[TS] = None) -> datetime:
        """Convert a time to datetime object.

        time: Optional[Union[:class:`str`, :class:`int`, :class:`float`, :class:`datetime.datetime`]]
            The time to be converted to a datetime object.
            This can be one of these types: datetime, float, int, str
            If no parameter is passed it will return the current
            datetime.

        Returns
        -------
        :class:`datetime.datetime`:
            The converted datetime object.
        """

        if isinstance(time, datetime):
            return time

        elif isinstance(time, str):
            return datetime.fromisoformat(time)

        elif isinstance(time, (int, float)):
            dt = datetime.utcfromtimestamp(t := int(time))

            if dt.year < 2015:
                t += DISCORD_EPOCH
            return datetime.utcfromtimestamp(t)

        return datetime.now()

    def __getattr__(self, key: str) -> int:
        return getattr(self.__time, key)

    def __str__(self) -> str:
        if len(string := str(self.__time)) == 19:
            return string + ".000"
        return string[:-3]

    def __int__(self) -> int:
        return self.__epoch

    def __float__(self) -> float:
        return self.__epoch / 1000

    def __ge__(self, other: Timestamp) -> bool:
        return self.__epoch >= other.__epoch

    def __gt__(self, other: Timestamp) -> bool:
        return self.__epoch > other.__epoch

    def __le__(self, other: Timestamp) -> bool:
        return self.__epoch <= other.__epoch

    def __lt__(self, other: Timestamp) -> bool:
        return self.__epoch < other.__epoch

    def __eq__(self, other: Timestamp) -> bool:
        return self.__epoch == other.__epoch

    def __ne__(self, other: Timestamp) -> bool:
        return self.__epoch != other.__epoch
