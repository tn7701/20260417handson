from datetime import datetime, timedelta

from pomodoro import create_app


def make_app():
    return create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })


def test_settings_and_session_api_round_trip():
    app = make_app()

    with app.test_client() as client:
        settings_response = client.get('/api/settings')
        assert settings_response.status_code == 200
        assert settings_response.get_json()['work_min'] == 25

        update_response = client.post('/api/settings', json={
            'work_min': 30,
            'short_break_min': 7,
            'auto_start_next': True,
        })
        assert update_response.status_code == 200
        updated = update_response.get_json()
        assert updated['work_min'] == 30
        assert updated['short_break_min'] == 7
        assert updated['auto_start_next'] is True

        start = datetime.utcnow()
        end = start + timedelta(minutes=30)
        session_response = client.post('/api/session', json={
            'start_ts': start.isoformat(),
            'end_ts': end.isoformat(),
            'duration_sec': 1800,
            'kind': 'work',
        })
        assert session_response.status_code == 201

        stats_response = client.get('/api/stats/today')
        assert stats_response.status_code == 200
        stats = stats_response.get_json()
        assert stats['completed'] == 1
        assert stats['total_minutes'] == 30

        sessions_response = client.get('/api/sessions')
        assert sessions_response.status_code == 200
        items = sessions_response.get_json()['items']
        assert len(items) == 1
        assert items[0]['kind'] == 'work'
