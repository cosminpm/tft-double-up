from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.requests import Request

from app.config import Settings
from app.services.tft_api_fetcher.fetch_champion_weapon_images import fetch_champion_weapon_images
from app.services.tft_api_fetcher.fetch_get_pairs import fetch_best_pairs
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions
from app.services.tft_api_fetcher.models.composition import Composition
from app.services.tft_api_fetcher.models.response.best_pairs_model import BestPairs, CompositionSortedByChampionTier

if TYPE_CHECKING:
    from httpx import AsyncClient, Response

settings = Settings()
fetch_router: APIRouter = APIRouter(tags=["Fetch"])


@fetch_router.get("/best_pairs")
@cache(expire=86400)
async def get_best_pairs(request: Request) -> list[BestPairs]:
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    top_compositions: list[Composition] = fetch_top_compositions(response)
    raw_pairs = fetch_best_pairs(top_compositions)

    result = []
    for key, pairs in raw_pairs.items():
        sorted_key = CompositionSortedByChampionTier(
            name=key.name,
            champions=list(key.champions),
            tier=key.tier,
            play_style=key.play_style,
        )
        sorted_pairs = [
            CompositionSortedByChampionTier(
                name=pair.name,
                champions=list(pair.champions),
                tier=pair.tier,
                play_style=pair.play_style,
            )
            for pair in pairs
        ]
        result.append(BestPairs(composition=sorted_key, pairs=sorted_pairs))

    return result

@fetch_router.get("/champion_weapon_images")
@cache(expire=86400)
async def get_champion_weapon_images(request: Request) -> dict[str, str]:
    request_client: AsyncClient = request.app.request_client
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")
    champion_images: dict[str, str] = fetch_champion_weapon_images(response)
    return champion_images
