"""SVG export service: render terrain + rooms as SVG."""

import svgwrite

from basalt.schemas.layout import Room
from basalt.schemas.terrain import TerrainResponse

# SVG pixels per meter
SVG_SCALE = 30

PHASE_COLORS = {
    1: "#a8d8ea",
    2: "#f4b183",
}


def _to_svg_coords(
    vertices: list[tuple[float, float]], scale: float, offset_x: float, offset_y: float
) -> list[tuple[float, float]]:
    """Convert meter coords to SVG coords (flip y-axis)."""
    return [(x * scale + offset_x, -y * scale + offset_y) for x, y in vertices]


def render_svg(terrain: TerrainResponse, rooms: list[Room]) -> str:
    """Render a complete plan as an SVG string."""
    # Compute bounding box in meters
    xs = [v[0] for v in terrain.vertices]
    ys = [v[1] for v in terrain.vertices]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    margin = 2  # meters
    width_m = max_x - min_x + margin * 2
    height_m = max_y - min_y + margin * 2

    svg_w = width_m * SVG_SCALE
    svg_h = height_m * SVG_SCALE
    offset_x = (-min_x + margin) * SVG_SCALE
    offset_y = (max_y + margin) * SVG_SCALE  # flip y

    dwg = svgwrite.Drawing(size=(f"{svg_w}px", f"{svg_h}px"))
    dwg.viewbox(0, 0, svg_w, svg_h)

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(svg_w, svg_h), fill="white"))

    # Terrain polygon
    terrain_pts = _to_svg_coords(terrain.vertices, SVG_SCALE, offset_x, offset_y)
    dwg.add(dwg.polygon(
        points=terrain_pts,
        fill="#c8dcc8",
        fill_opacity=0.15,
        stroke="#333",
        stroke_width=2,
    ))

    # Setback zone (buildable boundary)
    if terrain.buildable_polygon:
        buildable_pts = _to_svg_coords(terrain.buildable_polygon, SVG_SCALE, offset_x, offset_y)
        dwg.add(dwg.polygon(
            points=buildable_pts,
            fill="none",
            stroke="#e53e3e",
            stroke_width=1,
            stroke_dasharray="6,4",
        ))

    # Rooms
    for room in rooms:
        rx = room.x_m * SVG_SCALE + offset_x
        ry = -room.y_m * SVG_SCALE + offset_y - room.height_m * SVG_SCALE
        rw = room.width_m * SVG_SCALE
        rh = room.height_m * SVG_SCALE
        color = PHASE_COLORS.get(room.phase, "#ccc")

        # Outer rect (with walls)
        dwg.add(dwg.rect(
            insert=(rx, ry),
            size=(rw, rh),
            fill=color,
            stroke="#333",
            stroke_width=1,
            opacity=0.8,
        ))

        # Inner rect (habitable space)
        wt = room.wall_thickness_m * SVG_SCALE
        if wt > 0 and rw > 2 * wt and rh > 2 * wt:
            dwg.add(dwg.rect(
                insert=(rx + wt, ry + wt),
                size=(rw - 2 * wt, rh - 2 * wt),
                fill="white",
                stroke="none",
                opacity=0.6,
            ))

        # Label
        inner_w = room.width_m - 2 * room.wall_thickness_m
        inner_h = room.height_m - 2 * room.wall_thickness_m
        label = f"{room.label}\n{inner_w:.1f} × {inner_h:.1f}m"
        dwg.add(dwg.text(
            label,
            insert=(rx + rw / 2, ry + rh / 2),
            text_anchor="middle",
            dominant_baseline="middle",
            font_size="10px",
            font_family="sans-serif",
            fill="#333",
        ))

    # Scale bar (5m)
    bar_y = svg_h - 15
    bar_x = 15
    bar_len = 5 * SVG_SCALE
    dwg.add(dwg.line(start=(bar_x, bar_y), end=(bar_x + bar_len, bar_y), stroke="#333", stroke_width=2))
    dwg.add(dwg.line(start=(bar_x, bar_y - 4), end=(bar_x, bar_y + 4), stroke="#333", stroke_width=1))
    dwg.add(dwg.line(
        start=(bar_x + bar_len, bar_y - 4),
        end=(bar_x + bar_len, bar_y + 4),
        stroke="#333",
        stroke_width=1,
    ))
    dwg.add(dwg.text(
        "5m",
        insert=(bar_x + bar_len / 2, bar_y - 6),
        text_anchor="middle",
        font_size="10px",
        font_family="sans-serif",
        fill="#333",
    ))

    return dwg.tostring()
