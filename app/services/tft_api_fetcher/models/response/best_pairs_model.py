from pydantic import BaseModel

from app.services.tft_api_fetcher.models.composition import Composition


class CompositionSortedByChampionTier(Composition):
    def __init__(self, **data):
        super().__init__(**data)
        self.sorted_champions = sorted(
            self.champions, key=lambda c: int(c.tier) if c.tier.isdigit() else 99
        )


class BestPairs(BaseModel):
    composition: CompositionSortedByChampionTier
    pairs: list[CompositionSortedByChampionTier]
