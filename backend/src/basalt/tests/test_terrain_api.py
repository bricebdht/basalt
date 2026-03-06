"""Integration tests for the terrain API endpoints."""

from fastapi.testclient import TestClient

from basalt.main import app

client = TestClient(app)

REFERENCE_INPUT = {
    "input_mode": "sides_angles",
    "sides": {"a": 19.93, "b": 12.2},
    "angles_deg": {"alpha": 101.085},
    "setback_distance_m": 3.0,
}


def test_compute_terrain():
    response = client.post("/terrain/compute", json=REFERENCE_INPUT)
    assert response.status_code == 200
    data = response.json()
    assert data["id"]
    assert len(data["vertices"]) == 4
    assert abs(data["area_m2"] - 238.61) < 0.5
    assert data["perimeter_m"] > 0
    assert data["setback_distance_m"] == 3.0
    assert len(data["buildable_polygon"]) >= 3
    assert data["buildable_area_m2"] > 0
    assert data["buildable_area_m2"] < data["area_m2"]


def test_compute_terrain_sides_diagonals():
    response = client.post("/terrain/compute", json={
        "input_mode": "sides_diagonals",
        "sides": {"a": 19.93, "b": 12.2},
        "diagonals": {"e": 21.273},
        "setback_distance_m": 3.0,
    })
    assert response.status_code == 200
    data = response.json()
    assert abs(data["area_m2"] - 238.61) < 0.5


def test_compute_terrain_coordinates():
    response = client.post("/terrain/compute", json={
        "input_mode": "coordinates",
        "vertices": [[0, 0], [10, 0], [10, 5], [0, 5]],
        "setback_distance_m": 1.0,
    })
    assert response.status_code == 200
    data = response.json()
    assert abs(data["area_m2"] - 50.0) < 0.1


def test_compute_terrain_invalid_mode():
    response = client.post("/terrain/compute", json={
        "input_mode": "magic",
    })
    assert response.status_code == 422


def test_get_terrain_by_id():
    # First create a terrain
    create_resp = client.post("/terrain/compute", json=REFERENCE_INPUT)
    terrain_id = create_resp.json()["id"]

    # Then retrieve it
    get_resp = client.get(f"/terrain/{terrain_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == terrain_id


def test_get_terrain_not_found():
    response = client.get("/terrain/nonexistent-id")
    assert response.status_code == 404
