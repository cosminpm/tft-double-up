import json
from typing import TYPE_CHECKING

from fastapi import APIRouter
from starlette.requests import Request

from app.config import Settings
from app.services.tft_api_fetcher.fetch_get_pairs import fetch_best_pairs
from app.services.tft_api_fetcher.fetch_repeated_champions import fetch_repeated_champions
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions
from app.services.tft_api_fetcher.fetch_unique_compositions import fetch_unique_compositions
from app.services.tft_api_fetcher.models.composition import Composition
from app.services.tft_api_fetcher.models.response.best_pairs_model import BestPairs

if TYPE_CHECKING:
    from httpx import AsyncClient, Response

settings = Settings()
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
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    return fetch_top_compositions(response)


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
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    return fetch_repeated_champions(response)


@fetch_router.get("/get_unique_compositions")
async def get_unique_compositions(request: Request) -> list[Composition]:
    """Get statistics about how many times a champion is repeated acros multiple compositions.

    Args:
    ----
        request (Request): The request object.

    Returns:
    -------
    A dictionary containing the champion count.

    """
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    top_compositions: list[Composition] = fetch_top_compositions(response)
    repeated_champions: dict[str, int] = fetch_repeated_champions(response)
    return fetch_unique_compositions(top_compositions, repeated_champions)


@fetch_router.get("/get_best_pairs")
async def get_best_pairs(request: Request) -> list[BestPairs]:
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    top_compositions: list[Composition] = fetch_top_compositions(response)
    raw_pairs = fetch_best_pairs(top_compositions)
    return [BestPairs(composition=key, pairs=pairs) for key, pairs in raw_pairs.items()]

