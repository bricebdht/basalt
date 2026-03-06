"""Tests for the terrain geometry service using the reference terrain.

Reference terrain (parallelogram in Ceará, Brazil):
  Sides: a=19.93, b=12.2
  Angles: α=101.085°, β=78.915°
  Diagonals: e=21.273, f=25.289
  Area: 238.61 m²
"""

import math

import pytest
from shapely.geometry import Polygon

from basalt.services.geometry import (
    compute_vertices,
    sides_angles_to_vertices,
    sides_diagonals_to_vertices,
    validate_polygon,
)

REFERENCE_A = 19.93
REFERENCE_B = 12.2
REFERENCE_ALPHA = 101.085
REFERENCE_AREA = 238.61
REFERENCE_DIAG_E = 21.273


def test_sides_angles_vertices_count():
    verts = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    assert len(verts) == 4


def test_sides_angles_area():
    verts = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    poly = Polygon(verts)
    assert poly.area == pytest.approx(REFERENCE_AREA, abs=0.5)


def test_sides_angles_first_vertex_at_origin():
    verts = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    assert verts[0] == (0.0, 0.0)


def test_sides_angles_side_a_along_x():
    verts = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    assert verts[1][0] == pytest.approx(REFERENCE_A)
    assert verts[1][1] == pytest.approx(0.0)


def test_sides_diagonals_matches_angles():
    verts_from_angles = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    verts_from_diag = sides_diagonals_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_DIAG_E)

    for va, vd in zip(verts_from_angles, verts_from_diag):
        assert va[0] == pytest.approx(vd[0], abs=0.01)
        assert va[1] == pytest.approx(vd[1], abs=0.01)


def test_sides_diagonals_area():
    verts = sides_diagonals_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_DIAG_E)
    poly = Polygon(verts)
    assert poly.area == pytest.approx(REFERENCE_AREA, abs=0.5)


def test_compute_vertices_sides_angles():
    verts = compute_vertices(
        input_mode="sides_angles",
        sides={"a": REFERENCE_A, "b": REFERENCE_B},
        angles_deg={"alpha": REFERENCE_ALPHA},
    )
    assert len(verts) == 4
    assert Polygon(verts).area == pytest.approx(REFERENCE_AREA, abs=0.5)


def test_compute_vertices_sides_diagonals():
    verts = compute_vertices(
        input_mode="sides_diagonals",
        sides={"a": REFERENCE_A, "b": REFERENCE_B},
        diagonals={"e": REFERENCE_DIAG_E},
    )
    assert len(verts) == 4
    assert Polygon(verts).area == pytest.approx(REFERENCE_AREA, abs=0.5)


def test_compute_vertices_coordinates():
    raw = [(0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0)]
    verts = compute_vertices(input_mode="coordinates", vertices=raw)
    assert verts == raw
    assert Polygon(verts).area == pytest.approx(50.0)


def test_compute_vertices_unknown_mode():
    with pytest.raises(ValueError, match="Unknown input_mode"):
        compute_vertices(input_mode="magic")


def test_validate_polygon_valid():
    verts = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    poly = validate_polygon(verts)
    assert poly.area == pytest.approx(REFERENCE_AREA, abs=0.5)


def test_validate_polygon_degenerate():
    with pytest.raises(ValueError):
        validate_polygon([(0, 0), (1, 0), (2, 0)])  # collinear points


def test_diagonal_f_consistent():
    """Verify that the second diagonal f matches expectations."""
    verts = sides_angles_to_vertices(REFERENCE_A, REFERENCE_B, REFERENCE_ALPHA)
    # f = distance from V1 to V3
    dx = verts[3][0] - verts[1][0]
    dy = verts[3][1] - verts[1][1]
    f = math.sqrt(dx**2 + dy**2)
    assert f == pytest.approx(25.289, abs=0.05)
