import asyncio
import os
from functools import wraps
from slack import RTMClient as SlackRTMClient

from mebot.exceptions.MebotException import MebotException

class RTMClient:

    CLIENT = None

    @wraps(SlackRTMClient.__init__)
    def __init__(self, token, *args, **kwargs):
        if self.__class__.CLIENT != None:
            raise MebotException("RTMClient has already been initialized.")
        self.__class__.CLIENT = SlackRTMClient(
            token=token,
            run_async=True,
            loop=asyncio.get_running_loop(),
            *args,
            **kwargs)
        old_os_name = os.name
        os.name = 'nt'
        self.__class__.CLIENT.start()
        os.name = old_os_name
    
    @classmethod
    @wraps(SlackRTMClient.__init__)
    def start(cls, token, *args, **kwargs):
        if not cls.CLIENT:
            RTMClient(token, *args, **kwargs)
        return cls.CLIENT
    
    @classmethod
    async def stop(cls):
        await cls.CLIENT.async_stop()

    @classmethod
    def on(cls, event):
        def decorator(callback):
            @SlackRTMClient.run_on(event=event)
            @wraps(callback)
            async def wrapper(**payload):
                await callback(**payload)
            return wrapper
        return decorator