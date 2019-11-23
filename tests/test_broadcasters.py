
import asyncio
import random

import monitor.broadcasters
import monitor.dataclasses

from typing import Any, List


class SimpleConsumer(monitor.broadcasters.Consumer):
    def __init__(self):
        self.__storage: List[monitor.dataclasses.W3CHTTPAccessLog] = []

    async def put(self, msg: monitor.dataclasses.W3CHTTPAccessLog):
        self.__storage.append(msg)

    def messages(self) -> List[monitor.dataclasses.W3CHTTPAccessLog]:
        return self.__storage


async def generate_messages(messages: asyncio.Queue):
    for _ in range(100):
        await messages.put(random.randint(1, 10))


def test_broadcaster(event_loop):
    messages = asyncio.Queue(maxsize=1, loop=event_loop)
    first_consumer = SimpleConsumer()
    second_consumer = SimpleConsumer()

    broadcaster = monitor.broadcasters.Broadcaster(messages)
    broadcaster.register_consumer(first_consumer)
    broadcaster.register_consumer(second_consumer)
    broadcaster_task = event_loop.create_task(broadcaster())

    event_loop.run_until_complete(generate_messages(messages))
    broadcaster_task.cancel()

    assert first_consumer.messages() == second_consumer.messages()
