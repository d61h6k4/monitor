
import asyncio

import monitor.parsers as parsers


LOG_LINES = [
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123',
    '127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
    '127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 200 34',
    '127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 503 12',
]


async def set_tasks(tasks: asyncio.Queue):
    for log_line in LOG_LINES:
        await tasks.put(log_line)


def test_parser(event_loop):
    tasks = asyncio.Queue(maxsize=4, loop=event_loop)
    solutions = asyncio.Queue(maxsize=len(LOG_LINES), loop=event_loop)

    parser = parsers.Parser(tasks, solutions, event_loop)
    parser_task = event_loop.create_task(parser())

    event_loop.run_until_complete(set_tasks(tasks))
    parser_task.cancel()

    assert solutions.qsize() == len(LOG_LINES)
