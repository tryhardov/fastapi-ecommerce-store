import uuid
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import TokenCredentialsError

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: uuid.UUID) -> str:
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    }
    encoded_jwt = jwt.encode(payload, settings.secret_key, settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={'require': ['sub', 'exp']}
            )
        user_id = payload.get('sub')

        if not isinstance(user_id, str):
            raise TokenCredentialsError("Invalid 'sub' claim type")
        
        return uuid.UUID(user_id)
        
    except (jwt.InvalidTokenError, ValueError) as exc:
        raise TokenCredentialsError from exc