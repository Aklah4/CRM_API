"""
Role constants used throughout the application.

Single source of truth for role strings. Every place that compares
to a role (decorators, schemas, model defaults, ownership checks)
should import from here — never type the raw string.
"""


class Roles:
    """Allowed user roles, in order of increasing privilege."""
    USER = 'user'
    MANAGER = 'manager'
    ADMIN = 'admin'

    @classmethod
    def all(cls) -> tuple[str, ...]:
        """Return all role values. Used by Marshmallow validators."""
        return (cls.USER, cls.MANAGER, cls.ADMIN)

    @classmethod
    def is_valid(cls, role: str) -> bool:
        """Check if a string is a valid role."""
        return role in cls.all()
