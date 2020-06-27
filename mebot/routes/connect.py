import json

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from mebot.server import Server
from mebot.data import Data

async def process_action(websocket, action):
    if action["action"] == "dialogue":
        user = channel = None
        if "user" in action:
            user = action["user"]
        else:
            channel = action["channel"]
        response = await Server.SLACK_CLIENT.send_to_slack(
            channel = channel,
            user = user,
            msg = action["msg"],
            thread_id = action.get("dialogue_id", None)
        )
        if "dialogue_id" in response:
            Data.add_dialogue(websocket, response["dialogue_id"])
        return response

@Server.APP.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for action in websocket.iter_json():
            await websocket.send_json(await process_action(websocket, action))
    except WebSocketDisconnect:
        pass