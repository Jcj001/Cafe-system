from flask import Flask
from .boundary import boundary


def init_app():
    app = Flask(__name__)

    # APPLICATION CONFIGURATIONS
    app.config['SECRET_KEY'] = "12345678"

    # BLUEPRINTS REGISTRATION
    app.register_blueprint(boundary)

    return app
