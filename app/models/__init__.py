# app/models/__init__.py
"""
Import all models here so SQLAlchemy and Flask-Migrate can discover them.
Every new model file must be imported in this file.
"""
from app.models.users import User  # noqa: F401
