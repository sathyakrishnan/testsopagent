"""
Authentication endpoints with Azure AD integration
Dependencies: msal, azure-identity
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

from app.core.azure_auth import azure_auth, AzureADAuth
from app.core.logging_config import get_logger
from app.core.config import settings

router = APIRouter()
logger = get_logger(__name__)


class TokenRequest(BaseModel):
    """Token request for client credentials flow"""
    grant_type: str = "client_credentials"
    client_id: str
    client_secret: str
    scope: str = "claims.read claims.write"


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str
    expires_in: int


@router.post("/token", response_model=TokenResponse)
async def get_token(
    grant_type: str = Body(...),
    client_id: str = Body(...),
    client_secret: str = Body(...),
    scope: str = Body(default="claims.read claims.write")
):
    """
    OAuth 2.0 Token Endpoint (Azure AD Client Credentials Flow)
    
    For Mendix to authenticate:
    
    POST /api/v1/auth/token
    Content-Type: application/json
    
    {
        "grant_type": "client_credentials",
        "client_id": "your-azure-ad-client-id",
        "client_secret": "your-azure-ad-client-secret",
        "scope": "claims.read claims.write"
    }
    
    Returns JWT token valid for 1 hour.
    """
    
    logger.info(
        "token_request_received",
        grant_type=grant_type,
        client_id=client_id,
        requested_scope=scope
    )
    
    # Validate grant type
    if grant_type != "client_credentials":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only client_credentials grant type is supported"
        )
    
    # Convert scope string to list
    scope_list = [f"api://{settings.AZURE_CLIENT_ID}/.default"]
    
    try:
        # Get token from Azure AD
        result = await azure_auth.get_token_for_client(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope_list
        )
        
        return TokenResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("token_generation_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate token"
        )


@router.post("/token/legacy")
async def get_token_legacy(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Legacy OAuth endpoint for backward compatibility
    ⚠️  For development only - use /token for production
    """
    
    if settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Legacy authentication not available in production. Use Azure AD authentication at /api/v1/auth/token"
        )
    
    # Simple hardcoded check for development
    if form_data.username != "mendix_client" or form_data.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    from app.core.security import create_access_token
    from datetime import timedelta
    
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800
    }
