# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

# We found this file in the Pincer Python Module and modified it. Thank you Pincer Devs!

from __future__ import annotations

import copy
import datetime
from dataclasses import _is_dataclass_instance, fields
from enum import Enum, EnumMeta
from inspect import getfullargspec
from itertools import chain
from typing import (
    Dict,
    Union,
    Generic,
    TypeVar,
    Any, get_origin, Tuple, get_args,
)

from typing_extensions import get_type_hints

from melisa.utils.types import APINullable, TypeCache

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

    def __get_types(self, arg_type: type) -> Tuple[type]:
        origin = get_origin(arg_type)

        if origin is Union:
            # noinspection PyTypeChecker
            args: Tuple[type] = get_args(arg_type)

            if 2 <= len(args) < 4:
                return args

            raise TypeError

        return (arg_type, )

    def __attr_convert(self, attr_value: Dict, attr_type: T) -> T:
        factory = attr_type

        # Always use `__factory__` over __init__
        if getattr(attr_type, "__factory__", None):
            factory = attr_type.__factory__

        if attr_value is None:
            return None

        if attr_type is not None and isinstance(attr_value, attr_type):
            return attr_value

        if isinstance(attr_value, dict):
            return factory(attr_value)

        if isinstance(attr_value, datetime.datetime):
            return attr_value

        return factory(attr_value)

    def __post_init__(self):
        TypeCache()

        attributes = chain.from_iterable(
            get_type_hints(cls, globalns=TypeCache.cache).items()
            for cls in chain(self.__class__.__bases__, (self,))
        )

        for attr, attr_type in attributes:
            # Ignore private attributes.
            if attr.startswith("_"):
                continue

            types = self.__get_types(attr_type)

            types = tuple(
                filter(
                    lambda tpe: tpe is not None and tpe is not None, types
                )
            )

            if not types:
                raise TypeError

            specific_tp = types[0]

            attr_gotten = getattr(self, attr)

            if tp := get_origin(specific_tp):
                specific_tp = tp

            if isinstance(specific_tp, EnumMeta) and not attr_gotten:
                attr_value = None
            elif tp == list and attr_gotten and (classes := get_args(types[0])):
                attr_value = [
                    self.__attr_convert(attr_item, classes[0])
                    for attr_item in attr_gotten
                ]
            elif tp == dict and attr_gotten and (classes := get_args(types[0])):
                attr_value = {
                    key: self.__attr_convert(value, classes[1])
                    for key, value in attr_gotten.items()
                }
            else:
                attr_value = self.__attr_convert(attr_gotten, specific_tp)

            setattr(self, attr, attr_value)

    @classmethod
    def __factory__(cls: Generic[T], *args, **kwargs) -> T:
        return cls.from_dict(*args, **kwargs)

    def __repr__(self):
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if v and not k.startswith("_")
        )

        return f"{type(self).__name__}({attrs})"

    def __str__(self):
        if _name := getattr(self, "__name__", None):
            return f"{_name} {self.__class__.__name__.lower()}"

        return super().__str__()

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
                        data[key].value
                        if isinstance(data[key], Enum)
                        else data[key],
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
