from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str


class Champion(BaseModel):
    name: str
    items: list[Item] = Field(default_factory=list)


class Composition(BaseModel):
    id: int
    name: str
    champions: list[Champion] = Field(default_factory=list)
    tier: str
    play_style: str
