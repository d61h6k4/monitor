
import abc
import asyncio
import datetime
import monitor.dataclasses

from typing import List, Tuple


class Consumer(abc.ABC):
    @abc.abstractmethod
    async def put(self, msg: Tuple[float, monitor.dataclasses.W3CHTTPAccessLog]):
        return


class Broadcaster(object):
    def __init__(self, messages: asyncio.PriorityQueue):
        self.__messages = messages
        self.__consumers: List[Consumer] = []

    def register_consumer(self, consumer: Consumer):
        self.__consumers.append(consumer)

    async def __call__(self):
        while True:
            try:
                msg = await self.__messages.get()
            except asyncio.CancelledError:
                break
            self.__messages.task_done()

            for consumer in self.__consumers:
                try:
                    await consumer.put(msg)
                except asyncio.CancelledError:
                    break
