
import argparse
import pathlib

import monitor


def parse_args():
    parser = argparse.ArgumentParser(description='HTTP log monitoring console program')

    parser.add_argument('--log-path', help='specify path to log file', default='/tmp/access.log', type=pathlib.Path, required=True)

    return parser.parse_args()


def validate_log_path(filepath: pathlib.Path):
    if not filepath.exists():
        raise ValueError(f'{filepath} doesn\'t exists')

    if not filepath.is_file():
        raise ValueError(f'{filepath} is not file')


def main():
    validate_log_path(args.log_path)
    print(f'from main: {monitor.greet(":D")}')


if __name__ == "__main__":
    main()