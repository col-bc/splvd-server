"""
    Load app config from environment variables
"""
from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = environ.get("SECRET_KEY")
LIGHTSPEED_CLIENT_ID = environ.get("LIGHTSPEED_CLIENT_ID")
LIGHTSPEED_SECRET_KEY = environ.get("LIGHTSPEED_SECRET_KEY")
LIGHTSPEED_REDIRECT_URI = environ.get("LIGHTSPEED_REDIRECT_URI")

MONGO_DB_URI = environ.get("MONGO_DB_URI")
MONGO_DB_NAME = environ.get("MONGO_DB_NAME")