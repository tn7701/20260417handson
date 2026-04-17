from pomodoro.services.timer_service import TimerService


class FakeTime:
    def __init__(self, now=0):
        self._t = now

    def now(self):
        return self._t

    def advance(self, s):
        self._t += s


def test_start_and_countdown():
    fake = FakeTime(1000)
    svc = TimerService(1500, now_fn=fake.now)
    assert svc.get_remaining() == 1500
    svc.start()
    fake.advance(60)
    assert svc.get_remaining() == 1440


def test_pause_and_resume():
    fake = FakeTime(2000)
    svc = TimerService(120, now_fn=fake.now)
    svc.start()
    fake.advance(30)
    svc.pause()
    rem_after_pause = svc.get_remaining()
    fake.advance(60)
    assert svc.get_remaining() == rem_after_pause
    svc.resume()
    fake.advance(10)
    assert svc.get_remaining() == rem_after_pause - 10


def test_expire():
    fake = FakeTime(0)
    svc = TimerService(10, now_fn=fake.now)
    svc.start()
    fake.advance(20)
    assert svc.get_remaining() == 0
