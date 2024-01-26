"""
Main module for the FastAPI application.
Sets up the database connection and includes the routers for the API.
"""
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI

from api import auth, inventory, oauth
from database import database
from resources import lightspeed, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize and close the database connection"""
    print("Initializing database connection...")
    await init_beanie(database=database,
                      document_models=[lightspeed.AuthToken, users.Account])
    print("Database connected successfully..")
    yield
    # do something after app shutdown


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(inventory.router)
