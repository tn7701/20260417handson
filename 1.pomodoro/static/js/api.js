async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }
  return response.json();
}

export function getSettings() {
  return requestJson('/api/settings');
}

export function saveSettings(payload) {
  return requestJson('/api/settings', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function saveSession(payload) {
  return requestJson('/api/session', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getTodayStats() {
  return requestJson('/api/stats/today');
}

export function getSessions(query = '') {
  const suffix = query ? `?${query}` : '';
  return requestJson(`/api/sessions${suffix}`);
}
