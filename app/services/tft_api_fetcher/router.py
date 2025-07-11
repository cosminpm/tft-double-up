from typing import TYPE_CHECKING

from fastapi import APIRouter
from starlette.requests import Request

from app.services.tft_api_fetcher.fetch_repeated_champions import fetch_repeated_champions
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions
from app.services.tft_api_fetcher.models.composition import Composition

if TYPE_CHECKING:
    from httpx import AsyncClient

fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/get_top_compositions")
async def get_top_compositions(request: Request) -> list[Composition]:
    """Get the top tier compositions in Team Fight Tactics and parse it as it comes in a html.

    Args:
    ----
        request (Request): The request object.

    Returns:
    -------
    A list of the top tier compositions.

    """
    requests_client: AsyncClient = request.app.request_client
    return await fetch_top_compositions(requests_client)


@fetch_router.get("/get_repeated_champions")
async def get_repeated_champions(request: Request) -> dict[str, int]:
    """Get the most repeated champions in the top tier compositions.

    Args:
    ----
        request (Request): The request object.

    Returns:
    -------
    A dictionary containing the champion count.

    """
    requests_client: AsyncClient = request.app.request_client
    return await fetch_repeated_champions(requests_client)
