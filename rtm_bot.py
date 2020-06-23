#! /usr/bin/env python

import os
import subprocess
import yaml
from slack import RTMClient
from slack.errors import SlackApiError

slack_token = yaml.load(subprocess.check_output(
    ["blackbox_cat", "secrets/keys.yaml.gpg"],
    stderr=subprocess.DEVNULL,
    cwd=os.environ["TP_HOME"]), Loader=yaml.FullLoader)["capabiliti_bot"]["bot_token"]


@RTMClient.run_on(event='message')
def say_hello(**payload):
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


rtm_client = RTMClient(token=slack_token)
print("Starting the client!")
rtm_client.start()
