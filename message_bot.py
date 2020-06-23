#! /usr/bin/env python

import os
import subprocess

import uvicorn
import yaml
from fastapi import FastAPI
from pydantic import BaseModel
from slack import WebClient
from slack.errors import SlackApiError

class SlackMessage(BaseModel):
    channel: str
    msg: str

SlackToken = yaml.load(subprocess.check_output(
    ["blackbox_cat", "secrets/keys.yaml.gpg"],
    stderr=subprocess.DEVNULL,
    cwd=os.environ["TP_HOME"]), Loader=yaml.FullLoader)["capabiliti_bot"]["bot_token"]

SlackClient = WebClient(SlackToken, run_async=True)

app = FastAPI()

@app.post('/msg')
async def send_to_slack(slack_message: SlackMessage):
    channel = slack_message.channel
    msg = slack_message.msg
    try:
        response = await SlackClient.chat_postMessage(
            channel=channel,
            text=msg
        )
        assert response["message"]["text"] == msg
        return {}
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        return {}

if __name__ == '__main__':
    uvicorn.run("message_bot:app", host='localhost', port=int("5000"), log_level="debug")