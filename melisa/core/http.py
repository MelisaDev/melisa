from __future__ import annotations

import asyncio
from typing import Dict, Optional, Union, Any

from aiohttp import ClientSession, ClientResponse


class HTTPClient:
    def __init__(self, token: str, *, ttl: int = 5):
        self.url: str = f"https://discord.com/api/v9"
        self.max_ttl: int = ttl

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {token}",
            "User-Agent": f"Melisa Python Library"
        }

        self.__aiohttp_session: ClientSession = ClientSession(headers=headers)

    async def close(self):
        """Close the aiohttp session"""
        await self.__aiohttp_session.close()

    async def __send(
            self,
            method: str,
            endpoint: str,
            *,
            _ttl: int = None,
            **kwargs
    ) -> Optional[Dict]:
        """Send an API request to the Discord API."""

        ttl = _ttl or self.max_ttl

        url = f"{self.url}/{endpoint}"

        if ttl != 0:
            async with self.__aiohttp_session.request(method, url, **kwargs) as response:
                return await self.__handle_response(response, method, endpoint, __ttl=ttl, **kwargs)

    async def __handle_response(
            self,
            res: ClientResponse,
            method: str,
            endpoint: str,
            *,
            _ttl: int = None,
            **kwargs
    ) -> Optional[Dict]:
        """Handle responses from the Discord API."""
        if res.ok:
            return await res.json()

        retry_in = 1 + (self.max_ttl - _ttl) * 2

        await asyncio.sleep(retry_in)

        return await self.__send(
            method,
            endpoint,
            _ttl=_ttl - 1,
            **kwargs
        )

    async def get(
        self,
        route: str,
        params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """|coro|
        Sends a get request to a Discord REST endpoint.

        Parameters
        ----------
        route : :class:`str`
            The endpoint to send the request to.
        params: Optional[:class:`Dict`]
            The query parameters to add to the request.

        Returns
        -------
        Optional[:class:`Dict`]
            The response from Discord.
        """
        return await self.__send(
            "GET",
            route,
            params=params
        )
