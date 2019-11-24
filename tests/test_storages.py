import log_generators
import monitor.storages


async def put_messages(storage: monitor.storages.Storage, N: int):
    for log in log_generators.generate_log(N, 3):
        await storage.put((log.date.timestamp(), log))


def test_storages(event_loop):
    N = 1024
    storage = monitor.storages.Storage()
    event_loop.run_until_complete(put_messages(storage, N))

    assert len(storage.stats().stats()) > 0
