"""Tests for the setback computation service."""

import pytest
from shapely.geometry import Polygon

from basalt.services.geometry import sides_angles_to_vertices
from basalt.services.setback import compute_buildable_polygon

REFERENCE_VERTICES = sides_angles_to_vertices(19.93, 12.2, 101.085)


def test_buildable_polygon_is_inside_terrain():
    buildable_verts, _ = compute_buildable_polygon(REFERENCE_VERTICES, setback_m=3.0)
    terrain = Polygon(REFERENCE_VERTICES)
    buildable = Polygon(buildable_verts)
    assert terrain.contains(buildable)


def test_buildable_area_is_smaller():
    _, buildable_area = compute_buildable_polygon(REFERENCE_VERTICES, setback_m=3.0)
    terrain = Polygon(REFERENCE_VERTICES)
    assert buildable_area < terrain.area
    assert buildable_area > 0


def test_zero_setback_returns_same_area():
    _, buildable_area = compute_buildable_polygon(REFERENCE_VERTICES, setback_m=0.0)
    terrain = Polygon(REFERENCE_VERTICES)
    assert buildable_area == pytest.approx(terrain.area, abs=0.1)


def test_huge_setback_returns_empty():
    buildable_verts, buildable_area = compute_buildable_polygon(
        REFERENCE_VERTICES, setback_m=100.0
    )
    assert buildable_verts == []
    assert buildable_area == 0.0


def test_buildable_vertices_are_not_empty():
    buildable_verts, _ = compute_buildable_polygon(REFERENCE_VERTICES, setback_m=3.0)
    assert len(buildable_verts) >= 3
