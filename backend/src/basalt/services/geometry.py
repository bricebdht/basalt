"""Terrain geometry computation: convert sides/angles/diagonals to polygon vertices."""

import math

from shapely.geometry import Polygon


def sides_angles_to_vertices(
    a: float, b: float, alpha_deg: float
) -> list[tuple[float, float]]:
    """Compute parallelogram vertices from two sides and the angle between them.

    Places V0 at origin with side `a` along the x-axis.
    """
    alpha_rad = math.radians(alpha_deg)
    dx = b * math.cos(alpha_rad)
    dy = b * math.sin(alpha_rad)
    return [
        (0.0, 0.0),
        (a, 0.0),
        (a + dx, dy),
        (dx, dy),
    ]


def sides_diagonals_to_vertices(
    a: float, b: float, e: float
) -> list[tuple[float, float]]:
    """Compute parallelogram vertices from two sides and one diagonal.

    Uses the law of cosines on the parallelogram diagonal:
        cos(alpha) = (e² - a² - b²) / (2·a·b)
    where `e` is the diagonal from V0 to V2.
    """
    cos_alpha = (e**2 - a**2 - b**2) / (2 * a * b)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))  # clamp for floating point safety
    alpha_deg = math.degrees(math.acos(cos_alpha))
    return sides_angles_to_vertices(a, b, alpha_deg)


def compute_vertices(
    *,
    input_mode: str,
    sides: dict[str, float] | None = None,
    angles_deg: dict[str, float] | None = None,
    diagonals: dict[str, float] | None = None,
    vertices: list[tuple[float, float]] | None = None,
) -> list[tuple[float, float]]:
    """Route to the appropriate vertex computation based on input_mode."""
    if input_mode == "sides_angles":
        if not sides or not angles_deg:
            raise ValueError("sides and angles_deg are required for sides_angles mode")
        return sides_angles_to_vertices(sides["a"], sides["b"], angles_deg["alpha"])

    if input_mode == "sides_diagonals":
        if not sides or not diagonals:
            raise ValueError("sides and diagonals are required for sides_diagonals mode")
        e = diagonals.get("e")
        if e is None:
            raise ValueError("diagonal 'e' is required for sides_diagonals mode")
        return sides_diagonals_to_vertices(sides["a"], sides["b"], e)

    if input_mode == "coordinates":
        if not vertices or len(vertices) < 3:
            raise ValueError("At least 3 vertices are required for coordinates mode")
        return vertices

    raise ValueError(f"Unknown input_mode: {input_mode}")


def validate_polygon(vertices: list[tuple[float, float]]) -> Polygon:
    """Validate that vertices form a valid, non-self-intersecting polygon."""
    poly = Polygon(vertices)
    if not poly.is_valid:
        raise ValueError(f"Invalid polygon: {poly.is_valid}")
    if poly.area <= 0:
        raise ValueError("Polygon has zero or negative area")
    return poly
