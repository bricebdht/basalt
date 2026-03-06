"""Tests for the SVG export service and API."""

from fastapi.testclient import TestClient

from basalt.main import app

client = TestClient(app)

TERRAIN_INPUT = {
    "input_mode": "sides_angles",
    "sides": {"a": 19.93, "b": 12.2},
    "angles_deg": {"alpha": 101.085},
    "setback_distance_m": 3.0,
}


def test_export_svg_terrain_only():
    resp = client.post("/terrain/compute", json=TERRAIN_INPUT)
    terrain_id = resp.json()["id"]

    resp = client.post("/export/svg", json={"terrain_id": terrain_id, "rooms": []})
    assert resp.status_code == 200
    assert "image/svg+xml" in resp.headers["content-type"]
    assert "<svg" in resp.text
    assert "<polygon" in resp.text


def test_export_svg_with_rooms():
    resp = client.post("/terrain/compute", json=TERRAIN_INPUT)
    terrain_id = resp.json()["id"]

    resp = client.post("/export/svg", json={
        "terrain_id": terrain_id,
        "rooms": [
            {"id": "1", "label": "Bedroom", "x_m": 5, "y_m": 5, "width_m": 4, "height_m": 3},
        ],
    })
    assert resp.status_code == 200
    assert "Bedroom" in resp.text
    assert "<rect" in resp.text


def test_export_svg_terrain_not_found():
    resp = client.post("/export/svg", json={"terrain_id": "nonexistent"})
    assert resp.status_code == 404
