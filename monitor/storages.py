
import collections
import monitor.dataclasses


class Storage(object):
    def __init__(self):
        self.__section_counter = collections.Counter()

    async def put(self, msg: monitor.dataclasses.W3CHTTPAccessLog):
        self.__section_counter.update((msg.request.uri.section, 1))

    def stats(self) -> collections.Counter:
        return self.__section_counter
