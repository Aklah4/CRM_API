from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity )

from app.models.users import User
from app.extensions import db


def issue_tokens(user) -> dict:
    """
    Generate access + refresh tokens for a given user.
    Returns: {'access_token': '...', 'refresh_token': '...'}
    """
    # `identity` is what gets baked into the token's `sub` claim.
    # We use the user's ID as a string — JWT identities should be strings.
    identity = str(user.id)

    # `additional_claims` lets us bake extra context into the token
    # so route handlers don't always need to hit the DB to know the role.
    extra = {'role': user.role}

    access = create_access_token(identity=identity, additional_claims=extra)
    refresh = create_refresh_token(identity=identity, additional_claims=extra)
    return {'access_token': access, 'refresh_token': refresh}

def get_current_user():
    """
    Convenience function to get the current user from the JWT identity.
    Returns a User object or None if not found.
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return db.session.get(User, int(user_id))

