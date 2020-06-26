import asyncio
from functools import wraps
from slack import WebClient as SlackWebClient
from slack.errors import SlackApiError

from mebot.utils.Singleton import Singleton
from mebot.exceptions.MebotException import MebotException

class WebClient(Singleton):

    @wraps(SlackWebClient.__init__)
    def __init__(self, token, *args, **kwargs):
        super().__init__()
        self._client = SlackWebClient(
            token=token,
            run_async=True,
            loop=asyncio.get_running_loop(),
            *args,
            **kwargs)
    
    @classmethod
    @wraps(SlackWebClient.__init__)
    def start(cls, token, *args, **kwargs):
        return cls.instantiate(token, *args, **kwargs)._client

    @classmethod
    async def stop(cls):
        pass

    def on(cls, event):
        raise MebotException("Cannot wait for events on Websocket Client :/")

    @classmethod
    async def send_to_channel(cls, channel, msg, thread_id = None):
        try:
            if not thread_id:
                response = await cls.instance()._client.chat_postMessage(
                    channel=channel,
                    text=msg
                )
            else:
                response = await cls.instance()._client.chat_postMessage(
                    channel=channel,
                    text=msg,
                    thread_ts=thread_id
                )
            assert response["message"]["text"] == msg
            response = response["message"]
            return {
                "dialogue_id": response["thread_ts"] if "thread_ts" in response else response["ts"]
            }
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            return {}

    @classmethod
    async def send_to_user(cls, user_id, msg, thread_id = None):
        web_client = cls.instance()._client
        try:
            response = await web_client.conversations_open(
                users = [user_id]
            )
            im_id = response["channel"]["id"]
            return await cls.send_to_channel(im_id, msg, thread_id=thread_id)
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            return {}