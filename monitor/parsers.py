
import asyncio
import logging
import monitor.dataclasses

from typing import Any


_LOGGER = logging.getLogger(__name__)


class Parser(object):
    def __init__(self, raw_strings: asyncio.Queue, access_logs: asyncio.PriorityQueue, loop: Any):
        self.__input = raw_strings
        self.__outputs = access_logs

    async def __call__(self):
        while True:
            try:
                raw_string = await self.__input.get()
            except asyncio.CancelledError:
                break
            try:
                access_log = monitor.dataclasses.W3CHTTPAccessLog.from_string(raw_string)
            except ValueError as e:
                _LOGGER.critical(e)
                continue
            try:
                await self.__outputs.put((access_log.date.timestamp(), access_log))
            except asyncio.CancelledError:
                break
