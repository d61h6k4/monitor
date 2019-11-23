
import argparse
import asyncio
import pathlib
import signal

import monitor.log_watchers as log_watchers
import monitor.displays as displays


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
    args = parse_args()
    validate_log_path(args.log_path)

    loop = asyncio.get_event_loop()

    events_sink = asyncio.Queue(maxsize=1024, loop=loop)
    _ = log_watchers.LogWatcher(args.log_path, events_sink, loop)
    out_display = displays.Display(events_sink)

    display_task = loop.create_task(out_display())

    setup_signals_handlers(loop)
    try:
        loop.run_forever()
    finally:
        display_task.cancel()
        loop.close()


if __name__ == "__main__":
    main()
