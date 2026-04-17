from datetime import datetime

from .extensions import db


class PomodoroSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_ts = db.Column(db.DateTime, nullable=False)
    end_ts = db.Column(db.DateTime, nullable=False)
    duration_sec = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.String(32), nullable=False, default='work')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class AppSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_min = db.Column(db.Integer, nullable=False, default=25)
    short_break_min = db.Column(db.Integer, nullable=False, default=5)
    long_break_min = db.Column(db.Integer, nullable=False, default=15)
    long_break_interval = db.Column(db.Integer, nullable=False, default=4)
    auto_start_next = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


def get_default_setting():
    return {
        'work_min': 25,
        'short_break_min': 5,
        'long_break_min': 15,
        'long_break_interval': 4,
        'auto_start_next': False,
    }
