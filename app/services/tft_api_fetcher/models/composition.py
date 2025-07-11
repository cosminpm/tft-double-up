from bs4 import Tag
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str


class Champion(BaseModel):
    name: str
    items: list[Item] = Field(default_factory=list)

    @classmethod
    def from_tag(cls, tag: Tag):
        champ_name = tag.select_one(".team-character-name")
        if not champ_name:
            return None
        name = champ_name.text.strip()
        items_div = tag.select(".character-items img")
        items: list = [Item(name=img["alt"].strip()) for img in items_div]
        return cls(name=name, items=items)

    # Make comparison only between name
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Champion):
            return False
        return self.name == other.name


class Composition(BaseModel):
    name: str
    champions: set[Champion] = Field(default_factory=set)
    tier: str
    play_style: str

    @classmethod
    def from_tag(cls, tag: Tag):
        tier_soup = tag.select_one(".team-rank")
        tier = tier_soup.text.strip() if tag else None

        name_soup = tag.select_one(".team-name-elipsis")
        name = name_soup.contents[0].strip() if name_soup else None

        play_style_soup = tag.select_one(".team-playstyle")
        play_style = play_style_soup.text.strip() if play_style_soup else None

        return cls(name=name, play_style=play_style, tier=tier)
