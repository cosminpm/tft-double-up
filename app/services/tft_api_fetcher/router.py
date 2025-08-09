import json
from typing import TYPE_CHECKING

from fastapi import APIRouter
from starlette.requests import Request

from app.config import Settings
from app.services.tft_api_fetcher.fetch_champion_weapon_images import fetch_champion_weapon_images
from app.services.tft_api_fetcher.fetch_get_pairs import fetch_best_pairs
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions
from app.services.tft_api_fetcher.models.composition import Composition
from app.services.tft_api_fetcher.models.response.best_pairs_model import BestPairs

if TYPE_CHECKING:
    from httpx import AsyncClient, Response

settings = Settings()
fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/best_pairs")
async def get_best_pairs(request: Request) -> list[BestPairs]:
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    top_compositions: list[Composition] = fetch_top_compositions(response)
    raw_pairs = fetch_best_pairs(top_compositions)
    return [BestPairs(composition=key, pairs=pairs) for key, pairs in raw_pairs.items()]


@fetch_router.get("/champion_weapon_images")
async def get_best_pairs(request: Request) -> dict[str, str]:
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")
    champion_images: dict[str, str] = fetch_champion_weapon_images(response)
    return champion_images
