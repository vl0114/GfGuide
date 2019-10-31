data = dict()


class Caching:
    @staticmethod
    def save(key: str, obj):
        data[key] = obj

    @staticmethod
    def get(key: str):
        return data[key]

    @staticmethod
    def rm(key: str):
        data.pop(key)