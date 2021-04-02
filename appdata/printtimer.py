import time


class PrintTimerManager:
    def __init__(self):
        self._timers = []

    def time_left(self):
        if not self._timers:
            return -1
        return self._timers[-1].time_left()

    class PrintTimer:
        def __init__(self, seconds):
            self._start = time.time()
            self._seconds = seconds
            self._finished = self._start + seconds

        def time_left(self):
            return self._finished - time.time()

__INSTANCE = PrintTimerManager()