from flask import Flask 
from app.config import config_map
from app.extensions import db, migrate



def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    register_extensions(app)


    @app.route('/health')
    def health():
        return{'status': 'ok', 'env': config_name}

    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can discover them.
    # This must happen AFTER db.init_app() to avoid circular imports.
    from app import models  # noqa: F401