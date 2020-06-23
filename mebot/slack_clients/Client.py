from functools import wraps
from .RTMClient import RTMClient
from mebot.exceptions.MebotException import MebotException

class Client:
    _CLIENT_CLASSES = {
        "RTMClient": RTMClient
    }
    _CLIENTS = {}

    def __init__(self, client_type):
        self._client_type = client_type
        self._client_class = self._CLIENT_CLASSES[client_type]
        self._client = None

    def start(self, token, *args, **kwargs):
        self._client = self._client_class.start(token, *args, **kwargs)
        self._CLIENTS[self._client_type] = self._client
    
    async def stop(self):
        del self._CLIENTS[self._client_type]
        await self._client.stop()

    def on(self, event):
        def decorator(callback):
            @self._client_class.on(event)
            @wraps(callback)
            async def wrapper(**payload):
                await callback(**payload)
            return wrapper
        return decorator
    
    @classmethod
    def get(cls, client_type):
        return cls._CLIENTS.get(client_type)
