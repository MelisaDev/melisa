# i not like PEP8, sorry

class MelisaException(Exception):
    """Base exception"""
    pass


class NoMoreItems(MelisaException):
    """Occurs when there are no more elements in an asynchronous iterative operation"""
    pass


class NotFoundGateway(MelisaException):
    """Occurs when the gateway for the websocket was not found"""
    def __init__(self):
        message = "The gateway to connect to Discord was not found"
        
        super().__init__(message)


class ClientException(MelisaException):
    """Handling user errors"""
    pass



class InvalidData(ClientException):
    """Unknown or invalid data from Discord"""
    pass


class LoginFailure(ClientException):
    """Fails to log you in from improper credentials or some other misc."""
    pass


class ConnectionClosed(ClientException):
    """Exception that's thrown when the gateway connection is closed for reasons that could not be handled internally."""
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
        message = "Shard ID {} is requesting privileged intents that have not been explicitly enabled in the developer portal. Please visit to https://discord.com/developers/applications/ "

        super().__init__(message.format(self.shard_id))


class HttpException(MelisaException):
    """Occurs when an HTTP request operation fails."""

    def __init__(self, response):
        self.responce = response
        self.status = response.status
        message = "{} with responce status {}"
        
        super().__init__(message.format(self.responce, self.status))


class DiscordErrorServer(HttpException):
    """Error that is issued when the status code 500"""
    pass


class NotFound(HttpException):
    """Error that is issued when the status code 404"""
    pass


class Forbidden(HttpException):
    """Error that is issued when the status code 403"""
    pass
