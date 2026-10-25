import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

API_KEY_ENABLED = os.getenv("API_KEY_ENABLED", "false").lower() == "true"
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "sre-enterprise-secret-key")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_auth = HTTPBearer(auto_error=False)

def verify_api_key(
    header_key: Optional[str] = Security(api_key_header),
    bearer_creds: Optional[HTTPAuthorizationCredentials] = Security(bearer_auth)
) -> bool:
    """
    Validates API key from either 'X-API-Key' header or 'Authorization: Bearer <token>'.
    Bypassed if API_KEY_ENABLED is false.
    """
    if not API_KEY_ENABLED:
        return True

    provided_key = header_key or (bearer_creds.credentials if bearer_creds else None)

    if not provided_key or provided_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing enterprise API Key.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return True
