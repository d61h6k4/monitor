
import asyncio
import logging
import pathlib

from typing import Any


_LOGGER = logging.getLogger(__name__)


class LogWatcher(object):
    def __init__(self, log_file: pathlib.Path, events_sink: asyncio.Queue, loop: Any):
        self.__loop = loop
        self.__events_sink = events_sink
        self.__source = open(log_file, 'r')

        self.read_next_lines()
        self.__loop.add_reader(self.__source, self.read_next_lines)

    def read_next_lines(self):
        for line in self.__source:
            try:
                self.__events_sink.put_nowait(line.strip())
            except asyncio.QueueFull:
                _LOGGER.critical("Events queue is full")

    def __del__(self):
        self.__loop.remove_reader(self.__source)
