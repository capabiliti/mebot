import asyncio
import os
from functools import wraps
from slack import RTMClient as SlackRTMClient

from mebot.utils.Singleton import Singleton
from mebot.exceptions.MebotException import MebotException

class RTMClient(Singleton):

    @wraps(SlackRTMClient.__init__)
    def __init__(self, token, *args, **kwargs):
        super().__init__()
        self._client = SlackRTMClient(
            token=token,
            run_async=True,
            loop=asyncio.get_running_loop(),
            *args,
            **kwargs)
        old_os_name = os.name
        os.name = 'nt'
        self._client.start()
        os.name = old_os_name
    
    @classmethod
    @wraps(SlackRTMClient.__init__)
    def start(cls, token, *args, **kwargs):
        return cls.instantiate(token, *args, **kwargs)._client
    
    @classmethod
    async def stop(cls):
        await cls.instance()._client.async_stop()

    @classmethod
    def on(cls, event):
        def decorator(callback):
            @SlackRTMClient.run_on(event=event)
            @wraps(callback)
            async def wrapper(**payload):
                await callback(**payload)
            return wrapper
        return decorator