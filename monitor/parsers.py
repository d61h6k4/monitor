
import asyncio
import dataclasses

from typing import Any


@dataclasses.dataclass
class HTTPAccessLog(object):
    pass


class ParserAsWorker(object):
    def __init__(self, tasks: asyncio.Queue, solutions: asyncio.Queue, loop: Any):
        pass
