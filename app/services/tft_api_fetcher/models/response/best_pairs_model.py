from pydantic import BaseModel, Field

from app.services.tft_api_fetcher.models.composition import Composition, Champion


class CompositionSortedByChampionTier(Composition):
    champions: list[Champion] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.champions.sort(key=lambda c: int(c.tier) if c.tier.isdigit() else 99)


class BestPairs(BaseModel):
    composition: CompositionSortedByChampionTier
    pairs: list[CompositionSortedByChampionTier]
