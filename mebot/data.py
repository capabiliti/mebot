from mebot.exceptions.MebotException import MebotException
from mebot.utils.Singleton import Singleton

class Data(Singleton):
    _WEBSOCKETS = {}
    _DISABLED_SOCKETS = []
    _SLACK_USERS = {}
    
    @classmethod
    def add_dialogue(cls, websocket, dialogue_id):
        cls._WEBSOCKETS[dialogue_id] = websocket

    @classmethod
    async def update_dialogue(cls, dialogue_id, msg, key="msg"):
        if dialogue_id not in cls._WEBSOCKETS: return
        if cls._WEBSOCKETS[dialogue_id] not in cls._DISABLED_SOCKETS:
            await cls._WEBSOCKETS[dialogue_id].send_json({
                "dialogue_id": dialogue_id,
                key: msg
            })
        else:
            del cls._WEBSOCKETS[dialogue_id]
    
    @classmethod
    def remove_websocket(cls, websocket):
        cls._DISABLED_SOCKETS.append(websocket)

    @classmethod
    def add_users(cls, slack_users):
        cls._SLACK_USERS.update(slack_users)

    @classmethod
    def get_user_id(cls, username):
        try:
            return cls._SLACK_USERS[username]
        except KeyError:
            raise MebotException(f"{username} not found in database!")