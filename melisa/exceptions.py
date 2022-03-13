class MelisaException(Exception):
    """Base exception"""
    pass


class ClientException(MelisaException):
    """Handling user errors"""
    pass


class InvalidPayload(MelisaException):
    """This exception means invalid payload"""
    pass


class LoginFailure(ClientException):
    """Fails to log you in from improper credentials or some other misc."""
    pass


class ConnectionClosed(ClientException):
    """Exception that's thrown when the gateway connection is closed for reasons that could not be handled
    internally. """

    def __init__(self, socket, *, shard_id, code=None):
        message = "Websocket with shard ID {} closed with code {}"
        self.code = code or socket.close_code
        self.shard_id = shard_id

        super().__init__(message.format(self.shard_id, self.code))


class PrivilegedIntentsRequired(ClientException):
    """Occurs when the gateway requests privileged intents, but they are not yet marked on the developer page.

    Visit to https://discord.com/developers/applications/
    """

    def __init__(self, shard_id):
        self.shard_id = shard_id
        message = "Shard ID {} is requesting privileged intents that have not been explicitly enabled in the " \
                  "developer portal. Please visit to https://discord.com/developers/applications/ "

        super().__init__(message.format(self.shard_id))


class HTTPException(MelisaException):
    """Occurs when an HTTP request operation fails."""


class NotModifiedError(HTTPException):
    """Error code 304."""


class BadRequestError(HTTPException):
    """Error code 400."""


class UnauthorizedError(HTTPException):
    """Error code 401."""


class ForbiddenError(HTTPException):
    """Error code 403."""


class NotFoundError(HTTPException):
    """Error code 404."""


class MethodNotAllowedError(HTTPException):
    """Error code 405."""


class RateLimitError(HTTPException):
    """Error code 429."""


class GatewayError(HTTPException):
    """Error code 502."""


class ServerError(HTTPException):
    """Error code 5xx."""
