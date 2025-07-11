from bs4 import BeautifulSoup, ResultSet
from httpx import AsyncClient, Response

from app.config import Settings
from app.services.tft_api_fetcher.models.composition import Champion, Composition

settings = Settings()


async def fetch_top_compositions(request_client: AsyncClient) -> list[Composition]:
    """Fetch the top tier compositions in Team Fight Tactics and parse it as it comes in a html.

    Args:
    ----
        request_client (AsyncClient): The AsyncClient used for the async requests.

    """
    response: Response = await request_client.get(f"{settings.tft_url}/tierlist/team-comps/")

    html_content = response.content.decode("utf-8", errors="ignore")
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
    return parse_soup(soup)


def parse_soup(soup: BeautifulSoup) -> list[Composition]:
    """Parse BeautifulSoup object and transform it into a list of Compositions.

    Args:
    ----
        soup (BeautifulSoup): The BeautifulSoup object.

    Returns:
    -------
    A list of Compositions.

    """
    compositions: list[Composition] = []
    for team_div in soup.select(".team-portrait"):
        composition: Composition = Composition.from_tag(team_div)
        composition.champions = get_champions(team_div.select(".characters-item"))
        compositions.append(composition)
    return compositions


def get_champions(characters: ResultSet) -> set[Champion]:
    """Get champions given a BeautifulSoup object.

    Args:
    ----
        characters (ResultSet): The characters in a BeautifulSoup format

    Returns:
    -------
    (set[Champion]) A set of Champions

    """
    champions: set[Champion] = set()
    for champ_div in characters:
        champion = Champion.from_tag(champ_div)
        if champion:
            champions.add(champion)
    return champions
