# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass

from ...utils.api_model import APIModelBase
from ...utils.types import APINullable
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
