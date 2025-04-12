from flask import Flask
from .routes import routes
from .db import init_db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    init_db()
    return app
