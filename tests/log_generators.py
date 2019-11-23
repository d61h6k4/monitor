
import datetime
import random
import monitor.dataclasses

from typing import Generator


USERS = ['a', 'b', 'c', 'd']
STATUSES = [200, 301, 404, 500]
METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']
SECTIONS = ['books', 'photos', 'movies', 'users']


def generate_log() -> Generator[monitor.dataclasses.W3CHTTPAccessLog, None, None]:
    next_date = datetime.datetime.now()
    while True:
        authuser = random.choice(USERS)
        next_date += datetime.timedelta(seconds=random.randint(0, 2))
        method = random.choice(METHODS)
        section = random.choice(SECTIONS)
        uri = monitor.dataclasses.URI(section, f'/{section}/pages')
        request = monitor.dataclasses.Request(method, uri, 'HTTP/1.0')
        status = random.choice(STATUSES)
        size = random.randint(0, 1024)
        yield monitor.dataclasses.W3CHTTPAccessLog('127.0.0.1', '-', authuser, next_date, request, status, size)