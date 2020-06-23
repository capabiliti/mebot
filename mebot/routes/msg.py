from pydantic import BaseModel
from slack.errors import SlackApiError

from mebot.server import Server
from mebot.slack_clients.Client import Client


class SlackMessage(BaseModel):
    channel: str
    msg: str

@Server.APP.post("/msg")
async def send_to_slack(slack_message: SlackMessage):
    channel = slack_message.channel
    msg = slack_message.msg
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
