#! /usr/bin/env python
import os
import subprocess
import yaml
import uvicorn

import mebot.routes
from mebot.options import cli_args
from mebot.server import Server
from mebot.slack_clients.Client import Client

app = Server.APP
SLACK_CLIENT = Client("RTMClient")


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
def get_slack_key():
    global SLACK_TOKEN 
    SLACK_TOKEN = yaml.load(subprocess.check_output(
        ["blackbox_cat", "secrets/keys.yaml.gpg"],
        stderr=subprocess.DEVNULL,
        cwd=os.environ["TP_HOME"]), Loader=yaml.FullLoader)["capabiliti_bot"]["bot_token"]

@app.on_event('startup')
async def boot_slack():
    SLACK_CLIENT.start(token=SLACK_TOKEN)

@app.on_event('shutdown')
async def shutdown_slack():
    await SLACK_CLIENT.stop()

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=int("5000"), log_level="debug")
