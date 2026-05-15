# Admin-only user management is on blp (/admin/users).
# Self-or-admin user management is on blp_users (/users).

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from app.extensions import db
from app.models.users import User
from app.schemas.user_schema import (
    UserAdminSchema,
    UserSelfUpdateSchema,
    UserAdminUpdateSchema,
)
from app.utils.roles import Roles
from app.utils.decorators import role_required, require_self_or_admin
from app.utils.password import hash_password


# ── /users — self-or-admin ────────────────────────────────────────────────────

blp_users = Blueprint(
    'users', __name__,
    url_prefix='/users',
    description='User self-service endpoints (self or admin)',
)


@blp_users.route('/<int:user_id>')
class UserDetail(MethodView):
    @jwt_required()
    @blp_users.arguments(UserSelfUpdateSchema)
    @blp_users.response(200, UserAdminSchema)
    def patch(self, update_data, user_id):
        """Update your own profile (admins may update any user)"""
        user = db.session.get(User, user_id)
        if not user:
            abort(404, message='User not found')

        require_self_or_admin(user_id)

        if 'name' in update_data:
            user.name = update_data['name']

        if 'email' in update_data:
            conflict = User.query.filter_by(email=update_data['email']).first()
            if conflict and conflict.id != user_id:
                abort(409, message='Email already in use')
            user.email = update_data['email']

        if 'password' in update_data:
            user.password_hash = hash_password(update_data['password'])

        db.session.commit()
        return user


# ── /admin/users — admin only ─────────────────────────────────────────────────

blp = Blueprint(
    'admin_users', __name__,
    url_prefix='/admin/users',
    description='Admin-only endpoints for user management',
)


@blp.route('/')
class AdminUserList(MethodView):
    @jwt_required()
    @role_required(Roles.ADMIN)
    @blp.response(200, UserAdminSchema(many=True))
    def get(self):
        """Get a list of all users (Admin only)"""
        return User.query.all()


@blp.route('/<int:user_id>')
class AdminUserDetail(MethodView):
    @jwt_required()
    @role_required(Roles.ADMIN)
    @blp.response(200, UserAdminSchema)
    def get(self, user_id):
        """Get details of a specific user by ID (Admin only)"""
        user = db.session.get(User, user_id)
        if not user:
            abort(404, message='User not found')
        return user

    @jwt_required()
    @role_required(Roles.ADMIN)
    @blp.arguments(UserAdminUpdateSchema)
    @blp.response(200, UserAdminSchema)
    def patch(self, update_data, user_id):
        """Update any user's fields including role and active status (Admin only)"""
        user = db.session.get(User, user_id)
        if not user:
            abort(404, message='User not found')

        if 'name' in update_data:
            user.name = update_data['name']

        if 'email' in update_data:
            conflict = User.query.filter_by(email=update_data['email']).first()
            if conflict and conflict.id != user_id:
                abort(409, message='Email already in use')
            user.email = update_data['email']

        if 'role' in update_data:
            user.role = update_data['role']

        if 'is_active' in update_data:
            user.is_active = update_data['is_active']

        db.session.commit()
        return user
