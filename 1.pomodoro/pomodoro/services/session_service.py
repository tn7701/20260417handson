from datetime import datetime, timedelta

from ..extensions import db
from ..models import AppSetting, PomodoroSession, get_default_setting


def _to_naive_datetime(value):
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(value)
    if isinstance(value, str):
        normalized = value.replace('Z', '+00:00')
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=None)
    raise ValueError('Unsupported datetime value')


def _serialize_datetime(value):
    return value.isoformat(timespec='seconds')


def get_or_create_setting():
    setting = db.session.get(AppSetting, 1)
    if setting is None:
        setting = AppSetting(id=1, **get_default_setting())
        db.session.add(setting)
        db.session.commit()
    return setting


def update_setting(payload):
    setting = get_or_create_setting()
    for key in get_default_setting().keys():
        if key in payload:
            setattr(setting, key, payload[key])
    db.session.commit()
    return setting


def create_session(payload):
    start_ts = _to_naive_datetime(payload['start_ts'])
    end_ts = _to_naive_datetime(payload['end_ts'])
    duration_sec = int(payload.get('duration_sec') or max(0, (end_ts - start_ts).total_seconds()))
    kind = payload.get('kind', 'work')
    session = PomodoroSession(
        start_ts=start_ts,
        end_ts=end_ts,
        duration_sec=duration_sec,
        kind=kind,
    )
    db.session.add(session)
    db.session.commit()
    return session


def get_today_stats(now=None):
    now = now or datetime.utcnow()
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)
    sessions = PomodoroSession.query.filter(
        PomodoroSession.end_ts >= start,
        PomodoroSession.end_ts < end,
        PomodoroSession.kind == 'work',
    ).all()
    total_seconds = sum(session.duration_sec for session in sessions)
    return {
        'date': start.date().isoformat(),
        'completed': len(sessions),
        'total_minutes': total_seconds // 60,
        'total_seconds': total_seconds,
    }


def list_sessions(start=None, end=None, limit=100):
    query = PomodoroSession.query.order_by(PomodoroSession.end_ts.desc())
    if start is not None:
        query = query.filter(PomodoroSession.end_ts >= _to_naive_datetime(start))
    if end is not None:
        query = query.filter(PomodoroSession.end_ts < _to_naive_datetime(end))
    items = query.limit(limit).all()
    return [
        {
            'id': item.id,
            'start_ts': _serialize_datetime(item.start_ts),
            'end_ts': _serialize_datetime(item.end_ts),
            'duration_sec': item.duration_sec,
            'kind': item.kind,
            'created_at': _serialize_datetime(item.created_at),
        }
        for item in items
    ]
