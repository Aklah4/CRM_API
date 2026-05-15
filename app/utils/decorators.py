# This is a custom decorator for authorization checks

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_smorest import abort
from app.utils.roles import Roles


def role_required(*allowed_roles: str):
    """
    Restrict an endpoint to one or more roles.

    Usage:
        @role_required(Roles.ADMIN)
        def get(self): ...

        @role_required(Roles.ADMIN, Roles.MANAGER)
        def post(self): ...

    Must be combined with @jwt_required() — this decorator does NOT
    verify the token itself; it only inspects the role claim.
    """

    if not allowed_roles:
        raise ValueError("role_required must be called with at least one role")

    for role in allowed_roles:
        if not Roles.is_valid(role):
            raise ValueError(f"Invalid role: {role}")

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            if user_role not in allowed_roles:
                abort(403, message='You do not have permission to access this resource.')
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_self_or_admin(target_user_id: int) -> None:
    """
    Enforce that the current request comes from EITHER:
      - The user identified by `target_user_id`, or
      - An admin (regardless of who owns the resource)

    Aborts with 403 if neither condition is met.
    Must be called inside a route protected by @jwt_required().

    Usage:
        def patch(self, user_id):
            user = db.session.get(User, user_id)
            if user is None:
                abort(404, message='User not found.')
            require_self_or_admin(target_user_id=user.id)
            # ... safe to mutate `user` from here
    """
    verify_jwt_in_request()

    current_user_id = int(get_jwt_identity())
    current_role = get_jwt().get('role')

    is_self = current_user_id == target_user_id
    is_admin = current_role == Roles.ADMIN

    if not (is_self or is_admin):
        abort(403, message='You do not have permission to access this resource.')