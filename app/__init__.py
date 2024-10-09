from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.config import config

# Inicializar la base de datos
db = SQLAlchemy()


def create_app() -> Flask:
    app_context = os.getenv("FLASK_CONTEXT")
    app = Flask(__name__)

    f = config.factory(app_context)
    app.config.from_object(f)
    db.init_app(app)

    from app.routes.compras_routes import compras_bp

    app.register_blueprint(compras_bp, url_prefix="/compras")

    with app.app_context():
        db.create_all()

    return app
