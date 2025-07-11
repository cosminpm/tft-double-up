from app.services.tft_api_fetcher.models.composition import Composition


def fetch_unique_compositions(
    top_compositions: list[Composition], repeated_champions: dict[str, int]
) -> list[Composition]:
    """Get statistics about how many times a champion is repeated acros multiple compositions.

    Args:
    ----
        top_compositions (list[Composition]): Top tier compositions.
        repeated_champions (dict[str,int]): Statuses about repeated champions.

    Returns:
    -------
        A list of compositions including data of other compositions.

    """
    for composition in top_compositions:
        for champion in composition.champions:
            champion.seen_in_other_builds += repeated_champions[champion.name]
    return top_compositions
