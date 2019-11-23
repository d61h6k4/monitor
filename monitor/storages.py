
import collections
import datetime
import monitor.broadcasters
import monitor.dataclasses

from typing import Tuple


Stats = collections.Counter


class Storage(monitor.broadcasters.Consumer):
    def __init__(self):
        self.__section_counter: Stats = collections.Counter()

    async def put(self, msg: Tuple[datetime.datetime, monitor.dataclasses.W3CHTTPAccessLog]):
        self.__section_counter[msg[1].request.uri.section] += 1

    def stats(self) -> Stats:
        return self.__section_counter.copy()
