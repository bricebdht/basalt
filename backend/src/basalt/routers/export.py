"""Export API router."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from basalt.routers.terrain import _terrains
from basalt.schemas.layout import Room
from basalt.services.export import render_svg

router = APIRouter(prefix="/export", tags=["export"])


class SvgExportRequest(BaseModel):
    terrain_id: str
    rooms: list[Room] = []


@router.post("/svg")
def export_svg(req: SvgExportRequest) -> Response:
    terrain = _terrains.get(req.terrain_id)
    if not terrain:
        raise HTTPException(status_code=404, detail="Terrain not found")

    svg_content = render_svg(terrain, req.rooms)

    return Response(
        content=svg_content,
        media_type="image/svg+xml",
        headers={"Content-Disposition": "attachment; filename=basalt-plan.svg"},
    )
