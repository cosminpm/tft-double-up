from httpx import AsyncClient

from app.config import Settings

settings = Settings()


async def fetch_tft_top_compositions(request_client: AsyncClient) -> list:
    """Fetch the top tier compositions in Team Fight Tactics and parse it as it comes in a html.

    Args:
    ----
        request_client (AsyncClient): The AsyncClient used for the async requests.

    """
    await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")
    return []
