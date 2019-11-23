import random
import log_generators

import monitor.storages


async def put_messages(storage: monitor.storages.Storage, N: int):
    for i, log in enumerate(log_generators.generate_log()):
        if i >= N:
            break
        await storage.put(log)


def test_storages(event_loop):
    storage = monitor.storages.Storage()
    event_loop.run_until_complete(put_messages(storage, 100))

    assert storage.stats()