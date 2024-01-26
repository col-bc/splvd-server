"""
    Example endpoints for lightspeed integration
"""
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

import dependencies

router = APIRouter(prefix="/api/ls/inventory", tags=["lightspeed"])


@router.get("/items")
async def get_items(headers: dict = Depends(
    dependencies.get_lightspeed_headers)):
    """Get items from Lightspeed"""
    url = "https://api.lightspeedapp.com/API/V3/Account/{accountID}/ItemMatrix.json"
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=response.text,
    )
