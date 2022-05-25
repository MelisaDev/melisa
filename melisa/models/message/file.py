# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import io
import os
from typing import Union


class File:
    """
    A parameter object used for sending file objects.

    Attributes
    ----------
    filepath: Union[:class:`os.PathLike`, :class:`io.BufferedIOBase`]
        A file-like object opened in binary mode and read mode
        or a filename representing a file in the hard drive to
        open.

        .. note::
            If the file-like object passed is opened via ``open`` then the
            modes 'rb' should be used.
            To pass binary data, consider usage of ``io.BytesIO``.
    filename: Optional[:class:`str`]
        The filename to display when uploading to Discord.
        If this is not given then it defaults to ``fp.name`` or if ``filepath`` is
        a string then the ``filename`` will default to the string given.
    spoiler: :class:`bool`
        Whether the attachment is a spoiler.
    """

    def __init__(
        self,
        filepath: Union[str, bytes, os.PathLike, io.BufferedIOBase],
        *,
        filename: str = None,
        spoiler: bool = False,
    ):
        # Some features are from the discord.py lib, thanks discord.py devs.
        if isinstance(filepath, io.IOBase):
            if not (filepath.seekable() and filepath.readable()):
                raise ValueError(
                    f"File buffer {filepath!r} must be seekable and readable"
                )

            self.filepath = filepath
            self._owner = False
        else:
            self.filepath = open(filepath, "rb")
            self._owner = True

        if filename is None:
            if isinstance(filepath, str):
                _, self.filename = os.path.split(filepath)
            else:
                self.filename = getattr(filepath, "name", None)
        else:
            self.filename = filename

        self.spoiler = spoiler or (
            self.filename is not None and self.filename.startswith("SPOILER_")
        )

        if self.spoiler:
            self.filename = "SPOILER_" + filename

    def close(self):
        if self._owner:
            self.filepath.close()
