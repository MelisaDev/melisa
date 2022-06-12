# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations


class Snowflake(int):
    """
    Discord utilizes Twitter's snowflake format for uniquely identifiable descriptors (IDs).
    These IDs are guaranteed to be unique across all of Discord,
    except in some unique scenarios in which child objects share their parent's ID.
    Because Snowflake IDs are up to 64 bits in size (e.g. a uint64),
    they are always returned as strings in the HTTP API
    to prevent integer overflows in some languages.
    See Gateway ETF/JSON for more information regarding Gateway encoding.

    Read more here: https://discord.com/developers/docs/reference#snowflakes
    """

    _MAX_VALUE: int = 9223372036854775807
    _MIN_VALUE: int = 0
    _DISCORD_EPOCH = 1420070400

    def __init__(self, _):
        super().__init__()

        if self < self._MIN_VALUE:
            raise ValueError("snowflake value should be greater than or equal to 0.")

        if self > self._MAX_VALUE:
            raise ValueError(
                "snowflake value should be less than or equal to 9223372036854775807."
            )

    @classmethod
    def __factory__(cls, string: str) -> Snowflake:
        return cls.from_string(string)

    @classmethod
    def from_string(cls, string: str):
        """Initialize a new Snowflake from a string.
        Parameters
        ----------
        string: :class:`str`
            The snowflake as a string.
        """
        return Snowflake(int(string))

    @property
    def timestamp(self) -> float:
        """
        Milliseconds since Discord Epoch, the first second of 2015 or 1420070400000.
        """
        return (self >> 22) / 1000 + self._DISCORD_EPOCH

    @property
    def worker_id(self) -> int:
        """Internal worker ID"""
        return (self >> 17) % 16

    @property
    def process_id(self) -> int:
        """Internal process ID"""
        return (self >> 12) % 16

    @property
    def increment(self) -> int:
        """For every ID that is generated on that process, this number is incremented"""
        return self % 2048

    @property
    def unix(self) -> int:
        return self.timestamp + 1420070400000
