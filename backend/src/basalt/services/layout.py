"""Layout validation: check rooms against terrain constraints."""

from shapely.geometry import Polygon, box

from basalt.schemas.layout import Room, Violation


def room_to_polygon(room: Room) -> Polygon:
    """Convert a room (position + dimensions including walls) to a Shapely polygon."""
    return box(room.x_m, room.y_m, room.x_m + room.width_m, room.y_m + room.height_m)


def validate_layout(
    terrain_vertices: list[tuple[float, float]],
    buildable_vertices: list[tuple[float, float]],
    rooms: list[Room],
) -> list[Violation]:
    """Validate rooms against terrain and setback constraints."""
    violations: list[Violation] = []

    terrain_poly = Polygon(terrain_vertices)
    buildable_poly = Polygon(buildable_vertices) if buildable_vertices else None

    room_polygons = [(room, room_to_polygon(room)) for room in rooms]

    for room, poly in room_polygons:
        # Check out of terrain bounds
        if not terrain_poly.contains(poly):
            violations.append(Violation(
                room_id=room.id,
                type="out_of_bounds",
                message=f"'{room.label}' dépasse les limites du terrain",
            ))
        # Check setback violation
        elif buildable_poly and not buildable_poly.contains(poly):
            violations.append(Violation(
                room_id=room.id,
                type="setback_violation",
                message=f"'{room.label}' empiète sur la zone de recul",
            ))

    # Check pairwise overlaps
    for i, (room_a, poly_a) in enumerate(room_polygons):
        for room_b, poly_b in room_polygons[i + 1:]:
            if poly_a.intersects(poly_b) and not poly_a.touches(poly_b):
                violations.append(Violation(
                    room_id=room_a.id,
                    type="overlap",
                    message=f"'{room_a.label}' chevauche '{room_b.label}'",
                ))

    return violations
