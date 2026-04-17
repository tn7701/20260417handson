import time


class TimerService:
    """Pure timer logic with injectable time provider (seconds).

    - duration_sec: total duration in seconds
    - now_fn: callable returning current time in seconds
    """

    def __init__(self, duration_sec, now_fn=None):
        self.duration_sec = int(duration_sec)
        self.now = now_fn or (lambda: int(time.time()))
        self.state = 'stopped'
        self.start_ts = None
        self.end_ts = None
        self.remaining = self.duration_sec

    def start(self):
        if self.state == 'running':
            return
        now = int(self.now())
        self.start_ts = now
        self.end_ts = now + self.remaining
        self.state = 'running'

    def pause(self):
        if self.state != 'running':
            return
        now = int(self.now())
        self.remaining = max(0, self.end_ts - now)
        self.state = 'paused'

    def resume(self):
        if self.state != 'paused':
            return
        now = int(self.now())
        self.end_ts = now + self.remaining
        self.state = 'running'

    def reset(self):
        self.state = 'stopped'
        self.start_ts = None
        self.end_ts = None
        self.remaining = self.duration_sec

    def get_remaining(self):
        if self.state == 'running':
            return max(0, int(self.end_ts - int(self.now())))
        return int(self.remaining)

    def is_running(self):
        return self.state == 'running'
