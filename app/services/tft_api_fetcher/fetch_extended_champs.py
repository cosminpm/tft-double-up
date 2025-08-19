from httpx import Response

from app.services.tft_api_fetcher.models.composition import Composition
from app.services.tft_api_fetcher.models.planner_champ import PlannerChamp


def get_tft_set(response: Response) -> str:
    """Get TFT Set name given the response from the Raw Dragon API."""
    return next(iter(response.json().keys()))


def fetch_planner_composition(response: Response) -> dict[str, PlannerChamp]:
    """Fetch the planner code for each champion, for example 21a.

    Args:
    ----
        response (Response): Raw Dragon API response

    Returns: dict[str, PlannerChamp]

    """
    current_tft_set: str = get_tft_set(response)

    json_data = response.json()
    tft_set = json_data[current_tft_set]

    tft_characters: dict[str, PlannerChamp] = {}
    for character in tft_set:
        planner_champ: PlannerChamp = PlannerChamp(
            name=character["display_name"],
            planner_code=character["team_planner_code"],
            planner_hex=character["team_planner_code"],
        )
        tft_characters[planner_champ.name] = planner_champ
    return tft_characters


def composition_to_planner_code(
    composition: Composition, planner_champs: dict[str, PlannerChamp], tft_set: str
) -> str:
    """Build the TFT set code for a given composition.

    Args:
    ----
        composition (Composition): The team composition to convert into a planner code.
        planner_champs (dict[str, PlannerChamp]): Mapping of champion names to their corresponding
            PlannerChamp objects, used to generate the correct code.
        tft_set (str): The TFT set identifier (e.g., "set10") to ensure compatibility with
            the correct set format.

    Returns:
    -------
        str: The encoded planner code representing the given composition.

    """
    champions = [champion.name for champion in composition.champions]

    query = ""
    for champion in champions:
        query += planner_champs[champion].planner_hex

    query = query.ljust(30, "0")
    return "02" + query + tft_set
