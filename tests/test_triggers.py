import log_generators

import monitor.triggers


class DisplayMock(object):
    def __init__(self):
        self.messages = []

    def push(self, msg, **kwargs):
        self.messages.append(msg)


async def put_messages(average_load: monitor.triggers.AverageLoad, N: int):
    for log in log_generators.generate_log(N, speed=9):
        await average_load.put((log.date, log))


def test_storages_get_alerts(event_loop):
    N = 10240

    display = DisplayMock()
    average_load = monitor.triggers.AverageLoad(display)
    event_loop.run_until_complete(put_messages(average_load, N))

    assert len(display.messages) > 0


def test_storages_no_alert(event_loop):
    N = 10240

    display = DisplayMock()
    average_load = monitor.triggers.AverageLoad(display, rps_threshold=100)
    event_loop.run_until_complete(put_messages(average_load, N))

    assert len(display.messages) == 0
