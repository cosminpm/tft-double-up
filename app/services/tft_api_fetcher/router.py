from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.requests import Request

from app.config import Settings
from app.services.tft_api_fetcher.fetch_champion_weapon_images import fetch_champion_weapon_images
from app.services.tft_api_fetcher.fetch_get_pairs import fetch_best_pairs, sorted_best_pairs
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions
from app.services.tft_api_fetcher.models.response.best_pairs_model import (
    BestPairs,
)

if TYPE_CHECKING:
    from httpx import AsyncClient, Response

    from app.services.tft_api_fetcher.models.composition import Composition

settings = Settings()
fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/best_pairs")
@cache(expire=86400)
async def get_best_pairs(request: Request) -> list[BestPairs]:
    """Retrieve and return the best composition pairings from the TFT tier list.

    Args:
    ----
        request: FastAPI request object containing the shared HTTP client.

    Returns:
    -------
        List of `BestPairs` with sorted main and paired compositions.

    """
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    top_compositions: list[Composition] = fetch_top_compositions(response)
    raw_pairs = fetch_best_pairs(top_compositions)

    return sorted_best_pairs(raw_pairs)


@fetch_router.get("/champion_weapon_images")
@cache(expire=86400)
async def get_champion_weapon_images(request: Request) -> dict[str, str]:
    """Fetch champion weapon image URLs from the TFT tier list endpoint.

    Args:
    ----
        request: FastAPI request object containing the shared HTTP client.

    Returns:
    -------
        Mapping of champion names to their weapon image URLs.

    """
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")
    champion_images: dict[str, str] = fetch_champion_weapon_images(response)
    return champion_images
