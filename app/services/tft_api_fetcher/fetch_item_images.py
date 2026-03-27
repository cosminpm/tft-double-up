from httpx import AsyncClient

from app.config import Settings
from app.utils.normalize import normalize_champ_name

settings = Settings()

ITEMS_PATH = "/latest/plugins/rcp-be-lol-game-data/global/default/v1/tftitems.json"


async def fetch_item_images(client: AsyncClient) -> dict[str, str]:
    """Fetch TFT item icons from CommunityDragon.

    Returns:
        Mapping of normalized item names to their icon URLs.
    """
    url = settings.tft_champion_url + ITEMS_PATH
    response = await client.get(url)
    items = response.json()

    item_images: dict[str, str] = {}
    for item in items:
        name = item.get("name", "").strip()
        name_id = item.get("nameId", "")
        icon_path = item.get("squareIconPath", "")

        if not name or not name_id.startswith("TFT_Item_") or not icon_path:
            continue

        key = normalize_champ_name(name)
        if key and key not in item_images:
            item_images[key] = settings.tft_champion_url + icon_path.lower()

    return item_images
