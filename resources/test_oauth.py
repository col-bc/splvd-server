from httpx import Client
from pytest import main as pytest_main
from pytest import mark

client = Client()

URL_BASE = "http://localhost:8000/api/oauth"


class TestOauth:
    """Test oauth implementation"""

    def test_get_authorization_url(self):
        """Test get authorize url"""
        res = client.get(f"{URL_BASE}/authorize")
        assert res.status_code == 200
        assert res.json()["authorization_url"]

if __name__ == "__main__":
    pytest_main([__file__])

