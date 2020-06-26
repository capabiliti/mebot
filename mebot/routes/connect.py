import json

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from mebot.server import Server

async def process_action(action):
    if action["action"] == "dialogue":
        if "user" in action:
            user_id = Server.SLACK_USERS[action["user"]]
            return await Server.SLACK_CLIENT.send_to_slack(
                user_id = user_id,
                msg = action["msg"],
                thread_id = action.get("dialogue_id", None)
            )
        else:
            return await Server.SLACK_CLIENT.send_to_slack(
                channel = action["channel"],
                msg = action["msg"],
                thread_id = action.get("dialogue_id", None)
            )

@Server.APP.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for action in websocket.iter_json():
            await websocket.send_json(await process_action(action))
    except WebSocketDisconnect:
        pass