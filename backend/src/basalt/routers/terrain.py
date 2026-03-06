"""Terrain API router."""

import uuid

from fastapi import APIRouter, HTTPException

from basalt.schemas.terrain import TerrainInput, TerrainResponse
from basalt.services.geometry import compute_vertices, validate_polygon
from basalt.services.setback import compute_buildable_polygon

router = APIRouter(prefix="/terrain", tags=["terrain"])

# In-memory store for MVP
_terrains: dict[str, TerrainResponse] = {}


@router.post("/compute", response_model=TerrainResponse)
def compute_terrain(req: TerrainInput) -> TerrainResponse:
    try:
        verts = compute_vertices(
            input_mode=req.input_mode,
            sides=req.sides.model_dump() if req.sides else None,
            angles_deg=req.angles_deg.model_dump() if req.angles_deg else None,
            diagonals=req.diagonals.model_dump() if req.diagonals else None,
            vertices=req.vertices,
        )
        poly = validate_polygon(verts)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    buildable_verts, buildable_area = compute_buildable_polygon(
        verts, setback_m=req.setback_distance_m
    )

    terrain_id = str(uuid.uuid4())
    response = TerrainResponse(
        id=terrain_id,
        vertices=[(round(x, 4), round(y, 4)) for x, y in verts],
        area_m2=round(poly.area, 2),
        perimeter_m=round(poly.length, 2),
        setback_distance_m=req.setback_distance_m,
        buildable_polygon=[(round(x, 4), round(y, 4)) for x, y in buildable_verts],
        buildable_area_m2=buildable_area,
    )
    _terrains[terrain_id] = response
    return response


@router.get("/{terrain_id}", response_model=TerrainResponse)
def get_terrain(terrain_id: str) -> TerrainResponse:
    if terrain_id not in _terrains:
        raise HTTPException(status_code=404, detail="Terrain not found")
    return _terrains[terrain_id]
