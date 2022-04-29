# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from typing import Union, Optional

from .core.http import HTTPClient
from .utils.snowflake import Snowflake
from .models.guild.guild import Guild
from .models.user.user import User
from .models.guild.channel import _choose_channel_type, Channel


class RESTApp:
    """
    This instance may be used to send http requests to the Discord REST API.

    **It will not cache anything.**

    Parameters
    ----------
    token: :class:`str`
        The token to authorize (you can found it in the developer portal)
    """

    def __init__(self, token: str):
        self._http: HTTPClient = HTTPClient(token)

    async def fetch_user(self, user_id: Union[Snowflake, int, str]) -> User:
        """
        [**REST API**] Fetch User from the Discord API (by id).

        Parameters
        ----------
        user_id: Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of user to fetch
        """

        data = await self._http.get(f"users/{user_id}")

        return User.from_dict(data)

    async def fetch_guild(self, guild_id: Union[Snowflake, int, str]) -> Guild:
        """
        [**REST API**] Fetch Guild from the Discord API (by id).

        Parameters
        ----------
        guild_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of guild to fetch
        """

        data = await self._http.get(f"guilds/{guild_id}")

        return Guild.from_dict(data)

    async def fetch_channel(self, channel_id: Union[Snowflake, str, int]) -> Channel:
        """
        [**REST API**] Fetch Channel from the Discord API (by id).

        Parameters
        ----------
        channel_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of channel to fetch
        """

        data = await self._http.get(f"channels/{channel_id}")

        return _choose_channel_type(data)

    async def delete_message(
        self,
            channel_id: Union[Snowflake, str, int],
            message_id: Union[Snowflake, str, int],
            *,
            reason: Optional[str] = None
    ):
        """|coro|

        [**REST API**] Deletes only one specified message.

        Parameters
        ----------
        channel_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of channel, where message should be deleted
        message_id: Union[:class:`int`, :class:`str`, :class:`~.melisa.utils.snowflake.Snowflake`]
            Id of message to delete.
        reason: Optional[:class:`str`]
            The reason of the message delete operation.

        Raises
        -------
        HTTPException
            The request to perform the action failed with other http exception.
        ForbiddenError
            You do not have proper permissions to do the actions required.
            (You must have ``MANAGE_MESSAGES`` permission)
        """
        await self._http.delete(
            f"channels/{channel_id}/messages/{message_id}",
            headers={"X-Audit-Log-Reason": reason},
        )
