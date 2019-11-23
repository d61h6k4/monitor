
import asyncio


class Display(object):
    def __init__(self, source_queue: asyncio.Queue):
        self.__source_queue = source_queue

    async def __call__(self):
        while True:
            try:
                msg = await self.__source_queue.get()
            except asyncio.CancelledError:
                break
            print(msg)
            self.__source_queue.task_done()

    def __del__(self):
        self.__source_queue.task_done()
