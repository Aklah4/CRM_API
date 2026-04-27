import os                          # gives access to environment variables and OS-level settings
from datetime import timedelta     # used to express token expiry as a duration (e.g. 15 minutes)
from dotenv import load_dotenv     # reads a .env file and loads its key=value pairs into os.environ

load_dotenv()                      # actually runs the .env load — must be called before any os.getenv()


class Config:
    """Base config — settings shared across all environments."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-fallback-change-me')
    # Flask uses SECRET_KEY to sign cookies and sessions; reads from .env, falls back to a placeholder

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-fallback-change-me')
    # Flask-JWT-Extended uses this to sign/verify JWT tokens; separate from SECRET_KEY by convention

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    # Access tokens expire after 15 minutes — short-lived for security

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    # Refresh tokens last 7 days — used to issue new access tokens without re-login

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Disables SQLAlchemy's event system for model changes; not needed and causes a deprecation warning


class DevelopmentConfig(Config):          # inherits all settings from Config
    DEBUG = True                          # enables Flask's debugger and auto-reloader in dev

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        # builds a MySQL connection string using PyMySQL as the driver; credentials from .env
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        # appends host, port, and database name — all pulled from .env
    )


class TestingConfig(Config):              # inherits all settings from Config
    TESTING = True                        # tells Flask/extensions that tests are running
    DEBUG = True                          # keeps debug mode on so errors surface clearly in tests

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # uses an in-memory SQLite DB for tests — fast, disposable, no setup required


class ProductionConfig(Config):           # inherits all settings from Config
    DEBUG = False                         # disables the debugger in production — never expose it publicly

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # full DB URL comes entirely from the environment in production (no hardcoded fallback)


config_map = {
    'development': DevelopmentConfig,     # selected when FLASK_ENV=development
    'testing':     TestingConfig,         # selected when FLASK_ENV=testing
    'production':  ProductionConfig,      # selected when FLASK_ENV=production
}
# config_map lets the app factory do: app.config.from_object(config_map[env])
