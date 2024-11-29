from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os
from app.config import config, cache_config
from flask_migrate import Migrate

# Inicializar la base de datos
db = SQLAlchemy()
cache = Cache()

def create_app() -> Flask:
    app_context = os.getenv("FLASK_ENV")
    app = Flask(__name__)

    f = config.factory(app_context if app_context else "development")
    app.config.from_object(f)
    db.init_app(app)
    cache.init_app(app, config=cache_config)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    from app.routes.compras_routes import compras_bp

    app.register_blueprint(compras_bp, url_prefix="/compras")

    return app
