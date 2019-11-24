
import asyncio
import logging
import pathlib

from typing import Any, List


_LOGGER = logging.getLogger(__name__)


class LogWatcher(object):
    def __init__(self, log_file: pathlib.Path, events_sink: asyncio.Queue, loop: Any):
        self.__loop = loop
        self.__events_sink = events_sink
        self.__source = open(log_file, 'r')
        self.__buffer: List[str] = []

        self.read_next_lines()
        self.__loop.add_reader(self.__source, self.read_next_lines)

    def read_next_lines(self):
        if self.__buffer:
            for i, line in enumerate(self.__buffer):
                try:
                    self.__events_sink.put_nowait(line.strip())
                except asyncio.QueueFull:
                    _LOGGER.warn("Events queue is full")
                    self.__buffer = self.__buffer[i:]
                    self.__loop.call_later(1, self.read_next_lines)
                    return
            self.__buffer = []

        for line in self.__source:
            try:
                self.__events_sink.put_nowait(line.strip())
            except asyncio.QueueFull:
                _LOGGER.warn("Events queue is full")
                self.__buffer.append(line)
                self.__loop.call_soon(self.read_next_lines)
                return

    def __del__(self):
        self.__loop.remove_reader(self.__source)
