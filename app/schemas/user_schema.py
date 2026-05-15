from marshmallow import Schema, fields, validate

from app.utils.roles import Roles


class UserRegisterSchema(Schema):
    """Validates input when a new user signs up."""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )


class UserLoginSchema(Schema):
    """Validates input when a user logs in."""
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)




class UserSelfUpdateSchema(Schema):
    """
    Validates input when a user updates their OWN profile.
    Note: no role/is_active here — users can't change their own role/status.
    """
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    password = fields.Str(
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )


class UserAdminUpdateSchema(Schema):
    """
    Validates input when an admin updates another user.
    Admins CAN change role and is_active.
    """
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    role = fields.Str(validate=validate.OneOf(Roles.all()))
    is_active = fields.Bool()


# ──────────────────────────────────────────────────────────
# Output schemas
# ──────────────────────────────────────────────────────────

class UserPublicSchema(Schema):
    """
    Public-facing user data. Returned to the user about themselves
    (/auth/me) and embedded inside other public responses.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    role = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class UserAdminSchema(UserPublicSchema):
    """
    Admin-facing user data. Includes everything in UserPublicSchema
    plus operational fields that admins care about.
    """
    is_active = fields.Bool()
    updated_at = fields.DateTime(dump_only=True)
    last_login_at = fields.DateTime(dump_only=True, allow_none=True)



class UserResponseSchema(Schema):
    """Serializes a User model to JSON for responses. NEVER includes password_hash."""
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    role = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login_at = fields.DateTime(dump_only=True, allow_none=True)


class TokenResponseSchema(Schema):
    """The shape of /auth/login and /auth/register responses."""
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserResponseSchema)


class AccessTokenSchema(Schema):
    """The shape of /auth/refresh responses."""
    access_token = fields.Str()