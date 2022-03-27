# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import copy
from dataclasses import _is_dataclass_instance, fields
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


def to_dict_without_none(model):
    """
    Converts discord model or other object to dict.
    """
    if _is_dataclass_instance(model):
        result = []

        for field in fields(model):
            value = to_dict_without_none(getattr(model, field.name))

            if isinstance(value, Enum):
                result.append((field.name, value.value))
            elif value is not None and not field.name.startswith("_"):
                result.append((field.name, value))

        return dict(result)

    if isinstance(model, tuple) and hasattr(model, "_fields"):
        return type(model)(*[to_dict_without_none(v) for v in model])

    if isinstance(model, (list, tuple)):
        return type(model)(to_dict_without_none(v) for v in model)

    if isinstance(model, dict):
        return type(model)(
            (to_dict_without_none(k), to_dict_without_none(v)) for k, v in model.items()
        )

    return copy.deepcopy(model)


class APIModelBase:
    """
    Represents an object which has been fetched from the Discord API.
    """

    _client = None

    @property
    def _http(self):
        if not self._client:
            return None

        return self._client.http

    @classmethod
    def set_client(cls, client):
        cls._client = client

    @classmethod
    def from_dict(cls: Generic[T], data: Dict[str, Union[str, bool, int, Any]]) -> T:
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
                        data[key].value if isinstance(data[key], Enum) else data[key],
                    ),
                    filter(
                        lambda object_argument: data.get(object_argument) is not None,
                        getfullargspec(cls.__init__).args,
                    ),
                )
            )
        )

    def to_dict(self) -> Dict:
        return to_dict_without_none(self)
