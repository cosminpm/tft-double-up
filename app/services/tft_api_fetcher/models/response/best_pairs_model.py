from pydantic import BaseModel

from app.services.tft_api_fetcher.models.composition import Champion, Composition


class CompositionSortedByChampionTier(Composition):
    champions: list[Champion] = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.champions = sorted(
            self.champions, key=lambda c: int(c.tier) if c.tier.isdigit() else 99
        )


class BestPairs(BaseModel):
    composition: CompositionSortedByChampionTier
    pairs: list[CompositionSortedByChampionTier]
