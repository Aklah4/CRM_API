import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Returns a string suitable for storing in the password_hash column.
    """
    if not plain_password:
        raise ValueError("Password cannot be empty")

    # bcrypt works in bytes, so encode/decode at the boundaries
    hashed_bytes = bcrypt.hashpw(
        plain_password.encode('utf-8'),
        bcrypt.gensalt(rounds=12),
    )
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Check a plaintext password against a stored hash.
    Returns True if they match, False otherwise.
    """
    if not plain_password or not password_hash:
        return False

    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            password_hash.encode('utf-8'),
        )
    except (ValueError, TypeError):
        # Malformed hash in the DB — treat as no match
        return False