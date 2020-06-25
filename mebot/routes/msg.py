from typing import Union
from pydantic import BaseModel
from slack.errors import SlackApiError

from mebot.server import Server
from mebot.slack_clients.Client import Client


class SlackMessage(BaseModel):
    user: Union[str, None]
    channel: Union[str, None]
    msg: str


async def send_to_channel(channel, msg):
    try:
        response = await Client.get("RTMClient")._web_client.chat_postMessage(
            channel=channel,
            text=msg
        )
        assert response["message"]["text"] == msg
        return {}
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        return {}

async def send_to_user(user, msg):
    user_id = Server.SLACK_USERS[user]
    web_client = Client.get("RTMClient")._web_client
    try:
        response = await web_client.conversations_open(
            users = [user_id]
        )
        im_id = response["channel"]["id"]
        return await send_to_channel(im_id, msg)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        return {}

@Server.APP.post("/msg")
async def send_to_slack(slack_message: SlackMessage):
    channel = slack_message.channel if slack_message.channel else Server.SLACK_USERS[
        slack_message.user]
    msg = slack_message.msg
    if slack_message.channel:
        return await send_to_channel(slack_message.channel, msg)
    elif slack_message.user:
        return await send_to_user(slack_message.user, msg)

    
