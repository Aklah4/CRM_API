from datetime import datetime, timezone

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.users import User
from app.schemas.user_schema import (
    UserRegisterSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserSelfUpdateSchema,
    TokenResponseSchema,
    UserPublicSchema,
    AccessTokenSchema,
)
from app.utils.password import hash_password, verify_password
from app.utils.tokens import issue_tokens, get_current_user


blp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    description='Authentication: register, login, refresh, current user',
)


@blp.route('/register')
class Register(MethodView):

    @blp.arguments(UserRegisterSchema)
    @blp.response(201, TokenResponseSchema)
    def post(self, payload):
        """Register a new user account."""
        if User.query.filter_by(email=payload['email']).first():
            abort(409, message='An account with this email already exists.')

        user = User(
            name=payload['name'],
            email=payload['email'],
            password_hash=hash_password(payload['password']),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message='An account with this email already exists.')

        tokens = issue_tokens(user)
        return {**tokens, 'user': user}


@blp.route('/login')
class Login(MethodView):

    @blp.arguments(UserLoginSchema)
    @blp.response(200, TokenResponseSchema)
    def post(self, payload):
        """Authenticate a user and return access + refresh tokens."""
        user = User.query.filter_by(email=payload['email']).first()

        # Generic message — never reveal which part was wrong
        if not user or not verify_password(payload['password'], user.password_hash):
            abort(401, message='Invalid email or password.')

        if not user.is_active:
            abort(403, message='This account has been deactivated.')

        # Update last login timestamp
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()

        tokens = issue_tokens(user)
        return {**tokens, 'user': user}


@blp.route('/me')
class CurrentUser(MethodView):

    @jwt_required()
    @blp.response(200, UserPublicSchema)
    def get(self):
        """Get the currently authenticated user's profile."""
        user = get_current_user()
        if user is None:
            abort(401, message='User no longer exists.')
        return user
    
    @jwt_required()
    @blp.arguments(UserSelfUpdateSchema)
    @blp.response(200, UserPublicSchema)
    def patch(self, payload):
        """Update the currently authenticated user's profile."""
        user = get_current_user()
        if user is None:
            abort(401, message='User no longer exists.')

        if 'name' in payload:
            user.name = payload['name']

        if 'email' in payload:
            # Check if the new email is already taken by another user
            if payload['email'] != user.email:
                existing = User.query.filter_by(email=payload['email']).first()
                if existing:
                    abort(409, message='An account with this email already exists.')

            user.email = payload['email']

        if 'password' in payload:
            user.password_hash = hash_password(payload['password'])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message='An account with this email already exists.')

        return user


@blp.route('/refresh')
class Refresh(MethodView):

    @jwt_required(refresh=True)
    @blp.response(200, AccessTokenSchema)
    def post(self):
        """Exchange a refresh token for a new access token."""
        user_id = get_jwt_identity()
        existing_claims = get_jwt()
        new_access = create_access_token(
            identity=user_id,
            additional_claims={'role': existing_claims.get('role')},
        )
        return {'access_token': new_access}