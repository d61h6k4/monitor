
import asyncio
import random

import monitor.broadcasters as boradcasters

from typing import Any, List


class TestConsumer(broadcasters.Consumer):
    def __init__(self):
        self.__storage: List[Any] = []

    async def get(self, msg: Any):
        self.__storage.append(msg)

    def messages(self) -> List[Any]:
        return self.__storage


async def generate_messages(messages: asyncio.Queue):
    for _ in range(100):
        await messages.put(random.randint(1, 10))


def test_broadcaster(event_loop):
    messages = asyncio.Queue(maxsize=1, loop=event_loop)
    first_consumer = TestConsumer()
    second_consumer = TestConsumer()

    broadcaster = broadcaster.Broadvaster(messages, loop=event_loop)
    broadcaster.add_consumer(first_consumer, second_consumer)

    event_loop.run_until_complete(generate_messages(messages))

    assert first_consumer.messages() == second_consumer.messages()
