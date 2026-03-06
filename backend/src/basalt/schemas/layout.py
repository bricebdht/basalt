"""Pydantic schemas for the layout API."""

from pydantic import BaseModel, Field


class Room(BaseModel):
    id: str
    label: str
    x_m: float
    y_m: float
    width_m: float = Field(gt=0)
    height_m: float = Field(gt=0)
    wall_thickness_m: float = Field(ge=0, default=0.2)
    phase: int = Field(ge=1, default=1)


class Violation(BaseModel):
    room_id: str
    type: str  # "setback_violation", "overlap", "out_of_bounds"
    message: str


class LayoutValidationRequest(BaseModel):
    terrain_id: str
    rooms: list[Room]


class LayoutValidationResponse(BaseModel):
    valid: bool
    violations: list[Violation]
