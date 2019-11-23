
import asyncio
import monitor.dataclasses

from typing import Any


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
            access_log = monitor.dataclasses.W3CHTTPAccessLog.from_string(raw_string)
            await self.__outputs.put((access_log.date.timestamp(), access_log))
