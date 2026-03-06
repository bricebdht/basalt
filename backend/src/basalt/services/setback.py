"""Setback computation: derive the buildable area from terrain polygon."""

from shapely.geometry import Polygon


def compute_buildable_polygon(
    vertices: list[tuple[float, float]],
    setback_m: float = 3.0,
) -> tuple[list[tuple[float, float]], float]:
    """Compute the buildable polygon by applying an inward buffer (setback).

    Returns:
        A tuple of (buildable_vertices, buildable_area_m2).
        If the setback consumes the entire terrain, returns ([], 0.0).
    """
    terrain = Polygon(vertices)
    buildable = terrain.buffer(-setback_m, join_style="mitre")

    if buildable.is_empty:
        return [], 0.0

    coords = list(buildable.exterior.coords)
    # Remove the closing duplicate vertex that Shapely adds
    if coords and coords[0] == coords[-1]:
        coords = coords[:-1]

    return coords, round(buildable.area, 2)
