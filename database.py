"""
    This module is used to connect to the database.
"""
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_NAME, MONGO_DB_URI

client = AsyncIOMotorClient(MONGO_DB_URI)
database = client[MONGO_DB_NAME]