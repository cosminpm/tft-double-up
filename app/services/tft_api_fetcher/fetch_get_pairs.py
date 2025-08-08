import heapq
from collections import defaultdict

from app.services.tft_api_fetcher.models.composition import Composition


def fetch_best_pairs(top_compositions: list[Composition], top_n: int = 3) -> dict[Composition, list[Composition]]:
    """Get the best pairs for all the compositions.

    Args:
    ----
        top_compositions (list[Composition]): All the compositions

    Returns:
    -------
    dict[Composition, list[Composition]]

    """
    result: dict[Composition: list[Composition]] = defaultdict(list)

    for i, comp_1 in enumerate(top_compositions):
        for j in range(i + 1, len(top_compositions)):
            comp_2 = top_compositions[j]

            score: int = comp_1.compare_composition_similarity(comp_2)

            heapq.heappush(result[comp_1], (score, comp_2))
            if len(result[comp_1]) > top_n:
                heapq.heappop(result[comp_1])

            heapq.heappush(result[comp_2], (score, comp_1))
            if len(result[comp_2]) > top_n:
                heapq.heappop(result[comp_2])

    final_result: dict[Composition, list[Composition]] = {
        comp: [c for _, c in sorted(heap)]
        for comp, heap in result.items()
    }

    return final_result

