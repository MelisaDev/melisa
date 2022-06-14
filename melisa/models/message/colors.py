# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import random
import string
import typing


CT = typing.TypeVar("CT", bound="Color")


class Color:
    """Represents a Discord colour. This class is similar
    to a (red, green, blue) :class:`tuple`.

    .. container:: operations
        .. describe:: x == y
             Checks if two colours are equal.
        .. describe:: x != y
             Checks if two colours are not equal.
        .. describe:: hash(x)
             Return the colour's hash.
        .. describe:: str(x)
             Returns the hex format for the colour.
        .. describe:: int(x)
             Returns the raw colour value.

    Attributes
    ----------
    value: :class:`int`
        The raw integer colour value.
    """

    __slots__ = ("value",)

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int parameter, received {value.__class__.__name__} instead."
            )

        self.value: int = value

    def _get_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xFF

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, Color) and self.value == other.value

    def __ne__(self, other: typing.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<Colour value={self.value}>"

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def r(self) -> int:
        """:class:`int`: Returns the red component of the colour."""
        return self._get_byte(2)

    @property
    def g(self) -> int:
        """:class:`int`: Returns the green component of the colour."""
        return self._get_byte(1)

    @property
    def b(self) -> int:
        """:class:`int`: Returns the blue component of the colour."""
        return self._get_byte(0)

    def to_rgb(self) -> typing.Tuple[int, int, int]:
        """
        Tuple[:class:`int`, :class:`int`, :class:`int`]:
            Returns an (r, g, b) tuple representing the colour."""
        return (self.r, self.g, self.b)

    @classmethod
    def from_rgb(cls: typing.Type[CT], r: int, g: int, b: int) -> CT:
        """Constructs a :class:`Colour` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def from_hex_code(cls, hex_code: str, /) -> Color:
        """Convert the given hexadecimal color code to a `Color`.

        The inputs may be of the following format (case insensitive):
        `1a2`, `#1a2`, `0x1a2` (for web-safe colors), or
        `1a2b3c`, `#1a2b3c`, `0x1a2b3c` (for regular 3-byte color-codes).

        Parameters
        ----------
        hex_code: :class:`str`
            A hexadecimal color code to parse. This may optionally start with
            a case insensitive `0x` or `#`.

        Returns
        -------
        Color
            A corresponding Color object.

        Raises
        ------
        :class:`ValueError`
            If ``hex_code`` is not a hexadecimal or is a invalid length.
        """
        if hex_code.startswith("#"):
            hex_code = hex_code[1:]
        elif hex_code.startswith(("0x", "0X")):
            hex_code = hex_code[2:]

        if not all(c in string.hexdigits for c in hex_code):
            raise ValueError("Color code must be hexadecimal")

        if len(hex_code) == 3:
            r, g, b = (c << 4 | c for c in (int(c, 16) for c in hex_code))
            return cls.from_rgb(r, g, b)

        if len(hex_code) == 6:
            return cls.from_rgb(
                int(hex_code[:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)
            )

        raise ValueError("Color code is invalid length. Must be 3 or 6 digits")

    @classmethod
    def default(cls: typing.Type[CT]) -> CT:
        """A factory method that returns a :class:`Colour` with a value of ``0``."""
        return cls(0)
