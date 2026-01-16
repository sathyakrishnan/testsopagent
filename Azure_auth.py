"""
Azure AD OAuth 2.0 Integration
Dependencies: msal, azure-identity
"""
from typing import Optional, Dict
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import msal
from datetime import datetime, timedelta
import httpx

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/token")
bearer_scheme = HTTPBearer()


class AzureADAuth:
    """Azure AD authentication handler"""
    
    def __init__(self):
        self.tenant_id = settings.AZURE_TENANT_ID
        self.client_id = settings.AZURE_CLIENT_ID
        self.client_secret = settings.AZURE_CLIENT_SECRET
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = [f"api://{self.client_id}/.default"]
        
        # MSAL app for token validation
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
    
    async def get_token_for_client(self, client_id: str, client_secret: str, scope: list) -> Dict:
        """
        Get access token for client credentials flow
        This is what Mendix will call to get a token
        """
        
        try:
            # Create MSAL app for this client
            client_app = msal.ConfidentialClientApplication(
                client_id,
                authority=self.authority,
                client_credential=client_secret
            )
            
            # Acquire token
            result = client_app.acquire_token_for_client(scopes=scope)
            
            if "access_token" in result:
                logger.info(
                    "azure_token_issued",
                    client_id=client_id,
                    expires_in=result.get("expires_in")
                )
                return {
                    "access_token": result["access_token"],
                    "token_type": "Bearer",
                    "expires_in": result["expires_in"]
                }
            else:
                error = result.get("error_description", "Unknown error")
                logger.error("azure_token_failed", error=error)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Failed to acquire token: {error}"
                )
        
        except Exception as e:
            logger.error("azure_auth_error", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication service error"
            )
    
    async def verify_token(self, token: str) -> Dict:
        """
        Verify Azure AD token
        Returns decoded token payload if valid
        """
        
        try:
            # Get signing keys from Azure AD
            jwks_uri = f"{self.authority}/discovery/v2.0/keys"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(jwks_uri)
                jwks = response.json()
            
            # Decode and verify token
            # Note: In production, cache the signing keys
            unverified_header = jwt.get_unverified_header(token)
            
            # Find the key
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    break
            
            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find signing key"
                )
            
            # Verify token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=f"api://{self.client_id}",
                issuer=f"{self.authority}/v2.0"
            )
            
            logger.info("token_verified", subject=payload.get("sub"))
            return payload
        
        except JWTError as e:
            logger.error("token_verification_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception as e:
            logger.error("token_verification_error", error=str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )


# Global Azure AD auth instance
azure_auth = AzureADAuth()


async def get_current_user_azure(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict:
    """
    Dependency to get current user from Azure AD token
    Use this in endpoints that require Azure AD authentication
    """
    
    token = credentials.credentials
    payload = await azure_auth.verify_token(token)
    
    return {
        "sub": payload.get("sub"),
        "client_id": payload.get("azp") or payload.get("appid"),
        "roles": payload.get("roles", []),
        "scopes": payload.get("scp", "").split() if payload.get("scp") else []
    }


def require_scope_azure(required_scope: str):
    """
    Dependency to check if user has required scope from Azure AD token
    """
    
    async def scope_checker(current_user: Dict = Depends(get_current_user_azure)):
        user_scopes = current_user.get("scopes", [])
        
        if required_scope not in user_scopes:
            logger.warning(
                "insufficient_scope",
                required=required_scope,
                provided=user_scopes,
                user=current_user.get("sub")
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required scope: {required_scope}"
            )
        
        return None
    
    return scope_checker
