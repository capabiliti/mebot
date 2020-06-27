import os
import subprocess
import yaml

from fastapi import FastAPI
from mebot.utils.Singleton import Singleton
from mebot.slack_clients.Client import Client
from mebot.data import Data
# from mebot.options import cli_args


class Server(Singleton):
    APP = None
    SLACK_CLIENT = None
    SLACK_TOKEN = None

    def __init__(self):
        super().__init__()
        # debug = True if cli_args.log_level=="DEBUG" else False
        debug = False
        self.__class__.APP = FastAPI(debug=debug)
        self.__class__.SLACK_CLIENT = Client("RTMClient")


app = Server().APP


@app.on_event('startup')
def get_slack_key():
    Server.SLACK_TOKEN = yaml.load(subprocess.check_output(
        ["blackbox_cat", "secrets/keys.yaml.gpg"],
        stderr=subprocess.DEVNULL,
        cwd=os.environ["TP_HOME"]), Loader=yaml.FullLoader)["capabiliti_bot"]["bot_token"]


@app.on_event('startup')
async def boot_slack():
    Server.SLACK_CLIENT.start(token=Server.SLACK_TOKEN)
    for response in await Server.SLACK_CLIENT.get("RTMClient")._web_client.users_list(limit=0):
        Data.add_users(
            {member["profile"]["display_name"]: member["id"] for member in response["members"]})


@app.on_event('shutdown')
async def shutdown_slack():
    await Server.SLACK_CLIENT.stop()
