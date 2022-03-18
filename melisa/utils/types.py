from __future__ import annotations

from typing import TypeVar, Callable, Coroutine, Any, Union


T = TypeVar("T")

Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])

APINullable = Union[T, None]
