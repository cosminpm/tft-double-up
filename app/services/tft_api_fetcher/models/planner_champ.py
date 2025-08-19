from pydantic import BaseModel, field_validator

from app.utils.normalize import normalize_champ_name


class PlannerChamp(BaseModel):
    name: str
    planner_code: int
    planner_hex: str

    @field_validator("planner_hex", mode="before")
    @classmethod
    def transform_to_hex(cls, v: int) -> str:
        return f"{v:03x}"

    @field_validator("name", mode="before")
    @classmethod
    def remove_other_characters(cls, v: str) -> str:
        return normalize_champ_name(v)
