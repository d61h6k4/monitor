
import collections
import monitor.broadcasters
import monitor.dataclasses

from typing import List, Tuple


class Stats(object):
    def __init__(self):
        self.__section_counter = collections.Counter()
        self.__user_counter = collections.Counter()
        self.__method_counter = collections.Counter()

    def update_section(self, section: str):
        self.__section_counter[section] += 1

    def update_user(self, user: str):
        self.__user_counter[user] += 1

    def update_method(self, method: str):
        self.__method_counter[method] += 1

    def copy(self) -> 'Stats':
        new_stats = Stats()
        new_stats.__section_counter = self.__section_counter.copy()
        new_stats.__user_counter = self.__user_counter.copy()
        new_stats.__method_counter = self.__method_counter.copy()

        return new_stats

    def subtract(self, other: 'Stats'):
        self.__section_counter.subtract(other.__section_counter)
        self.__user_counter.subtract(other.__user_counter)
        self.__method_counter.subtract(other.__method_counter)

    def update(self, other: 'Stats'):
        self.__section_counter.update(other.__section_counter)
        self.__user_counter.update(other.__user_counter)
        self.__method_counter.update(other.__method_counter)

    def section_stats(self, most_common: int = 3) -> List[Tuple[str, int]]:
        return self.__section_counter.most_common(most_common)

    def user_stats(self, most_common: int = 3) -> List[Tuple[str, int]]:
        return self.__user_counter.most_common(most_common)

    def method_stats(self, most_common: int = 3) -> List[Tuple[str, int]]:
        return self.__method_counter.most_common(most_common)

    def stats(self, most_common: int = 3) -> List[Tuple[str, int]]:
        return self.section_stats(most_common) + self.user_stats(most_common) + self.method_stats(most_common)


class Storage(monitor.broadcasters.Consumer):
    def __init__(self):
        self.__stats: Stats = Stats()

    async def put(self, msg: Tuple[float, monitor.dataclasses.W3CHTTPAccessLog]):
        self.__stats.update_section(msg[1].request.uri.section)
        self.__stats.update_user(msg[1].authuser)
        self.__stats.update_method(msg[1].request.method)

    def stats(self) -> Stats:
        return self.__stats.copy()
