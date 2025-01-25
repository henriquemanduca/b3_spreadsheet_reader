import json
import os

from datetime import datetime, timedelta


CACHE_FILE = 'cache.json'
CACHE_EXPIRATION_DAYS = 1


class CacheService():
    def __init__(self, reset = False):
        self.__cache = self.__load_from_file()
        self.reset = reset

    def __load_from_file(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def get_value(self, key):
        try:
            value = self.__cache[key]
            if datetime.fromisoformat(value['timestamp']) > datetime.now() - timedelta(days=CACHE_EXPIRATION_DAYS) and self.reset == False:
                return value

            return None
        except KeyError:
            return None

    def set_value(self, key, value):
        self.__cache[key] = value
        self.save()

    def save(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.__cache, f, indent=4)
