from httpx import AsyncClient

from app.config import Settings
from app.utils.normalize import normalize_champ_name

settings = Settings()


def _url_from_square_path(icon_path: str) -> str:
    """Convert squareIconPath (/lol-game-data/assets/...) to CDragon URL."""
    relative = icon_path.removeprefix("/lol-game-data/assets/")
    return f"{settings.tft_champion_url}/latest/game/{relative.lower()}"


def _url_from_icon_field(icon_path: str) -> str:
    """Convert icon field (ASSETS/...) to CDragon URL."""
    path = icon_path.lower().replace(".tex", ".png")
    return f"{settings.tft_champion_url}/latest/game/{path}"


async def fetch_item_images(client: AsyncClient) -> dict[str, str]:
    """Fetch TFT item icons from CommunityDragon.

    Combines standard items from tftitems.json with set-specific items
    from en_us.json so that items like Dead Man's Dagger are included.

    Returns:
        Mapping of normalized item names to their icon URLs.
    """
    item_images: dict[str, str] = {}

    # Standard items (squareIconPath format)
    response = await client.get(
        f"{settings.tft_champion_url}/latest/plugins/rcp-be-lol-game-data"
        "/global/default/v1/tftitems.json"
    )
    for item in response.json():
        name = (item.get("name") or "").strip()
        name_id = item.get("nameId", "")
        icon_path = item.get("squareIconPath", "")
        if not name or not name_id.startswith("TFT_Item_") or not icon_path:
            continue
        key = normalize_champ_name(name)
        if key and key not in item_images:
            item_images[key] = _url_from_square_path(icon_path)

    # Set-specific items (icon field format, supplement only)
    response2 = await client.get(
        f"{settings.tft_champion_url}/latest/cdragon/tft/en_us.json"
    )
    for item in response2.json().get("items", []):
        name = (item.get("name") or "").strip()
        api_name = item.get("apiName", "")
        icon_path = item.get("icon", "")
        if not name or "_Item_" not in api_name or not icon_path:
            continue
        key = normalize_champ_name(name)
        if key and key not in item_images:
            item_images[key] = _url_from_icon_field(icon_path)

    return item_images
