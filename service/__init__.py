from flask_cors import CORS
from flask import Flask
import config

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret
    CORS(app)

    with app.app_context():
        from .history import history

        app.register_blueprint(history)

        return app
