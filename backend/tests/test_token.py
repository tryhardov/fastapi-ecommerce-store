import uuid
from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.core.config import settings
from app.core.exceptions import TokenCredentialsError
from app.core.security import create_access_token, decode_access_token


def test_decode_returns_original_user_id():
    user_id = uuid.uuid4()
    token = create_access_token(user_id)

    result = decode_access_token(token)

    assert result == user_id


def test_tampered_signature_is_rejected():
    user_id = uuid.uuid4()
    token = create_access_token(user_id)

    parts = token.split('.')

    assert len(parts) == 3

    header, payload, signature = parts
    middle_index = len(signature) // 2

    char_for_change = signature[middle_index]
    new_char = 'B' if char_for_change != 'B' else 'A'

    tampered_signature = signature[:middle_index] + new_char + signature[middle_index + 1:]
    tampered_token = '.'.join([header, payload, tampered_signature])

    with pytest.raises(TokenCredentialsError):
        decode_access_token(tampered_token)



def make_token(payload: dict, key: str | None = None) -> str:
    if key is None:
        key = settings.secret_key
    return jwt.encode(payload, key, settings.algorithm)


def minutes_for_payload(minutes: int) -> datetime:
    return datetime.now(UTC) + timedelta(minutes=minutes)


@pytest.mark.parametrize(
    'bad_token',
    [
        pytest.param(
            make_token({'sub': str(uuid.uuid4()), 'exp': minutes_for_payload(-5)}),
            id='expired'
        ),
        pytest.param(
            make_token({'sub': str(uuid.uuid4())}),
            id='no_exp'
        ),
        pytest.param(
            make_token({'exp': minutes_for_payload(30)}),
            id='no_sub'
        ),
        pytest.param(
            make_token({'sub': 'abc', 'exp': minutes_for_payload(30)}),
            id='sub_not_uuid'
        ),
        pytest.param(
            make_token({'sub': 123, 'exp': minutes_for_payload(30)}),
            id='sub_is_number'
        ),
        pytest.param(
            'not-a-token',
            id='invalid_token'
        ),
        pytest.param(
            make_token(
                {'sub': str(uuid.uuid4()), 'exp': minutes_for_payload(30)},
                 key='another_secret_key_0123456789qweasdzxcv'
                ),
            id='wrong_key'
        )
    ]
)
def test_invalid_tokens_are_rejected(bad_token):
    with pytest.raises(TokenCredentialsError):
        decode_access_token(bad_token)


def test_token_with_tampered_payload_is_rejected():
    token_a = create_access_token(uuid.uuid4())
    token_b = create_access_token(uuid.uuid4())

    header_a, payload_a, signature_a = token_a.split('.')
    header_b, payload_b, signature_b = token_b.split('.')

    assert payload_a != payload_b

    forged_token = '.'.join([header_a, payload_b, signature_a])

    with pytest.raises(TokenCredentialsError):
        decode_access_token(forged_token)