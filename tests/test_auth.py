from urllib.parse import urlencode

from httpx import Client
from pytest import main as pytest_main
from pytest import mark

client = Client()

URL_BASE = "http://localhost:8000/api/auth"


class TestAuth:
    """Test authentication"""

    # Get this token from the /api/auth/login endpoint
    # Replace the token below with the one you got from the login endpoint
    token: str = ""

    def setup_class(self):
        """Setup"""
        if not self.token:
            raise ValueError("Token is required to run this test")

    @mark.skipif(
        True, reason="Change email to a non registered  address to run this")
    def test_create_user(self):
        """Test create user"""
        res = client.post(f"{URL_BASE}/register",
                          json={
                              "email": "jdoe@acme.org",
                              "password": "Passw0rd",
                              "full_name": "John Doe",
                          })
        assert res.status_code == 201

    def test_create_duplicate_user(self):
        """Test create user"""
        res = client.post(f"{URL_BASE}/register",
                          json={
                              "email": "jdoe@acme.org",
                              "password": "Passw0rd",
                              "full_name": "John Doe",
                          })
        assert res.status_code == 409

    def test_login(self):
        """Test login"""
        res = client.post(
            f"{URL_BASE}/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            content=urlencode({
                "username": "jdoe@acme.org",
                "password": "Passw0rd",
                "grant_type": "password"
            }))
        assert res.status_code == 200
        assert res.json()["access_token"]
        assert res.json()["token_type"] == "bearer"
        self.token = res.json()["access_token"]
        print("Auth Token: " + self.token)

    def test_login_invalid(self):
        """Test login with invalid credentials"""
        res = client.post(
            f"{URL_BASE}/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            content=urlencode({
                "username": "jdoe@acme.org",
                "password": "wrong-pass",
                "grant_type": "password"
            }))
        assert res.status_code == 401
        assert res.json(
        )["detail"] == "Username name or password does not match our records"

    def test_get_profile(self, ):
        """Test get profile"""
        print({"Authorization": f"Bearer {self.token}"})
        res = client.get(f"{URL_BASE}/me",
                         headers={"Authorization": f"Bearer {self.token}"})
        assert res.status_code == 200
        assert isinstance(res.json()["id"], str)
        assert res.json()["email"] is not None
        assert res.json()["full_name"] is not None
        assert res.json()["account_type"] in ['streamer', 'admin']
        assert res.json()["created_at"] is not None
        assert res.json()["updated_at"] is not None

    def test_get_profile_unauthorized(self):
        """Test get profile without token"""
        res = client.get(f"{URL_BASE}/me")
        assert res.status_code == 401
        assert res.json()["detail"] == "Not authenticated"


if __name__ == "__main__":
    pytest_main([__file__])
