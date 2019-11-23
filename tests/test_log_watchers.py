
import asyncio
import pathlib
import tempfile
import random

import monitor.log_watchers as log_watchers


LOG_LINE='127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123'


async def write_logs(log_path: pathlib.Path, num_times: int):
    with open(log_path, 'a') as sink:
        for _ in range(num_times):
            sink.write(f'{LOG_LINE}\n')


def test_log_watcher(event_loop):
    N = 512
    events_sink = asyncio.Queue(maxsize=2 * N, loop=event_loop)

    with tempfile.TemporaryDirectory() as tmpdirname:
        log_path = pathlib.Path(tmpdirname) / 'access.log'
        with open(log_path, 'w') as sink:
            for _ in range(N):
                sink.write(f'{LOG_LINE}\n')

        log_watcher = log_watchers.LogWatcher(log_path, events_sink, event_loop)
        event_loop.run_until_complete(write_logs(log_path, N))

    assert not events_sink.empty()
    assert events_sink.qsize() == 2 * N
    for _ in range(2 * N):
        event = events_sink.get_nowait()
        events_sink.task_done()

        assert event == LOG_LINE
