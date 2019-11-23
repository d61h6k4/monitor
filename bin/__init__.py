
import argparse
import asyncio
import datetime
import logging
import pathlib
import signal

import monitor.broadcasters
import monitor.differs
import monitor.displays
import monitor.log_watchers
import monitor.parsers
import monitor.storages


def parse_args():
    parser = argparse.ArgumentParser(description='HTTP log monitoring console program')

    parser.add_argument('--log-path', help='specify path to log file', default='/tmp/access.log', type=pathlib.Path)

    return parser.parse_args()


def validate_log_path(filepath: pathlib.Path):
    if not filepath.exists():
        raise ValueError(f'{filepath} doesn\'t exists')

    if not filepath.is_file():
        raise ValueError(f'{filepath} is not file')


def setup_signals_handlers(loop):
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, loop.stop)


def main():
    logging.basicConfig(level=logging.DEBUG)

    args = parse_args()
    validate_log_path(args.log_path)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    events = asyncio.Queue(maxsize=1024, loop=loop)
    logs = asyncio.PriorityQueue(maxsize=1024, loop=loop)
    _ = monitor.log_watchers.LogWatcher(args.log_path, events, loop)
    parser = monitor.parsers.Parser(events, logs, loop)

    storage = monitor.storages.Storage()
    broadcaster = monitor.broadcasters.Broadcaster(logs)
    broadcaster.register_consumer(storage)

    out_display = monitor.displays.Display()
    _ = monitor.differs.Differ(datetime.timedelta(seconds=10), storage, out_display, loop)

    parser_task = loop.create_task(parser())
    broadcaster_task = loop.create_task(broadcaster())

    setup_signals_handlers(loop)
    try:
        loop.run_forever()
        for t in [t for t in [parser_task, broadcaster_task] if not (t.done() or t.cancelled())]:
            t.cancel()
            # give canceled tasks the last chance to run
            loop.run_until_complete(t)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
