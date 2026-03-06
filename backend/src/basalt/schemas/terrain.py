"""Pydantic schemas for the terrain API."""

from typing import Literal

from pydantic import BaseModel, Field


class TerrainSides(BaseModel):
    a: float = Field(gt=0)
    b: float = Field(gt=0)


class TerrainAngles(BaseModel):
    alpha: float = Field(gt=0, lt=180)


class TerrainDiagonals(BaseModel):
    e: float | None = Field(default=None, gt=0)
    f: float | None = Field(default=None, gt=0)


class TerrainInput(BaseModel):
    input_mode: Literal["sides_angles", "sides_diagonals", "coordinates"]
    sides: TerrainSides | None = None
    angles_deg: TerrainAngles | None = None
    diagonals: TerrainDiagonals | None = None
    vertices: list[tuple[float, float]] | None = None
    setback_distance_m: float = Field(default=3.0, ge=0)


class TerrainResponse(BaseModel):
    id: str
    vertices: list[tuple[float, float]]
    area_m2: float
    perimeter_m: float
    setback_distance_m: float
    buildable_polygon: list[tuple[float, float]]
    buildable_area_m2: float
