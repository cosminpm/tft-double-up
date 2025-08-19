from pydantic import BaseModel, field_validator


class PlannerChamp(BaseModel):
    name: str
    planner_code: str
    planner_hex: str

    @field_validator('planner_hex')
    @classmethod
    def transform_to_hex(cls, v: str) -> str:
        return f"{v:03x}"
