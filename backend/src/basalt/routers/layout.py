"""Layout API router."""

from fastapi import APIRouter, HTTPException

from basalt.routers.terrain import _terrains
from basalt.schemas.layout import LayoutValidationRequest, LayoutValidationResponse
from basalt.services.layout import validate_layout

router = APIRouter(prefix="/layout", tags=["layout"])


@router.post("/validate", response_model=LayoutValidationResponse)
def validate(req: LayoutValidationRequest) -> LayoutValidationResponse:
    terrain = _terrains.get(req.terrain_id)
    if not terrain:
        raise HTTPException(status_code=404, detail="Terrain not found")

    violations = validate_layout(
        terrain_vertices=terrain.vertices,
        buildable_vertices=terrain.buildable_polygon,
        rooms=req.rooms,
    )

    return LayoutValidationResponse(
        valid=len(violations) == 0,
        violations=violations,
    )
