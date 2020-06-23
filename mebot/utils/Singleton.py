from mebot.exceptions import MebotException


class Singleton:

    _INSTANCE = None

    def __init__(self):
        if self.__class__._INSTANCE:
            raise MebotException("Singleton class should not be re-initialized.")
        self.__class__._INSTANCE = self

    @classmethod
    def instantiate(cls, *args, **kwargs):
        return cls(*args, **kwargs) if not cls._INSTANCE else cls._INSTANCE

    @classmethod
    def instance(cls):
        return cls._INSTANCE
