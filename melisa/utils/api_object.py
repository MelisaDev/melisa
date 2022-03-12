from __future__ import annotations

from enum import Enum
from inspect import getfullargspec
from typing import (
    Dict,
    Union,
    Generic,
    TypeVar,
    Any,
)

T = TypeVar("T")


class APIObjectBase:
    """
    Represents an object which has been fetched from the Discord API.
    """

    _client = None

    @property
    def _http(self):
        if not self._client:
            raise AttributeError("Object is not yet linked to a main client")

        return self._client.http

    @classmethod
    def from_dict(
        cls: Generic[T], data: Dict[str, Union[str, bool, int, Any]]
    ) -> T:
        """
        Parse an API object from a dictionary.
        """
        if isinstance(data, cls):
            return data

        # noinspection PyArgumentList
        return cls(
            **dict(
                map(
                    lambda key: (
                        key,
                        data[key].value
                        if isinstance(data[key], Enum)
                        else data[key],
                    ),
                    filter(
                        lambda object_argument: data.get(object_argument)
                        is not None,
                        getfullargspec(cls.__init__).args,
                    ),
                )
            )
        )
