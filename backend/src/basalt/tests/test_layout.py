"""Tests for the layout validation service and API."""

from fastapi.testclient import TestClient

from basalt.main import app
from basalt.schemas.layout import Room
from basalt.services.geometry import sides_angles_to_vertices
from basalt.services.layout import validate_layout
from basalt.services.setback import compute_buildable_polygon

client = TestClient(app)

TERRAIN_VERTS = sides_angles_to_vertices(19.93, 12.2, 101.085)
BUILDABLE_VERTS, _ = compute_buildable_polygon(TERRAIN_VERTS, setback_m=3.0)

TERRAIN_INPUT = {
    "input_mode": "sides_angles",
    "sides": {"a": 19.93, "b": 12.2},
    "angles_deg": {"alpha": 101.085},
    "setback_distance_m": 3.0,
}


def _make_room(id: str, label: str, x: float, y: float, w: float, h: float) -> Room:
    return Room(id=id, label=label, x_m=x, y_m=y, width_m=w, height_m=h)


# ── Service tests ────────────────────────────────────────────────────────────


def test_valid_layout():
    rooms = [_make_room("1", "Bedroom", 5.0, 5.0, 4.0, 3.0)]
    violations = validate_layout(TERRAIN_VERTS, BUILDABLE_VERTS, rooms)
    assert violations == []


def test_setback_violation():
    # Place room at origin — inside terrain but outside buildable area
    rooms = [_make_room("1", "Bedroom", 0.5, 0.5, 3.0, 3.0)]
    violations = validate_layout(TERRAIN_VERTS, BUILDABLE_VERTS, rooms)
    types = [v.type for v in violations]
    assert "setback_violation" in types or "out_of_bounds" in types


def test_out_of_bounds():
    rooms = [_make_room("1", "Bedroom", 50.0, 50.0, 4.0, 3.0)]
    violations = validate_layout(TERRAIN_VERTS, BUILDABLE_VERTS, rooms)
    assert any(v.type == "out_of_bounds" for v in violations)


def test_overlap():
    rooms = [
        _make_room("1", "Bedroom 1", 5.0, 5.0, 4.0, 3.0),
        _make_room("2", "Bedroom 2", 6.0, 6.0, 4.0, 3.0),
    ]
    violations = validate_layout(TERRAIN_VERTS, BUILDABLE_VERTS, rooms)
    assert any(v.type == "overlap" for v in violations)


def test_touching_rooms_no_overlap():
    rooms = [
        _make_room("1", "Room A", 5.0, 5.0, 2.0, 2.0),
        _make_room("2", "Room B", 7.0, 5.0, 2.0, 2.0),  # adjacent, touching
    ]
    violations = validate_layout(TERRAIN_VERTS, BUILDABLE_VERTS, rooms)
    assert not any(v.type == "overlap" for v in violations)


# ── API tests ────────────────────────────────────────────────────────────────


def test_validate_api_valid():
    # First create a terrain
    resp = client.post("/terrain/compute", json=TERRAIN_INPUT)
    terrain_id = resp.json()["id"]

    resp = client.post("/layout/validate", json={
        "terrain_id": terrain_id,
        "rooms": [{"id": "1", "label": "Bedroom", "x_m": 5, "y_m": 5, "width_m": 4, "height_m": 3}],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert data["violations"] == []


def test_validate_api_with_violation():
    resp = client.post("/terrain/compute", json=TERRAIN_INPUT)
    terrain_id = resp.json()["id"]

    resp = client.post("/layout/validate", json={
        "terrain_id": terrain_id,
        "rooms": [{"id": "1", "label": "Bedroom", "x_m": 0, "y_m": 0, "width_m": 4, "height_m": 3}],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is False
    assert len(data["violations"]) > 0


def test_validate_api_terrain_not_found():
    resp = client.post("/layout/validate", json={
        "terrain_id": "nonexistent",
        "rooms": [],
    })
    assert resp.status_code == 404
