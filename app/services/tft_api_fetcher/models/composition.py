import re

from bs4 import Tag
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str


class Champion(BaseModel):
    name: str
    items: list[Item] = Field(default_factory=list)
    tier: str = "Z"
    is_3_star: bool = False

    @classmethod
    def from_tag(cls, tag: Tag):
        champ_name = tag.select_one(".team-character-name")
        if not champ_name:
            return None
        name = champ_name.text.strip()
        items_div = tag.select(".character-items img")
        items: list = [Item(name=img["alt"].strip()) for img in items_div]

        # get champion tier
        tier_color_parse: list[str] = tag.get("class", [])
        tier = next((cls for cls in tier_color_parse if re.match(r"^c\d+$", cls)), None)[1:]  # type: ignore[index]
        is_3_star = bool(next((cls for cls in tier_color_parse if re.match(r"^l\d+$", cls)), None))

        return cls(name=name, items=items, tier=tier, is_3_star=is_3_star)

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

    def compare_composition_similarity(self, composition: "Composition") -> int:
        return -len(self.champions & composition.champions)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Champion):
            return False
        return self.name == other.name

    def __lt__(self, other: "Composition"):
        tier_order = {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4, "F": 5}

        self_tier_rank = tier_order.get(self.tier.upper(), 99)
        other_tier_rank = tier_order.get(other.tier.upper(), 99)

        if self_tier_rank != other_tier_rank:
            return self_tier_rank < other_tier_rank
        return self.name < other.name

    @classmethod
    def from_tag(cls, tag: Tag):
        tier_soup = tag.select_one(".team-rank")
        tier = tier_soup.text.strip() if tag else None

        name_soup = tag.select_one(".team-name-elipsis")
        name = name_soup.contents[0].strip() if name_soup else None

        play_style_soup = tag.select_one(".team-playstyle")
        play_style = play_style_soup.text.strip() if play_style_soup else None

        return cls(name=name, play_style=play_style, tier=tier)
