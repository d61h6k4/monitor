
import monitor.dataclasses


class Storage(object):
    def __init__(self):
        self.__storage = []

    async def put(self, msg: monitor.dataclasses.W3CHTTPAccessLog):
        self.__storage.append(msg)

    def stats(self) -> int:
        return 1
