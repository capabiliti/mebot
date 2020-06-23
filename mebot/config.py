import yaml
from collections import namedtuple
from mebot.utils.Singleton import Singleton


class Config(Singleton):

    def __init__(self, config_path):
        super().__init__()
        with open(config_path) as config:
            self._config = yaml.load(config_path, Loader=yaml.FullLoader)
        self.config_tuple = namedtuple('ParsedConfig', sorted(self._config))

    @classmethod
    def get_config(cls):
        return self.config_tuple(cls.instance()._config)
