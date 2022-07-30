# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from typing import Dict


class LocalizedField:
    """
    Represents a field, that could be localized

    original: str
        Value of non-localized field
    localizations: Optional[Dict[str, str]]
        Dictionary with keys in
        `available locales <https://discord.com/developers/docs/reference#locales>`_

        Localization dictionary for the name field.
        Values follow the same restrictions as name

    """

    original: str
    localizations: Optional[Dict[str, str]]

    def __init__(
        self,
        original: str = None,
        localizations: Dict[str, str] = None,
    ):
        self.original: str = original
        self.localizations: Dict[str, str] = localizations

    def insert(self, locale: str, value: str) -> LocalizedField:
        self.localizations[locale] = value
        return self

    def remove(self, locale: str) -> LocalizedField:
        self.localizations.pop(locale, None)
        return self

    def __repr__(self):
        return f"<LocalizedField original={self.original} localizations={self.localizations}>"

    def __eq__(self, other):
        return self.original == other.original and self.localizations == other.localizations

    def __hash__(self):
        return hash((self.original, self.localizations))

    def __getitem__(self, key):
        return self.localizations[key]

    def __setitem__(self, key, value):
        self.localizations[key] = value

    def __delitem__(self, key):
        self.localizations.pop(key, None)

    def __contains__(self, key):
        return key in self.localizations

    def __iter__(self):
        return iter(self.localizations)

    def __len__(self):
        return len(self.localizations)

    def __str__(self):
        return self.original
