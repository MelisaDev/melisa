# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from enum import IntEnum


class ApplicationCommandTypes(IntEnum):
    """Application Command Types

    Attributes
    ----------
    CHAT_INPUT:
        Slash commands; a text-based command that shows up when a user types /
    USER:
        A UI-based command that shows up when you right click or tap on a user
    MESSAGE:
        A UI-based command that shows up when you right click or tap on a message
    """

    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3

    def __int__(self):
        return self.value
