from __future__ import annotations

from typing import TypeVar, Callable, Coroutine, Any, Union


class MissingType:

    def __repr__(self):
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, __o: object) -> bool:
        return __o is MISSING

    def __hash__(self) -> int:
        return hash(None)

MISSING = MissingType()

T = TypeVar("T")

Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])

APINullable = Union[T, None]