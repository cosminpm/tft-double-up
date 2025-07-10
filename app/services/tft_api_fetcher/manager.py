from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from httpx import AsyncClient

from app.config import Settings
from app.services.tft_api_fetcher.models.composition import Composition

if TYPE_CHECKING:
    from fastapi import Response

settings = Settings()


async def fetch_tft_top_compositions(request_client: AsyncClient) -> list:
    """Fetch the top tier compositions in Team Fight Tactics and parse it as it comes in a html.

    Args:
    ----
        request_client (AsyncClient): The AsyncClient used for the async requests.

    """
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    html_content = response.content.decode("utf-8", errors="ignore")
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
    parse_soup(soup)
    return []


def parse_soup(soup: BeautifulSoup) -> list[Composition]:
    """
    Parse beautful soup and transform it into a list of Compositions
    Args:
        soup:

    Returns:

    """
    for team_div in soup.select(".team-portrait"):
        composition = Composition.from_tag(team_div)

        champions = []
        for champ_div in team_div.select(".characters-item"):
            champ_name = champ_div.select_one(".team-character-name")
            if not champ_name:
                continue

            name_text_champ = champ_name.text.strip()

            # Items (if any)
            items_div = champ_div.select(".character-items img")
            items = [img["alt"].strip() for img in items_div] if items_div else []

            champions.append({"name": name_text_champ, "items": items})
    return []