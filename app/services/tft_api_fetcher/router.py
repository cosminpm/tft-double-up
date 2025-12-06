import asyncio
import hashlib
import json
from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from starlette import status
from starlette.requests import Request

from app.config import Settings
from app.services.tft_api_fetcher.fetch_champion_weapon_images import fetch_champion_weapon_images
from app.services.tft_api_fetcher.fetch_extended_champs import (
    fetch_planner_composition,
    get_tft_set,
)
from app.services.tft_api_fetcher.fetch_get_pairs import fetch_pairs, sorted_best_pairs
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions

if TYPE_CHECKING:
    from httpx import AsyncClient, Response

    from app.services.tft_api_fetcher.models.composition import Composition
    from app.services.tft_api_fetcher.models.planner_champ import PlannerChamp
    from app.services.tft_api_fetcher.models.response.best_pairs_model import BestPairs

settings = Settings()
fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/best_pairs")
@cache(expire=86400) if not settings.debug else (lambda f: f)
async def get_best_pairs(request: Request) -> JSONResponse:
    """Retrieve and return the best composition pairings from the TFT tier list.

    Args:
    ----
        request: FastAPI request object containing the shared HTTP client.

    Returns:
    -------
        List of `BestPairs` with sorted main and paired compositions.

    """
    request_client: AsyncClient = request.app.request_client

    top_compositions_response, planner_codes_response = await asyncio.gather(
        request_client.get(f"{settings.tft_url}/tierlist/team-comps/"),
        request_client.get(
            f"{settings.tft_champion_url}/latest/plugins/rcp-be-lol-game-data/global/default/v1/tftchampions-teamplanner.json"
        ),
    )

    tft_set: str = get_tft_set(planner_codes_response)
    planner_champs: dict[str, PlannerChamp] = fetch_planner_composition(planner_codes_response)
    top_compositions: list[Composition] = fetch_top_compositions(
        top_compositions_response, planner_champs, tft_set
    )

    raw_pairs = fetch_pairs(top_compositions)

    sorted_pairs: list[BestPairs] = sorted_best_pairs(raw_pairs)

    serializable_pairs = [pair.model_dump() for pair in sorted_pairs]  # Pydantic v2
    content_bytes = json.dumps(serializable_pairs).encode("utf-8")
    etag = hashlib.md5(content_bytes).hexdigest()

    if request.headers.get("if-none-match") == etag:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content=None)
    return JSONResponse(content=serializable_pairs, headers={"ETag": etag})


@fetch_router.get("/champion_weapon_images")
@cache(expire=86400)
async def get_champion_weapon_images(request: Request) -> JSONResponse:
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

    content_bytes = json.dumps(champion_images).encode("utf-8")
    etag = hashlib.md5(content_bytes).hexdigest()

    if request.headers.get("if-none-match") == etag:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content=None)

    return JSONResponse(content=champion_images, headers={"ETag": etag})
