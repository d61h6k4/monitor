
import datetime
import monitor.displays
import monitor.storages

from typing import Any


class Differ(object):
    def __init__(self,
                 diff: datetime.timedelta,
                 storage: monitor.storages.Storage,
                 display: monitor.displays.Display,
                 loop: Any):
        self.__diff = diff
        self.__storage = storage
        self.__display = display
        self.__loop = loop

        self.__prev_stats: monitor.storages.Stats = monitor.storages.Stats()
        self.__loop.call_later(self.__diff.seconds, self.snapshot)

    def snapshot(self):
        diff_stats = self.__storage.stats()
        diff_stats.subtract(self.__prev_stats)
        self.__display.push(diff_stats, tag=monitor.displays.Tags.STATS)
        self.__prev_stats.update(diff_stats)
        self.__loop.call_later(self.__diff.seconds, self.snapshot)
