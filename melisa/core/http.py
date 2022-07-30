# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import asyncio
import logging
from urllib.parse import quote
from typing import Dict, Optional, Any

from aiohttp import ClientSession, ClientResponse

from ..exceptions import (
    NotModifiedError,
    BadRequestError,
    ForbiddenError,
    UnauthorizedError,
    HTTPException,
    NotFoundError,
    MethodNotAllowedError,
    ServerError,
    RateLimitError,
)
from .ratelimiter import RateLimiter
from ..utils import remove_none

_logger = logging.getLogger("melisa.http")


class HTTPClient:
    API_VERSION = 10

    def __init__(self, token: str, *, ttl: int = 5):
        self.url: str = f"https://discord.com/api/v{self.API_VERSION}"
        self.max_ttl: int = ttl
        self.__rate_limiter = RateLimiter()

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {token}",
            "User-Agent": "Melisa Python Library",
        }

        self.__http_exceptions: Dict[int, HTTPException] = {
            304: NotModifiedError(),
            400: BadRequestError(),
            401: UnauthorizedError(),
            403: ForbiddenError(),
            404: NotFoundError(),
            405: MethodNotAllowedError(),
            429: RateLimitError(),
        }

        self.__aiohttp_session: ClientSession = ClientSession(headers=headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        """Close the aiohttp session"""
        await self.__aiohttp_session.close()

    async def __send(
        self,
        method: str,
        endpoint: str,
        *,
        _ttl: int = None,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Send an API request to the Discord API."""

        ttl = _ttl or self.max_ttl

        if ttl == 0:
            raise ServerError(f"Maximum amount of retries for `{endpoint}`.")

        _logger.debug(f"Sending {method} request to the {endpoint}")

        await self.__rate_limiter.wait_until_not_ratelimited(endpoint, method)

        url = f"{self.url}/{endpoint}"

        if headers is not None and headers.get("X-Audit-Log-Reason") is not None:
            headers["X-Audit-Log-Reason"] = quote(
                headers["X-Audit-Log-Reason"], safe="/ "
            )

        async with self.__aiohttp_session.request(
            method,
            url,
            params=remove_none(params),
            headers={
                "Content-Type": "application/json",
                **(remove_none(headers) or {}),
            },
            **kwargs,
        ) as response:
            return await self.__handle_response(
                response, method, endpoint, _ttl=ttl, **kwargs
            )

    async def __handle_response(
        self,
        res: ClientResponse,
        method: str,
        endpoint: str,
        *,
        _ttl: int = None,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Handle responses from the Discord API."""

        _logger.debug(f"Received response for the {endpoint} ({await res.text()})")

        self.__rate_limiter.save_response_bucket(endpoint, method, res.headers)

        if res.ok:
            if res.status == 204:
                _logger.debug("Request has been sent successfully.")
                return

            _logger.debug(
                "Request has been sent successfully and returned json response."
            )

            return await res.json()

        exception = self.__http_exceptions.get(res.status)

        if exception:
            if isinstance(exception, RateLimitError):
                timeout = (await res.json()).get("retry_after", 40)

                _logger.exception(
                    f"You are being ratelimited: {res.reason}."
                    f" The scope is {res.headers.get('X-RateLimit-Scope')}."
                    f" I will retry in {timeout} seconds"
                )

                await asyncio.sleep(timeout)
                return await self.__send(method, endpoint, **kwargs)

            _logger.error(
                f"  HTTP exception occurred while trying to send "
                f"a request to {endpoint}. ({res.status}, {res.reason})"
            )

            exception.__init__(res.reason)
            raise exception

        retry_in = 1 + (self.max_ttl - _ttl) * 2

        _logger.debug(
            "Discord side error occurred (hahahhaha, discord, fix yourself)."
            f" Status-Code: {res.status}. I will retry sending in {retry_in}s."
        )

        await asyncio.sleep(retry_in)

        return await self.__send(method, endpoint, _ttl=_ttl - 1, **kwargs)

    async def get(self, route: str, *, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """|coro|
        Sends a GET request to a Discord REST API endpoint.

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
        return await self.__send("GET", route, params=params)

    async def post(
        self,
        route: str,
        *,
        headers: Dict[str, Any] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """|coro|
        Sends a POST request to a Discord REST API endpoint.

        Parameters
        ----------
        route: :class:`str`
            The endpoint to send the request to.
        json: Dict[str, Any]
            Json data to post
        data: Any
            Data to post
        headers: Dict[str, Any]
            Custom request headers

        Returns
        -------
        Optional[:class:`Dict`]
            JSON response from the Discord API.
        """
        return await self.__send("POST", route, json=json, data=data, headers=headers)

    async def delete(self, route: str, *, headers: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """|coro|
        Sends a DELETE request to a Discord REST API endpoint.

        Parameters
        ----------
        route : :class:`str`
            The endpoint to send the request to.
        headers : :class:`dict`
            Custom request headers

        Returns
        -------
        Optional[:class:`Dict`]
            JSON response from the Discord API.
        """
        return await self.__send("DELETE", route, headers=headers)

    async def patch(
        self,
        route: str,
        *,
        headers: Dict[str, Any] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """|coro|
        Sends a PATCH request to a Discord REST API endpoint.

        Parameters
        ----------
        route : :class:`str`
            The endpoint to send the request to.
        data : Any
            Data to post
        json: Dict
            Json data to post
        headers : :class:`dict`
            Custom request headers

        Returns
        -------
        Optional[:class:`Dict`]
            JSON response from the Discord API.
        """
        return await self.__send("PATCH", route, json=json, data=data, headers=headers)

    async def put(
        self, route: str, *, headers: Dict[str, Any] = None, data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """|coro|
        Sends a PUT request to a Discord REST API endpoint.

        Parameters
        ----------
        route : :class:`str`
            The endpoint to send the request to.
        data : Dict
            Data to post
        headers : :class:`dict`
            Custom request headers

        Returns
        -------
        Optional[:class:`Dict`]
            JSON response from the Discord API.
        """
        return await self.__send("PUT", route, json=data, headers=headers)
