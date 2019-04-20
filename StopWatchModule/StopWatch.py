import time

class StopWatch:
    def __init__(self):
        self._t0=time.time()

    def getSeconds(self):
        return time.time()-self._t0
