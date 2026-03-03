from flask import Flask, redirect, url_for
from app.config import get_config
from app.models.base import init_db


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    init_db(app)
    register_modules(app)

    @app.route('/')
    def index():
        return redirect(url_for('chat.chat_page'))

    return app


def register_modules(app):
    from app.modules.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    app.config['REGISTERED_MODULES'] = [
        {'name': 'Chat', 'icon': '💬', 'url': '/chat', 'id': 'chat'}
    ]
