
import datetime
import random
import scipy.stats
import monitor.dataclasses

from typing import Iterator


USERS = ['a', 'b', 'c', 'd']
STATUSES = [200, 301, 404, 500]
METHODS = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']
SECTIONS = ['books', 'photos', 'movies', 'users']


def generate_log(approx_n: int = 100, speed: int = 5) -> Iterator[monitor.dataclasses.W3CHTTPAccessLog]:
    log_per_second_num = scipy.stats.poisson.rvs(speed, size=int(approx_n / speed))
    next_date = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(seconds=10800)))

    for log_num in log_per_second_num:
        for _ in range(int(log_num)):
            authuser = random.choice(USERS)
            method = random.choice(METHODS)
            section = random.choice(SECTIONS)
            uri = monitor.dataclasses.URI(section, f'/{section}/pages')
            request = monitor.dataclasses.Request(method, uri, 'HTTP/1.0')
            status = random.choice(STATUSES)
            size = random.randint(0, 1024)

            yield monitor.dataclasses.W3CHTTPAccessLog('127.0.0.1', '-', authuser, next_date, request, status, size)

        next_date += datetime.timedelta(seconds=1)