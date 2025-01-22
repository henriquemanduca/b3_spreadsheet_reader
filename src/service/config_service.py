import json
import os


CONFIG_FILE = 'configuration.json'


def empty_config():
    return {
        'altered_tickers': {},
        'skip': [],
        'unfolds': {}
    }


class ConfigService():
    def __init__(self):
        self.__config = self.__load_configuration_from_file()

    def __load_configuration_from_file(self):
        if not os.path.exists(CONFIG_FILE):
            return empty_config()

        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return empty_config()

    def get_unfold_factor(self, ticker):
        try:
            return self.__config['unfolds'][ticker]
        except Exception:
            return None

    def get_altered_ticker(self, ticker):
        try:
            return self.__config['altered_tickers'][ticker]
        except Exception:
            return None

    def get_tickers_to_skip(self,):
        return self.__config['skip']


