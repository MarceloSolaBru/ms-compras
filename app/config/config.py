import os
from pathlib import Path
from dotenv import load_dotenv


basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-csearch_path=compras_schema"}
    }
    CACHE_REDIS_HOST = os.environ.get('REDIS_HOST')
    CACHE_REDIS_PORT = os.environ.get('REDIS_PORT')
    CACHE_REDIS_DB = os.environ.get('REDIS_DB')
    CACHE_REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-csearch_path=compras_schema"}
    }
    CACHE_REDIS_HOST = os.environ.get('REDIS_HOST')
    CACHE_REDIS_PORT = os.environ.get('REDIS_PORT')
    CACHE_REDIS_DB = os.environ.get('REDIS_DB')
    CACHE_REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_PROD_URL")
    SQLALCHEMY_ENGINE_OPTIONS = os.getenv("SQLALCHEMY_ENGINE_OPTIONS")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-csearch_path=compras_schema"}
    }

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


def factory(app):
    configuation = {
        "development": DevelopmentConfig,
        "testing": TestConfig,
        "production": ProductionConfig,
    }
    return configuation[app]
