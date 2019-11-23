import random

import monitor.storages


async def put_messages(storage: monitor.storages.Storage, N: int):
    for _ in range(N):
        await storage.put(random.randint(1, 10))


def test_storages(event_loop):
    storage = monitor.storages.Storage()
    event_loop.run_until_complete(put_messages(storage, 100))

    assert storage.stats()