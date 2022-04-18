# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from typing import Union

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
        self.http: HTTPClient = HTTPClient(token)

    async def fetch_user(self, user_id: Union[Snowflake, int, str]) -> User:
        """
        Fetch User from the Discord API (by id).

        Parameters
        ----------
        user_id: Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of user to fetch
        """

        data = await self.http.get(f"users/{user_id}")

        return User.from_dict(data)

    async def fetch_guild(self, guild_id: Union[Snowflake, int, str]) -> Guild:
        """
        Fetch Guild from the Discord API (by id).

        Parameters
        ----------
        guild_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of guild to fetch
        """

        data = await self.http.get(f"guilds/{guild_id}")

        return Guild.from_dict(data)

    async def fetch_channel(self, channel_id: Union[Snowflake, str, int]) -> Channel:
        """
        Fetch Channel from the Discord API (by id).

        Parameters
        ----------
        channel_id : Union[:class:`~melisa.utils.snowflake.Snowflake`, str, int]
            Id of channel to fetch
        """

        # ToDo: Update cache if CHANNEL_CACHE enabled.

        data = await self.http.get(f"channels/{channel_id}")

        return _choose_channel_type(data)
