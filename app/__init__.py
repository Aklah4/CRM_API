from flask import Flask
from app.config import config_map
from app.extensions import db, migrate, jwt, api



def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    register_extensions(app)
    register_blueprints(app)


    @app.route('/health')
    def health():
        return{'status': 'ok', 'env': config_name}

    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # Import models so Flask-Migrate can discover them.
    # This must happen AFTER db.init_app() to avoid circular imports.
    from app import models  # noqa: F401


def register_blueprints(app):
    """Register all Blueprints with Flask-Smorest's Api."""
    from app.resources.auth import blp as auth_blp
    from app.resources.users import blp as admin_users_blp, blp_users

    api.register_blueprint(auth_blp)
    api.register_blueprint(blp_users)
    api.register_blueprint(admin_users_blp)

    
