# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

# We found this file in the Pincer Python Module and modified it. Thank you Pincer Devs!

from __future__ import annotations

import copy
from dataclasses import _is_dataclass_instance, fields
from enum import Enum, EnumMeta
from inspect import getfullargspec
from itertools import chain
from typing import (
    Dict,
    Union,
    Generic,
    TypeVar,
    Any,
    get_origin,
    Tuple,
    get_args, Optional,
)

from typing_extensions import get_type_hints

from melisa.utils.types import UndefinedType, TypeCache, UNDEFINED

T = TypeVar("T")


def _asdict_ignore_none(obj: Generic[T]) -> Union[Tuple, Dict, T]:
    """
    Returns a dict from a dataclass that ignores
    all values that are None
    Modification of _asdict_inner from dataclasses
    Parameters
    ----------
    obj: Generic[T]
        The object to convert
    Returns
    -------
        A dict without None values
    """

    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_ignore_none(getattr(obj, f.name))

            if isinstance(value, Enum):
                result.append((f.name, value.value))
            # This if statement was added to the function
            elif not isinstance(value, UndefinedType) and not f.name.startswith(
                "_"
            ):
                result.append((f.name, value))

        return dict(result)

    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[_asdict_ignore_none(v) for v in obj])

    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_ignore_none(v) for v in obj)

    elif isinstance(obj, dict):
        return type(obj)(
            (_asdict_ignore_none(k), _asdict_ignore_none(v))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


class APIModelBase:
    """
    Represents an object which has been fetched from the Discord API.
    """

    _client: Optional[Any] = None

    @property
    def _http(self):
        if not self._client:
            raise AttributeError("Object is not yet linked to a client")

        return self._client.http

    @classmethod
    def set_client(cls, client):
        cls._client = client

    def __get_types(self, attr: str, arg_type: type) -> Tuple[type]:
        origin = get_origin(arg_type)

        if origin is Union:
            # Ahh yes, typing module has no type annotations for this...
            # noinspection PyTypeChecker
            args: Tuple[type] = get_args(arg_type)

            if 2 <= len(args) < 4:
                return args

            raise ValueError(
                f"Attribute `{attr}` in `{type(self).__name__}` has too many "
                f"or not enough arguments! (got {len(args)} expected 2-3)"
            )

        return (arg_type,)

    def __attr_convert(self, attr_value: Dict, attr_type: T) -> T:
        factory = attr_type

        # Always use `__factory__` over __init__
        if getattr(attr_type, "__factory__", None):
            factory = attr_type.__factory__

        if attr_value is UNDEFINED:
            return UNDEFINED

        if attr_type is not None and isinstance(attr_value, attr_type):
            return attr_value

        if isinstance(attr_value, dict):
            return factory(attr_value)

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

            types = self.__get_types(attr, attr_type)

            types = tuple(
                filter(
                    lambda tpe: tpe is not None and tpe is not UNDEFINED, types
                )
            )

            if not types:
                raise ValueError(
                    f"Attribute `{attr}` in `{type(self).__name__}` only "
                    "consisted of missing/optional type!"
                )

            specific_tp = types[0]

            attr_gotten = getattr(self, attr)

            if tp := get_origin(specific_tp):
                specific_tp = tp

            if isinstance(specific_tp, EnumMeta) and not attr_gotten:
                attr_value = UNDEFINED
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

    def to_dict(self) -> Dict:
        """
        Transform the current object to a dictionary representation. Parameters that
        start with an underscore are not serialized.
        """
        return _asdict_ignore_none(self)
