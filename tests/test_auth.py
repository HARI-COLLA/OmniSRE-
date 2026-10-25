import pytest
from fastapi import HTTPException
from src import auth

def test_auth_disabled_by_default():
    # When API_KEY_ENABLED is False, any or no key should pass
    auth.API_KEY_ENABLED = False
    assert auth.verify_api_key(header_key=None, bearer_creds=None) is True

def test_auth_enabled_valid_key():
    auth.API_KEY_ENABLED = True
    auth.ADMIN_API_KEY = "test-secret-key-123"
    try:
        assert auth.verify_api_key(header_key="test-secret-key-123", bearer_creds=None) is True
    finally:
        auth.API_KEY_ENABLED = False

def test_auth_enabled_invalid_key_raises_401():
    auth.API_KEY_ENABLED = True
    auth.ADMIN_API_KEY = "test-secret-key-123"
    try:
        with pytest.raises(HTTPException) as exc:
            auth.verify_api_key(header_key="wrong-key", bearer_creds=None)
        assert exc.value.status_code == 401
    finally:
        auth.API_KEY_ENABLED = False
