// Pure timer engine module (no DOM)
export class TimerEngine {
  constructor(durationSec, nowFn = null, onComplete = null) {
    this.durationSec = Number(durationSec);
    this.now = nowFn || (() => Date.now() / 1000);
    this.onComplete = onComplete;
    this.state = 'stopped';
    this.startTs = null;
    this.endTs = null;
    this.remaining = this.durationSec;
  }

  setDuration(durationSec, resetRemaining = true) {
    this.durationSec = Number(durationSec);
    if (resetRemaining || this.state === 'stopped') {
      this.remaining = this.durationSec;
    }
  }

  hydrate(snapshot) {
    if (!snapshot) return;
    if (snapshot.durationSec) {
      this.durationSec = Number(snapshot.durationSec);
    }
    this.state = snapshot.state || 'stopped';
    this.startTs = snapshot.startTs ?? null;
    this.endTs = snapshot.endTs ?? null;
    this.remaining = Number(snapshot.remaining ?? this.durationSec);
    if (this.state === 'running' && this.endTs != null) {
      const remaining = this.endTs - this.now();
      if (remaining <= 0) {
        this.complete();
      } else {
        this.remaining = remaining;
      }
    }
  }

  start() {
    if (this.state === 'running') return;
    if (this.state === 'completed' && this.remaining <= 0) {
      this.remaining = this.durationSec;
    }
    const now = this.now();
    this.startTs = now;
    this.endTs = now + this.remaining;
    this.state = 'running';
  }

  pause() {
    if (this.state !== 'running') return;
    const now = this.now();
    this.remaining = Math.max(0, this.endTs - now);
    this.state = 'paused';
  }

  resume() {
    if (this.state !== 'paused') return;
    const now = this.now();
    this.endTs = now + this.remaining;
    this.state = 'running';
  }

  reset() {
    this.state = 'stopped';
    this.startTs = null;
    this.endTs = null;
    this.remaining = this.durationSec;
  }

  complete() {
    if (this.state === 'completed') {
      return;
    }
    this.state = 'completed';
    this.remaining = 0;
    if (typeof this.onComplete === 'function') {
      this.onComplete({
        startTs: this.startTs,
        endTs: this.endTs,
        durationSec: this.durationSec,
        kind: 'work',
      });
    }
  }

  tick() {
    if (this.state !== 'running') {
      return false;
    }
    if (this.now() >= this.endTs) {
      this.complete();
      return true;
    }
    return false;
  }

  getRemaining() {
    if (this.state === 'running') {
      const remaining = this.endTs - this.now();
      if (remaining <= 0) {
        return 0;
      }
      return remaining;
    }
    return this.remaining;
  }

  getRemainingSec() {
    return Math.ceil(this.getRemaining());
  }

  isRunning() {
    return this.state === 'running';
  }
}
