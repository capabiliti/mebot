from fastapi import FastAPI
from mebot.utils.Singleton import Singleton
from mebot.options import cli_args

class Server(Singleton):
    APP = None
    def __init__(self):
        super().__init__()
        debug = True if cli_args.log_level=="DEBUG" else False
        self.__class__.APP = FastAPI(debug=debug)

Server()