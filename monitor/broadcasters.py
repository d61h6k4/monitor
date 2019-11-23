
import abc
import asyncio
import monitor.dataclasses

from typing import List


class Consumer(abc.ABC):
    @abc.abstractmethod
    async def put(self, msg: monitor.dataclasses.W3CHTTPAccessLog):
        return


class Broadcaster(object):
    def __init__(self, messages: asyncio.Queue):
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

            for consumer in self.__consumers:
                await consumer.put(msg)
