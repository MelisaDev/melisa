# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

import logging
import logging.config
import sys
from typing import Union, Dict, Any


def init_logging(
    flavor: Union[None, str, int, Dict[str, Any]],
) -> None:
    """Attempt to initialize logging for the user.
    If any handlers already exist, this is ignored entirely. This ensures the
    user can use any existing logging configuration without us interfering.
    You can manually disable logging by passing `None` as the `flavor` parameter.

    Parameters
    ----------
    flavor: Optional[None, :class:`str`, Dict[:class:`str`, Any]]
        This can be `None` to disable logging automatically.
        If you pass a :class:`str` or a :class:`int`, it is interpreted as
        the global logging level to use, and should match one of **DEBUG**,
        **INFO**, **WARNING**, **ERROR** or **CRITICAL**, if :class:`str`.
    """

    # This method was found in the hikari source code and modified, thank you, hikari devs

    if len(logging.root.handlers) != 0 or flavor is None:
        return

    if isinstance(flavor, dict):
        logging.config.dictConfig(flavor)

        if flavor.get("handlers"):
            return

        flavor = None

    logging.logThreads = False
    logging.logProcesses = False

    logging.basicConfig(
        level=flavor,
        format="[%(asctime)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )
    logging.captureWarnings(True)
