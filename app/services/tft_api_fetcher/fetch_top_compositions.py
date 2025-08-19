from bs4 import BeautifulSoup, ResultSet
from httpx import Response

from app.config import Settings
from app.services.tft_api_fetcher.fetch_extended_champs import composition_to_planner_code
from app.services.tft_api_fetcher.models.composition import Champion, Composition
from app.services.tft_api_fetcher.models.planner_champ import PlannerChamp

settings = Settings()


def fetch_top_compositions(
    top_compositions_response: Response, planner_champs: dict[str, PlannerChamp], tft_set: str
) -> list[Composition]:
    """Fetch the top tier compositions in Team Fight Tactics and parse it as it comes in a html.

    Args:
    ----
        top_compositions_response (Response): The Response in HTML format of the top compositions.
        planner_champs (dict[str, PlannerChamp]): Mapping of champion names to their corresponding
            PlannerChamp objects, used to build the composition details.
        tft_set (str): The TFT set identifier (e.g., "set10") to determine which version of the
            game data is being parsed.

    Returns:
    -------
        list[Composition]: A list of parsed top-tier team compositions.

    """
    html_content = top_compositions_response.content.decode("utf-8", errors="ignore")
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")

    compositions: list[Composition] = parse_soup(soup)
    return build_planner_codes(compositions, planner_champs, tft_set)


def build_planner_codes(
    compositions: list[Composition], planner_champs: dict[str, PlannerChamp], tft_set: str
) -> list[Composition]:
    """Add the planer code for each composition."""
    result: list[Composition] = []
    for composition in compositions:
        composition.planner_code = composition_to_planner_code(composition, planner_champs, tft_set)
        result.append(composition)
    return result


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
