"""
    OAuth endpoints for Lightspeed integration
"""
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel

import dependencies
from resources import lightspeed

router = APIRouter(prefix="/api/oauth", tags=["oauth"])


class AuthorizationResponse(BaseModel):
    """Authorization response model"""

    authorization_url: str


@router.get("/authorize", response_model=AuthorizationResponse)
def authorize(token_helper: lightspeed.TokenHelper = Depends(
    dependencies.get_lightspeed_token_helper)):
    """Returns the authorization URL for Lightspeed OAuth integration"""
    url = token_helper.get_user_consent()
    return {"authorization_url": url}


@router.get("/callback")
async def callback(
    code: str,
    token_helper: lightspeed.TokenHelper = Depends(
        dependencies.get_lightspeed_token_helper),
):
    """Callback endpoint forLightspeed OAuth Integration"""
    try:
        await token_helper.exchange_code(code)
        return {"detail": "Token successfully created. Authorization complete"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
