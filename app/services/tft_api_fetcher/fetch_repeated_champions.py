from bs4 import BeautifulSoup
from httpx import AsyncClient, Response
from mypy.checkpattern import defaultdict

from app.config import Settings
from app.services.tft_api_fetcher.models.composition import Champion

settings = Settings()


async def fetch_repeated_champions(request_client: AsyncClient) -> dict[str, int]:
    """Fetch the top most repeated champions in Team Fight Tactics and return the champion count.

    Args:
    ----
        request_client (AsyncClient): The AsyncClient used for the async requests.

    """
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    html_content = response.content.decode("utf-8", errors="ignore")
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
    return parse_soup(soup)


def parse_soup(soup: BeautifulSoup) -> dict[str, int]:
    """Parse BeautifulSoup object and transform it into a dict of champions count.

    Args:
    ----
        soup (BeautifulSoup): The BeautifulSoup object.

    Returns:
    -------
    A dictionary containing the champion count

    """
    champions: dict[str, int] = defaultdict(int)
    for team_div in soup.select(".team-portrait"):
        for champ_div in team_div.select(".characters-item"):
            champion = Champion.from_tag(champ_div)
            if champion:
                champions[champion.name] += 1
    return champions
