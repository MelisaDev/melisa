# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED
from ...utils.snowflake import Snowflake
from ...utils.timestamp import Timestamp


@dataclass(repr=False)
class ThreadMetadata(APIModelBase):
    """
    Represents a Discord Thread Metadata object

    Attributes
    ----------
    archived: :class:`bool`
        Whether the thread is archived
    auto_archive_duration: :class:`int`
        Duration in minutes to automatically archive the thread after recent activity,
        can be set to: 60, 1440, 4320, 10080
    archive_timestamp: :class:`~melisa.utils.timestamp.Timestamp`
        Timestamp when the thread's archive status was last changed,
        used for calculating recent activity
    locked: :class:`bool`
        Whether the thread is locked; when a thread is locked,
        only users with ``MANAGE_THREADS`` can unarchive it
    invitable: Optional[:class:`bool`]
        Whether non-moderators can add other non-moderators to a thread;
        only available on private threads
    create_timestamp: Optional[:class:`~melisa.utils.timestamp.Timestamp`]
        Timestamp when the thread was created; only populated for threads created after 2022-01-09
    """

    archived: bool
    auto_archive_duration: int
    archive_timestamp: Timestamp
    locked: bool
    invitable: APINullable[bool] = None
    create_timestamp: APINullable[Timestamp] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a thread metadata object from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into thread metadata.
        """
        self: ThreadMetadata = super().__new__(cls)

        self.archived = data["archived"]
        self.auto_archive_duration = data["auto_archive_duration"]
        self.archive_timestamp = Timestamp.parse(data["archive_timestamp"])
        self.locked = data["locked"]

        self.invitable = data.get("invitable", None)

        if data.get("create_timestamp"):
            self.create_timestamp = Timestamp.parse(data["create_timestamp"])
        else:
            self.create_timestamp = None

        return self


@dataclass(repr=False)
class ThreadMember(APIModelBase):
    """Represents a Discord Thread Member object

    Attributes
    ----------
    id: Optional[:class:`~melisa.utils.snowflake.Snowflake`]
        The id of the thread
    user_id: Optional[:class:`~melisa.utils.snowflake.Snowflake`]
        The id of the user
    join_timestamp: :class:`~melisa.utils.timestamp.Timestamp`
        The time the current user last joined the thread
    flags: :class:`int`
        Any user-thread settings, currently only used for notifications
    """

    join_timestamp: Timestamp
    flags: int
    id: APINullable[Snowflake] = None
    user_id: APINullable[Snowflake] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a thread member object from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into thread member.
        """
        self: ThreadMember = super().__new__(cls)

        self.archived = data["flags"]
        self.archive_timestamp = Timestamp.parse(data["join_timestamp"])

        self.id = Snowflake(data["id"]) if data.get("id") is not None else None
        self.user_id = (
            Snowflake(data["user_id"]) if data.get("user_id") is not None else None
        )

        return self
