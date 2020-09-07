from typing import Union
from pydantic import BaseModel

from mebot.server import Server


class SlackMessage(BaseModel):
    user: Union[str, None]
    channel: Union[str, None]
    msg: str


@Server.APP.post("/send_msg")
async def send_to_slack(slack_message: SlackMessage):
    msg = slack_message.msg
    if slack_message.channel:
        return await Server.SLACK_CLIENT.send_to_slack(
            channel = slack_message.channel,
            msg = msg)
    elif slack_message.user:
        return await Server.SLACK_CLIENT.send_to_slack(
            user = slack_message.user,
            msg = msg)
