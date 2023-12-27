from app.iris.effects import CroppingConfiguration
from app.iris.utils import Point, Dimension, AspectRatio


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
