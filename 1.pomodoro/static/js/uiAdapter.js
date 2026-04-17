import { getSettings, getTodayStats, saveSession } from './api.js';
import { TimerEngine } from './timerEngine.js';

document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('startBtn');
  const resetBtn = document.getElementById('resetBtn');
  const timeEl = document.getElementById('time');
  const statusEl = document.getElementById('status');
  const todayCountEl = document.getElementById('today-count');
  const todayTotalEl = document.getElementById('today-total');
  const circle = document.querySelector('.progress-ring .progress');

  let settings = {
    work_min: 25,
  };

  let lastSavedSignature = '';

  const engine = new TimerEngine(25 * 60, null, async (payload) => {
    try {
      await saveSession({
        start_ts: new Date((payload.startTs || Date.now() / 1000) * 1000).toISOString(),
        end_ts: new Date((payload.endTs || Date.now() / 1000) * 1000).toISOString(),
        duration_sec: payload.durationSec,
        kind: payload.kind,
      });
      await refreshTodayStats();
    } catch (error) {
      console.error('Failed to save session', error);
    }
  });

  const radius = 45;
  const circumference = 2 * Math.PI * radius;

  if (circle) {
    circle.style.strokeDasharray = String(circumference);
    circle.style.strokeDashoffset = String(circumference);
    circle.style.strokeLinecap = 'round';
  }

  let lastSec = null;

  function serializeState() {
    return {
      state: engine.state,
      startTs: engine.startTs,
      endTs: engine.endTs,
      remaining: Math.ceil(engine.getRemaining()),
      durationSec: engine.durationSec,
    };
  }

  function saveTimerState() {
    const snapshot = serializeState();
    const signature = JSON.stringify(snapshot);
    if (signature === lastSavedSignature) {
      return;
    }
    lastSavedSignature = signature;
    localStorage.setItem('pomodoro.timerState', signature);
  }

  function restoreTimerState() {
    const raw = localStorage.getItem('pomodoro.timerState');
    if (!raw) {
      return;
    }
    try {
      const snapshot = JSON.parse(raw);
      engine.hydrate(snapshot);
    } catch (error) {
      console.warn('Failed to restore timer state', error);
    }
  }

  async function refreshTodayStats() {
    try {
      const stats = await getTodayStats();
      if (todayCountEl) {
        todayCountEl.textContent = String(stats.completed ?? 0);
      }
      if (todayTotalEl) {
        todayTotalEl.textContent = `${stats.total_minutes ?? 0}分`;
      }
    } catch (error) {
      console.warn('Failed to load stats', error);
    }
  }

  function applySettingsToUi() {
    const label = document.querySelector('.card-header h2');
    if (label) {
      label.textContent = 'ポモドーロタイマー';
    }
    engine.setDuration((settings.work_min || 25) * 60, false);
    if (engine.state === 'stopped') {
      engine.reset();
    }
  }

  function updateUI() {
    engine.tick();
    const remFloat = engine.getRemaining();
    const remSec = Math.ceil(remFloat);
    if (timeEl && remSec !== lastSec) {
      const mm = Math.floor(remSec / 60).toString().padStart(2, '0');
      const ss = (remSec % 60).toString().padStart(2, '0');
      timeEl.textContent = `${mm}:${ss}`;
      lastSec = remSec;
    }

    if (circle) {
      const progress = Math.max(0, Math.min(1, (engine.durationSec - remFloat) / engine.durationSec));
      const offset = circumference * (1 - progress);
      circle.style.strokeDashoffset = String(offset);
    }

    if (statusEl) {
      statusEl.textContent = engine.isRunning()
        ? '作業中'
        : (engine.state === 'paused' ? '一時停止' : (engine.state === 'completed' ? '完了' : '準備中'));
    }

    if (startBtn) {
      startBtn.textContent = engine.isRunning() ? '一時停止' : '開始';
    }

    saveTimerState();
  }

  function loop() {
    updateUI();
    requestAnimationFrame(loop);
  }

  (async () => {
    restoreTimerState();
    try {
      settings = await getSettings();
      applySettingsToUi();
    } catch (error) {
      console.warn('Failed to load settings', error);
    }
    await refreshTodayStats();
    updateUI();
    loop();
  })();

  startBtn?.addEventListener('click', () => {
    if (!engine.isRunning()) {
      engine.start();
    } else {
      engine.pause();
    }
    updateUI();
  });

  resetBtn?.addEventListener('click', () => {
    engine.reset();
    updateUI();
  });
});
