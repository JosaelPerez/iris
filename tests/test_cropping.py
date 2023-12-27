from app.iris.effects import CroppingConfiguration
from app.iris.utils import Point, Dimension, AspectRatio
import pytest

def test_pass_positive_point():
    point = Point(x=100, y=100)
    assert point.x == 100
    assert point.y == 100

def test_pass_zero_point():
    point = Point(x=0, y=0)
    assert point.x == 0
    assert point.y == 0

def test_pass_negative_point():
    point = Point(x=-1, y=-1)
    assert point.x == -1
    assert point.y == -1

def test_pass_positive_dimension():
    dimension = Dimension(width=100, height=100)
    assert dimension.width == 100
    assert dimension.height == 100

def test_pass_zero_dimension():
    dimension = Dimension(width=0, height=0)
    assert dimension.width == 0
    assert dimension.height == 0

def test_pass_negative_dimension():
    dimension = Dimension(width=-1, height=-1)
    assert dimension.width == -1
    assert dimension.height == -1

def test_pass_default_height_dimension():
    dimension = Dimension(width=100)
    assert dimension.width == 100
    assert dimension.height == 0

def test_pass_positive_origin():
    origin = Point(x=100, y=100)
    dimensions = Dimension(width=100, height=100)
    aspect_ratio = AspectRatio.FREE

    configuration = CroppingConfiguration(origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio)
    assert configuration.origin == origin

def test_pass_zero_origin():
    origin = Point(x=0, y=0)
    dimensions = Dimension(width=100, height=100)
    aspect_ratio = AspectRatio.FREE

    configuration = CroppingConfiguration(origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio)
    assert configuration.origin == origin

def test_fail_negative_origin():
    origin = Point(x=-1, y=-1)
    dimensions = Dimension(width=100, height=100)
    aspect_ratio = AspectRatio.FREE

    with pytest.raises(ValueError):
        CroppingConfiguration(origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio)

def test_fail_free_cropping_configuration_to_small_dimensions():
    origin = Point(x=0, y=0)
    dimensions = Dimension(width=10, height=10)
    aspect_ratio = AspectRatio.FREE

    with pytest.raises(ValueError):
        CroppingConfiguration(origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio)

def test_fail_free_cropping_configuration_with_zero_dimensions():
    origin = Point(x=0, y=0)
    dimensions = Dimension(width=0, height=0)
    aspect_ratio = AspectRatio.FREE

    with pytest.raises(ValueError):
        CroppingConfiguration(origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio)