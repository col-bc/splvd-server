"""
    Load app config from environment variables
"""
from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# TODO: Load environment variables from .env file
SECRET_KEY = "fake-secret-e7c1021d2c802fb05fb169510eae0ce3" # replace this before production
LIGHTSPEED_CLIENT_ID = "lightspeed-client-id"
LIGHTSPEED_SECRET_KEY = "lightspeed-secret-key"
MONGO_DB_URI = environ.get("MONGO_DB_URI")
MONGO_DB_NAME = environ.get("MONGO_DB_NAME")
