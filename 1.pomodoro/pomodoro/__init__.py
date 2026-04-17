import os

from flask import Flask, render_template

from .extensions import db
from .routes import api_bp


def create_app(test_config=None):
    pkg_dir = os.path.dirname(__file__)
    template_folder = os.path.join(pkg_dir, '..', 'templates')
    static_folder = os.path.join(pkg_dir, '..', 'static')
    instance_dir = os.path.join(pkg_dir, '..', 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(instance_dir, 'pomodoro.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
