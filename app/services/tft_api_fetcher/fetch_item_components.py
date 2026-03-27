from httpx import AsyncClient

from app.config import Settings
from app.utils.normalize import normalize_champ_name

settings = Settings()

TFT_DATA_PATH: str = "/latest/cdragon/tft/en_us.json"


async def fetch_item_components(client: AsyncClient) -> dict[str, list[str]]:
    """Fetch TFT item recipe data from CommunityDragon.

    Returns:
        Mapping of normalized item names to their two component item names.
    """
    response = await client.get(
        f"{settings.tft_champion_url}{TFT_DATA_PATH}"
    )
    data = response.json()
    items = data.get("items", [])

    api_to_name: dict[str, str] = {
        item["apiName"]: normalize_champ_name((item["name"] or "").strip())
        for item in items
        if item.get("apiName") and (item.get("name") or "").strip()
    }

    item_components: dict[str, list[str]] = {}
    for item in items:
        api_name = item.get("apiName", "")
        name = (item.get("name") or "").strip()
        composition = item.get("composition") or []

        if not name or not api_name.startswith("TFT_Item_") or len(composition) != 2:
            continue

        comp_names = [api_to_name.get(c, "") for c in composition]
        if all(comp_names):
            key = normalize_champ_name(name)
            if key:
                item_components[key] = comp_names

    return item_components
