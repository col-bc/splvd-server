"""
    This module contains the authentication routes for the API.
"""
import re

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

import dependencies
from resources import users

router = APIRouter(prefix="/api/auth", tags=["authentication"])


class TokenResponse(BaseModel):
    """Token response model"""

    access_token: str
    token_type: str
    expires_in: int
    role: users.Account.AccountType


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Request auth token for user"""
    account = await users.Account.find_one({"email": form_data.username})
    if account:
        if account.check_password(form_data.password):
            token, exp = account.generate_token()
            return {
                "access_token": token,
                "token_type": "bearer",
                "expires_in": exp,
                "role": account.account_type,
            }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username name or password does not match our records",
        headers={"WWW-Authenticate": "Bearer"},
    )


class RegisterUserRequest(BaseModel):
    """Request model for registering a new user"""

    email: str = Field(..., description="User's email")
    password: str = Field(..., description="User's password")
    full_name: str = Field(..., description="User's full name")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(form_data: RegisterUserRequest):
    """Register a new user"""
    existing_user = await users.Account.find_one({"email": form_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', form_data.password):
        new_user = users.Account(
            email=form_data.email,
            full_name=form_data.full_name,
            password=form_data.password,
        )
        await new_user.insert()
        return Response(status_code=status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=
        "Password must be at least 8 characters long and contain at least " \
        "one uppercase letter, one lowercase letter and one number",
    )


@router.get("/me", response_model=users.AccountResponse)
async def get_user(user: users.Account = Depends(
    dependencies.get_current_user)):
    """Get current user"""
    return user.serialize()
