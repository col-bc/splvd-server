"""
Main module for the FastAPI application.
Sets up the database connection and includes the routers for the API.
"""
import os
from contextlib import asynccontextmanager
from tracemalloc import start

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import FileResponse

from api import auth, inventory, oauth
from database import database
from resources import lightspeed, users

# start tracing memory usage
start()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize and close the database connection"""
    print("Initializing database connection...")
    await init_beanie(database=database,
                      document_models=[lightspeed.AuthToken, users.Account])
    print("Database connected successfully..")
    yield
    # do something after app shutdown


desc = """
This is the API for the SPLYD Frontend. It is ued as the middleware between the frontend and the Lightspeed Retail API.
"""

app = FastAPI(lifespan=lifespan,
              title="SPLYD Inventory API",
              description=desc,
              version="ALPHA",
              license_info={
                  "name": "MIT",
                  "url": "https://splyd.colbyc.dev/terms"
              },
              servers=[
                  {
                      "url": "https://splyd.colbyc.dev",
                      "description": "Production Server"
                  },
              ],
              contact={
                  "name": "GitHub Issues",
                  "url": "https://github.com/col-bc/splvd-server/issues/new",
              },
              redoc_url="/",
              docs_url="/docs")


@app.get("/terms")
def render_terms():
    """Render the terms of service page."""
    path = os.path.join(os.path.dirname(__file__), "LICENSE")
    return FileResponse(path)


app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(inventory.router)
