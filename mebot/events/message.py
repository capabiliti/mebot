from slack.errors import SlackApiError
from mebot.server import Server
from mebot.data import Data

@Server.SLACK_CLIENT.on(event='message')
async def relay_messages(**payload):
    data = payload['data']
    if 'text' in data and 'bot_id' not in data:
        try:
            dialogue_id = data['thread_ts'] if 'thread_ts' in data else data['ts']
            await Data.update_dialogue(dialogue_id, data['text'])
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")