from flask import Blueprint, jsonify, request

from .services.session_service import (
    create_session,
    get_or_create_setting,
    get_today_stats,
    list_sessions,
    update_setting,
)


api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.get('/settings')
def read_settings():
    setting = get_or_create_setting()
    return jsonify({
        'id': setting.id,
        'work_min': setting.work_min,
        'short_break_min': setting.short_break_min,
        'long_break_min': setting.long_break_min,
        'long_break_interval': setting.long_break_interval,
        'auto_start_next': setting.auto_start_next,
    })


@api_bp.post('/settings')
def write_settings():
    payload = request.get_json(silent=True) or {}
    setting = update_setting(payload)
    return jsonify({
        'id': setting.id,
        'work_min': setting.work_min,
        'short_break_min': setting.short_break_min,
        'long_break_min': setting.long_break_min,
        'long_break_interval': setting.long_break_interval,
        'auto_start_next': setting.auto_start_next,
    })


@api_bp.post('/session')
def write_session():
    payload = request.get_json(silent=True) or {}
    required = ['start_ts', 'end_ts']
    missing = [field for field in required if field not in payload]
    if missing:
        return jsonify({'error': f'missing fields: {", ".join(missing)}'}), 400
    session = create_session(payload)
    return jsonify({
        'id': session.id,
        'start_ts': session.start_ts.isoformat(timespec='seconds'),
        'end_ts': session.end_ts.isoformat(timespec='seconds'),
        'duration_sec': session.duration_sec,
        'kind': session.kind,
    }), 201


@api_bp.get('/stats/today')
def today_stats():
    return jsonify(get_today_stats())


@api_bp.get('/sessions')
def sessions():
    start = request.args.get('from')
    end = request.args.get('to')
    limit = int(request.args.get('limit', 100))
    return jsonify({'items': list_sessions(start=start, end=end, limit=limit)})
