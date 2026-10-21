import pytest

from app.core.security import get_password_hash, verify_password

VALID_PASSWORD = 'qwerty123'


def test_correct_password_is_verified():
    hashed_password = get_password_hash(VALID_PASSWORD)

    assert verify_password(VALID_PASSWORD, hashed_password) is True


@pytest.mark.parametrize(
        'wrong_password',
        [
            pytest.param(
                'qwerty123123',
                id='wrong_password'
            ),
            pytest.param(
                'Qwerty123',
                id='same_password_with_capital_letter'
            ),
            pytest.param(
                'qwerty123 ',
                id='same_password_with_trailing_space'
            ),
            pytest.param(
                '',
                id='empty_password'
            )
        ]
)
def test_wrong_passwords_are_rejected(wrong_password):
    hashed_password = get_password_hash(VALID_PASSWORD)

    assert verify_password(wrong_password, hashed_password) is False


def test_same_password_produces_different_hashes():
    hash_a = get_password_hash(VALID_PASSWORD)
    hash_b = get_password_hash(VALID_PASSWORD)

    assert hash_a != hash_b

    assert verify_password(VALID_PASSWORD, hash_a) is True 
    assert verify_password(VALID_PASSWORD, hash_b) is True