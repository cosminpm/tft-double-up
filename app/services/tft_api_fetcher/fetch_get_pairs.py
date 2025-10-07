import heapq
from collections import defaultdict

from app.services.tft_api_fetcher.models.composition import Composition
from app.services.tft_api_fetcher.models.response.best_pairs_model import (
    BestPairs,
    CompositionSortedByChampionTier,
)
from app.utils.consts import TIER_ORDER


def fetch_best_pairs(
        top_compositions: list[Composition], top_n: int = 3
) -> dict[Composition, list[Composition]]:
    """Get the best pairs for all the compositions based on multiple scoring factors."""
    def number_of_collisions(c1: Composition, c2: Composition) -> float:
        # More than 2 collisions
        overlap = c1.champions & c2.champions

        if len(overlap) > 2:
            return -1
        # At least one of the collision is the carry
        if any(champ.is_carry for champ in overlap):
            return -1
        return 1.0 / (1 + len(overlap))

    def last_b_tiers(c1: Composition, c2: Composition) -> float:
        if TIER_ORDER["B"] > c1.tier_value or TIER_ORDER["B"] > c2.tier_value:
            return -1
        return (c1.tier_value + c2.tier_value) / 2.0

    def reroll_vs_fast_8(c1: Composition, c2: Composition) -> float:
        if "Roll" in c2.play_style and "Roll" in c1.play_style:
            return 1
        if "Roll" not in c2.play_style and not "Roll" in c1.play_style:
            return 1
        return 0

    def total_pair_score(c1: Composition, c2: Composition) -> float:
        """Combine all valid scoring factors. If any return -1 → skip pair."""
        scores = [
            number_of_collisions(c1, c2) * 100,
            last_b_tiers(c1, c2) * 10,
            reroll_vs_fast_8(c1, c2),
        ]

        if any(s == -1 for s in scores):
            return -1
        return sum(scores)

    result: dict[Composition, list[tuple[float, Composition]]] = defaultdict(list)

    for i, comp_1 in enumerate(top_compositions):
        for j in range(i + 1, len(top_compositions)):
            comp_2 = top_compositions[j]
            score = total_pair_score(comp_1, comp_2)
            if score == -1:
                continue

            heapq.heappush(result[comp_1], (score, comp_2))
            if len(result[comp_1]) > top_n:
                heapq.heappop(result[comp_1])

            heapq.heappush(result[comp_2], (score, comp_1))
            if len(result[comp_2]) > top_n:
                heapq.heappop(result[comp_2])

    final_result: dict[Composition, list[Composition]] = {
        comp: [comp_obj for _, comp_obj in sorted(heap, key=lambda x: -x[0])]
        for comp, heap in result.items()
    }

    return final_result


def sorted_best_pairs(raw_pairs: dict[Composition, list[Composition]]) -> list[BestPairs]:
    """Convert a mapping of compositions to `BestPairs`.

    Args:
    ----
        raw_pairs: Dict mapping a main `Composition` to a list of paired `Composition` objects.

    Returns:
    -------
        List of `BestPairs` with sorted main and paired compositions.

    """
    result: list = []
    for key, pairs in raw_pairs.items():
        sorted_key = CompositionSortedByChampionTier(
            name=key.name,
            champions=list(key.champions),
            tier=key.tier,
            play_style=key.play_style,
            planner_code=key.planner_code,
        )
        sorted_pairs = [
            CompositionSortedByChampionTier(
                name=pair.name,
                champions=list(pair.champions),
                tier=pair.tier,
                play_style=pair.play_style,
                planner_code=pair.planner_code,
            )
            for pair in pairs
        ]
        result.append(BestPairs(composition=sorted_key, pairs=sorted_pairs))
    return result
