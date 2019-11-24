
import datetime
import logging
import monitor.broadcasters
import monitor.dataclasses
import monitor.displays

from typing import Any, Optional, Tuple


_LOGGER = logging.getLogger(__name__)


class AverageLoad(monitor.broadcasters.Consumer):
    def __init__(self,
                 display: monitor.displays.Display,
                 window_size: datetime.timedelta = datetime.timedelta(minutes=2),
                 rps_threshold: int = 10):
        self.__display = display

        self.__start_dt: Optional[float] = None
        self.__current_dt: Optional[float] = None
        self.__previous_dt: float = 0.0

        self.__loads: float = 0.0
        self.__current_value: int = 0
        self.__window_size = float(window_size.seconds)
        self.__rps_threshold = float(rps_threshold)

        self.__ready_to_shoot = False
        self.__upper_threshold = False

    @property
    def ready_to_shoot(self):
        if not self.__ready_to_shoot:
            self.__ready_to_shoot = (self.__current_dt - self.__start_dt) > self.__window_size

        return self.__ready_to_shoot

    @ready_to_shoot.setter
    def ready_to_shoot(self, _: Any):
        raise RuntimeError("read to shoot is read only")

    async def put(self, msg: Tuple[float, monitor.dataclasses.W3CHTTPAccessLog]):
        if self.__current_dt is not None:
            if self.__current_dt < msg[0]:
                self.store_value(self.__previous_dt, self.__current_dt, msg[0])

                self.__current_value = 0
                self.__previous_dt, self.__current_dt = self.__current_dt, msg[0]

            elif self.__current_dt > msg[0]:
                _LOGGER.critical(f'Got message from past: {repr(msg[1])}')
        else:
            self.__start_dt = msg[0]
            self.__previous_dt = msg[0] - 1
            self.__current_dt = msg[0]

        self.__current_value += 1

    def store_value(self, prev_dt: float, current_dt: float, dt: float):
        weight = min((current_dt - prev_dt) / self.__window_size, 1.0)
        self.__loads = (1.0 - weight) * self.__current_value + weight * self.__loads

        if self.ready_to_shoot:
            if self.__loads >= self.__rps_threshold:
                self.__upper_threshold = True

                msg = f'High traffic generated an alert - hits = {int(self.__loads)}, triggered at {int(current_dt)}'
                self.__display.push(msg, tag=monitor.displays.Tags.ALERT)
            elif self.__upper_threshold:
                self.__display.push(f'Alert recovered at {int(current_dt)}', tag=monitor.displays.Tags.NORMAL)
                self.__upper_threshold = False

    def stats(self) -> int:
        return int(self.__loads)
