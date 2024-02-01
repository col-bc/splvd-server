"""
    This module contains the dependency functions for the API.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import LIGHTSPEED_CLIENT_ID, LIGHTSPEED_SECRET_KEY
from resources import lightspeed, users

token_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(
    token_scheme)) -> users.Account:
    """Restrict resource to authenticated users"""
    user = await users.Account.check_token(token)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_admin(user: users.Account = Depends(get_current_user)):
    """Restrict resource to admin users"""
    if user.account_type == users.Account.AccountType.ADMIN:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this resource",
    )


def get_lightspeed_token_helper() -> lightspeed.TokenHelper:
    """Return a LightspeedToken helper"""
    return lightspeed.TokenHelper(
        LIGHTSPEED_CLIENT_ID,
        LIGHTSPEED_SECRET_KEY,
    )


async def get_lightspeed_token(helper=Depends(
    get_lightspeed_token_helper)) -> lightspeed.AuthToken:
    """Return the latest Lightspeed auth token from the database"""
    ls_auth_token = await lightspeed.AuthToken.find_one(sort=[("created_at",
                                                               -1)])
    if ls_auth_token:
        if ls_auth_token.is_expired:
            ls_auth_token = helper.refresh_token(ls_auth_token.refresh_token)
        return ls_auth_token
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No token found. Please authorize the app first",
    )


def get_lightspeed_headers(token: lightspeed.AuthToken = Depends(
    get_lightspeed_token)) -> dict:
    """Return the latest Lightspeed auth token from the database"""
    return {"Authorization": f"Bearer {token.access_token}"}
