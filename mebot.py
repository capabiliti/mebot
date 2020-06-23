#! /usr/bin/env python

import asyncio
import os
import subprocess
import yaml
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from slack.errors import SlackApiError

from mebot.options import cli_args
from mebot.slack_clients.Client import Client

SLACK_CLIENT = Client("RTMClient")
app = FastAPI()
class SlackMessage(BaseModel):
    channel: str
    msg: str

slack_token = yaml.load(subprocess.check_output(
    ["blackbox_cat", "secrets/keys.yaml.gpg"],
    stderr=subprocess.DEVNULL,
    cwd=os.environ["TP_HOME"]), Loader=yaml.FullLoader)["capabiliti_bot"]["bot_token"]


@SLACK_CLIENT.on(event='message')
async def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'text' in data and 'Hello' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                text=f"Hi <@{user}>!",
                thread_ts=thread_ts
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            # str like 'invalid_auth', 'channel_not_found'
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

@app.on_event('startup')
async def boot_slack():
    SLACK_CLIENT.start(token=slack_token)

@app.on_event('shutdown')
async def shutdown_slack():
    await SLACK_CLIENT.stop()

@app.post('/msg')
async def send_to_slack(slack_message: SlackMessage):
    channel = slack_message.channel
    msg = slack_message.msg
    try:
        response = await SLACK_CLIENT.get("RTMClient")._web_client.chat_postMessage(
            channel=channel,
            text=msg
        )
        assert response["message"]["text"] == msg
        return {}
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        return {}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=int("5000"), log_level="debug")
