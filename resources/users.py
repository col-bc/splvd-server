"""
    This module contains the UserAccount model and the pydantic models for CRUD operations.
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from bcrypt import checkpw, gensalt, hashpw
from beanie import Document
from jose import jwt
from pydantic import BaseModel, Field

from config import SECRET_KEY


class Account(Document):
    """UserAccount model"""

    class AccountType(str, Enum):
        """Available account types"""

        STREAMER = "streamer"
        ADMIN = "admin"

    email: str = Field(...)
    password: Optional[str] = Field(...)
    full_name: str = Field(...)
    account_type: AccountType = Field(AccountType.STREAMER)
    # TODO: Other account related fields ...
    created_at: datetime = Field(datetime.utcnow())
    updated_at: datetime = Field(datetime.utcnow())

    _READ_ONLY_FIELDS = ("id", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id:
            self.id = str(self.id)

    async def set_password(self, plain_password: str):
        """Set password hash"""
        self.password = hashpw(plain_password.encode(), gensalt()).decode()
        await self.save()

    async def check_password(self, plain_password: str) -> bool:
        """Check password hash"""
        return checkpw(plain_password.encode(), self.password.encode())

    def serialize(self) -> dict:
        """Serialize UserAccount model"""
        #
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "account_type": self.account_type,
            "created_at": self.created_at.isoformat(),  #pylint: disable=no-member
            "updated_at": self.updated_at.isoformat(),
        }

    async def generate_token(self) -> tuple:
        """Generate a new JWT token. Returns the token and its expiration time"""
        now = int(datetime.utcnow().timestamp())
        expires = int(now + timedelta(hours=4).total_seconds())
        return jwt.encode(
            {
                "sub": self.id,
                "iat": now,
                "exp": expires,
            },
            SECRET_KEY,
            algorithm="HS256",
        ), expires

    @staticmethod
    async def check_token(token: str) -> Optional['Account']:
        """Check if token is valid and returns a UserAccount object"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.JWTError:
            print("Invalid token")
            return None
        if payload.get("sub"):
            return await Account.get(payload["sub"])
        return None

    async def save(self, *args, **kwargs):
        """Save UserAccount model"""
        self.updated_at = datetime.utcnow()
        await super().save(*args, **kwargs)

    def __setattr__(self, key, value):
        """Override __setattr__ to prevent changing read-only fields"""
        if key in self._READ_ONLY_FIELDS:
            raise AttributeError(f"Cannot update read-only field {key}")
        super().__setattr__(key, value)


class AccountCreate(BaseModel):
    """UserAccount create model"""

    email: str = Field(description="User's email", alias="username")
    password: str = Field(...)
    full_name: str = Field(min_length=3, max_length=50)
    account_type: Account.AccountType = Field(Account.AccountType.STREAMER)


class AccountResponse(BaseModel):
    """UserAccount response model"""

    id: str
    email: str
    full_name: str
    account_type: Account.AccountType
    created_at: str
    updated_at: str


class AccountUpdate(BaseModel):
    """UserAccount update model"""

    full_name: str = Field(min_length=3, max_length=50)
