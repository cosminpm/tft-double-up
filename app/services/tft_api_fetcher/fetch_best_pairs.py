import asyncio

from httpx import AsyncClient

from app.config import Settings
from app.services.tft_api_fetcher.fetch_extended_champs import get_tft_set, fetch_planner_composition
from app.services.tft_api_fetcher.fetch_get_pairs import fetch_pairs, sorted_best_pairs
from app.services.tft_api_fetcher.fetch_top_compositions import fetch_top_compositions

settings = Settings()

async def generate_best_pairs(client: AsyncClient) -> list[dict]:
    top_compositions_response, planner_codes_response = await asyncio.gather(
        client.get(f"{settings.tft_url}/tierlist/team-comps/"),
        client.get(
            f"{settings.tft_champion_url}/latest/plugins/rcp-be-lol-game-data/global/default/v1/tftchampions-teamplanner.json"
        ),
    )

    tft_set: str = get_tft_set(planner_codes_response)
    planner_champs = fetch_planner_composition(planner_codes_response)
    top_compositions = fetch_top_compositions(
        top_compositions_response,
        planner_champs,
        tft_set,
    )

    raw_pairs = fetch_pairs(top_compositions)
    sorted_pairs = sorted_best_pairs(raw_pairs)

    return [pair.model_dump() for pair in sorted_pairs]