from functools import wraps
from .RTMClient import RTMClient
from .WebClient import WebClient
from mebot.exceptions.MebotException import MebotException

class Client:
    _CLIENT_CLASSES = {
        "RTMClient": RTMClient,
        "WebClient": WebClient
    }
    _CLIENTS = {}

    def __init__(self, client_type):
        self._client_type = client_type
        self._client_class = self._CLIENT_CLASSES[client_type]
        self._client = None

    def start(self, token, *args, **kwargs):
        if "WebClient" not in self._CLIENTS:
            self._CLIENTS["WebClient"] = WebClient.start(token, *args, **kwargs)
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
    
    @classmethod
    async def send_to_slack(cls, *, channel=None, user_id=None, thread_id=None, msg):
        if channel:
            return await cls._CLIENT_CLASSES["WebClient"].send_to_channel(
                channel = channel,
                msg = msg,
                thread_id = thread_id
            )
        else:
            return await cls._CLIENT_CLASSES["WebClient"].send_to_user(
                user_id = user_id,
                msg = msg,
                thread_id = thread_id
            )