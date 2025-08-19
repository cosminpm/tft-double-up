import heapq
from collections import defaultdict

from app.services.tft_api_fetcher.models.composition import Composition
from app.services.tft_api_fetcher.models.response.best_pairs_model import (
    BestPairs,
    CompositionSortedByChampionTier,
)


def fetch_best_pairs(
    top_compositions: list[Composition], top_n: int = 3
) -> dict[Composition, list[Composition]]:
    """Get the best pairs for all the compositions.

    Args:
    ----
        top_compositions (list[Composition]): All the compositions
        top_n (int): The number of top compositions to return

    Returns:
    -------
    dict[Composition, list[Composition]]

    """
    result: dict[Composition, list[Composition]] = defaultdict(list)

    tier_order = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}

    for i, comp_1 in enumerate(top_compositions):
        for j in range(i + 1, len(top_compositions)):
            comp_2 = top_compositions[j]

            shared = len(comp_1.champions & comp_2.champions)
            score = -shared

            tier_rank_2 = tier_order.get(comp_2.tier.upper(), -1)
            tier_rank_1 = tier_order.get(comp_1.tier.upper(), -1)

            heapq.heappush(result[comp_1], (score, tier_rank_2, comp_2))  # type: ignore[misc]
            if len(result[comp_1]) > top_n:
                heapq.heappop(result[comp_1])

            heapq.heappush(result[comp_2], (score, tier_rank_1, comp_1))  # type: ignore[misc]
            if len(result[comp_2]) > top_n:
                heapq.heappop(result[comp_2])

    final_result: dict[Composition, list[Composition]] = {
        comp: [
            comp_obj  # type: ignore[misc]
            for score, tier_rank, comp_obj in sorted(
                heap,
                key=lambda x: (x[0], -x[1]),  # type: ignore[index]
            )
        ]
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
