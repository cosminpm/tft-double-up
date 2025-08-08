from pydantic import BaseModel

from app.services.tft_api_fetcher.models.composition import Composition


class BestPairs(BaseModel):
    composition: Composition
    pairs: list[Composition]
