from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.config import config
from flask_migrate import Migrate

# Inicializar la base de datos
db = SQLAlchemy()


def create_app() -> Flask:
    app_context = os.getenv("FLASK_ENV")
    app = Flask(__name__)

    f = config.factory(app_context if app_context else "development")
    app.config.from_object(f)
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    from app.routes.compras_routes import compras_bp

    app.register_blueprint(compras_bp, url_prefix="/compras")

    return app
