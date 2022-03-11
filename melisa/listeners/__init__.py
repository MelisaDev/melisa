from __future__ import annotations

from glob import glob
from importlib import import_module
from os import chdir
from pathlib import Path


def get_listeners():
    listeners_list = {}

    chdir(Path(__file__).parent.resolve())

    for listener_path in glob("*.py"):
        if listener_path.startswith("__"):
            continue

        event = listener_path[:-3]

        try:
            listeners_list[event] = getattr(
                import_module(f".{event}", package=__name__), "export"
            )()
        except AttributeError:
            continue

    return listeners_list


listeners = get_listeners()
