from typing import TYPE_CHECKING

from fastapi import APIRouter
from starlette.requests import Request

from app.services.tft_api_fetcher.manager import fetch_tft_top_compositions

if TYPE_CHECKING:
    from httpx import AsyncClient

fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/get_tft_top_compositions")
async def get_tft_top_compositions(request: Request) -> list:
    """Get the top tier compositions in Team Fight Tactics and parse it as it comes in a html.

    Args:
    ----
        request (Request): The request object.

    """
    requests_client: AsyncClient = request.app.request_client
    return await fetch_tft_top_compositions(requests_client)
