from bs4 import BeautifulSoup
from httpx import Response, AsyncClient

from app.utils.normalize import normalize_champ_name
from app.config import Settings

settings = Settings()

async def fetch_champion_weapon_images(client: AsyncClient) -> dict[str, str]:
    """Parse a TFT tier list response to extract champion weapon image URLs.

    Args:
    ----
        response: HTTP response containing the tier list HTML.

    Returns:
    -------
        Mapping of champion names to their weapon image URLs.

    """
    response: Response = await client.get(f"{settings.tft_url}/tierlist/team-comps/")
    html_content = response.content.decode("utf-8", errors="ignore")
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
    return parse_soup(soup)


def parse_soup(soup: BeautifulSoup) -> dict[str, str]:
    """Extract champion image URLs from the given HTML.

    Args:
    ----
        soup: Parsed BeautifulSoup object of the TFT team compositions page.

    Returns:
    -------
        Mapping of champion names to their image URLs.

    """
    champion_images: dict[str, str] = {}
    for team_div in soup.select(".team-portrait"):
        for character in team_div.select(".character-icon"):
            if (name := normalize_champ_name(character.get("alt"))) not in champion_images:
                champion_images[name] = character.get("src")
    return champion_images
