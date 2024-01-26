"""
    This module contains the Lightspeed AuthToken model and it's helper class.
"""
from datetime import datetime, timedelta
from typing import Optional

import httpx as http
from beanie import Document
from pydantic import Field

from config import (LIGHTSPEED_CLIENT_ID, LIGHTSPEED_REDIRECT_URI,
                    LIGHTSPEED_SECRET_KEY)


class AuthToken(Document):
    """Lightspeed Token model"""

    access_token: str = Field(...)
    expires_at: datetime = Field(...)
    token_type: str = Field(...)
    scope: str = Field(...)
    domain_prefix: str
    refresh_token: str = Field(...)
    created_at: datetime = Field(datetime.utcnow())
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id:
            self.id = str(self.id)

    @property
    def expired(self) -> bool:
        """Check if token is expired"""
        return self.expires_at < datetime.utcnow()

    def serialize(self) -> dict:
        """Returns json serializable object"""
        return {
            "id": self.id,
            "access_token": self.access_token,
            "expires_at": self.expires_at.isoformat(),  # pylint: disable=no-member
            "token_type": self.token_type,
            "scope": self.scope,
            "refresh_token": self.refresh_token,
            "domain_prefix": self.domain_prefix,
            "is_expired": self.expired,
            "created_at": self.created_at.isoformat(),  # pylint: disable=no-member
        }

    @classmethod
    async def read_latest_token(cls) -> Optional["AuthToken"]:
        """Returns the latest token from the database"""
        return await cls.find_one(sort=[("created_at", -1)])


class TokenHelper:
    """Token helper class
        This class is used to get the user consent URL and exchange the authorization code for an access token. Use it to create a new token or refresh an existing one.
    """

    def __init__(self, client_id: str, secret_key: str):
        self.client_id = client_id or LIGHTSPEED_CLIENT_ID
        self.secret_key = secret_key or LIGHTSPEED_SECRET_KEY
        self.redirect_uri = LIGHTSPEED_REDIRECT_URI
        self.http = http.AsyncClient()

    @property
    def scope(self) -> str:
        """Return the scopes for the token"""
        return "employee:inventory_read"

    def get_user_consent(self):
        """Gets user consent for OAuth2.0 integration"""
        url = f"https://secure.vendhq.com/connect?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}"

        return url

    async def exchange_code(self, domain_prefix: str,
                            code: str) -> Optional[AuthToken]:
        """Exchange authorization code for access token and inserts AccessToken into database"""
        url = f"https://{domain_prefix}.vendhq.com/api/1.0/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.secret_key,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://colbyc.dev/api/oauth/token"
        }
        async with http.AsyncClient() as client:
            response = await client.post(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            expiration = datetime.utcnow() + timedelta(
                seconds=data["expires_in"])
            token = AuthToken(
                access_token=data["access_token"],
                expires_at=expiration,
                token_type=data["token_type"],
                scope=data["scope"],
                refresh_token=data["refresh_token"],
            )
            await token.insert()
            return token
        raise ValueError(response.text)

    async def refresh_token(self, refresh_token: str) -> Optional[AuthToken]:
        """Refreshes the access token and saves it to the database"""
        url = "https://cloud.lightspeedapp.com/oauth/access_token.php"
        params = {
            "client_id": self.client_id,
            "client_secret": self.secret_key,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        async with http.AsyncClient() as client:
            response = await client.post(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            expiration = datetime.utcnow() + timedelta(
                seconds=data["expires_in"])
            token = AuthToken(
                access_token=data["access_token"],
                expires_at=expiration,
                token_type=data["token_type"],
                scope=data["scope"],
                refresh_token=data["refresh_token"],
            )
            await token.save()
            return token
        raise ValueError(response.text)
