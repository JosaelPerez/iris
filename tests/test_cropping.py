from fastapi.testclient import TestClient
import pytest
from app.effects.cropping import CroppingConfiguration
from app.effects.utils import Point, Dimension, AspectRatio, Orientation
from app.main import app


client = TestClient(app)


@pytest.mark.parametrize(
    "x, y", [(100, 100), (0, 0), (-1, -1)], ids=["positive", "zero", "negative"]
)
def test_pass_point(x: int, y: int):
    point = Point(x=x, y=y)
    assert point.x == x
    assert point.y == y


@pytest.mark.parametrize(
    "width, height",
    [(100, 100), (0, 0), (-1, -1)],
    ids=["positive", "zero", "negative"],
)
def test_pass_dimension(width: int, height: int):
    dimension = Dimension(width=width, height=height)
    assert dimension.width == width
    assert dimension.height == height


def test_pass_default_height_dimension():
    dimension = Dimension(width=100)
    assert dimension.width == 100
    assert dimension.height == 0


@pytest.mark.parametrize("x, y", [(100, 100), (0, 0)], ids=["positive", "zero"])
def test_pass_cropping_configuration_origin(x: int, y: int):
    origin = Point(x=x, y=y)
    dimensions = Dimension(width=100, height=100)
    aspect_ratio = AspectRatio.FREE

    configuration = CroppingConfiguration(
        origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio
    )
    assert configuration.origin == origin


def test_fail_cropping_configuration_negative_origin():
    origin = Point(x=-1, y=-1)
    dimensions = Dimension(width=100, height=100)
    aspect_ratio = AspectRatio.FREE

    with pytest.raises(ValueError):
        CroppingConfiguration(
            origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio
        )


def test_fail_free_cropping_configuration_too_small_dimensions():
    origin = Point(x=0, y=0)
    dimensions = Dimension(width=10, height=10)
    aspect_ratio = AspectRatio.FREE

    with pytest.raises(ValueError):
        CroppingConfiguration(
            origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio
        )


def test_fail_free_cropping_configuration_with_zero_dimensions():
    origin = Point(x=0, y=0)
    dimensions = Dimension(width=0, height=0)
    aspect_ratio = AspectRatio.FREE

    with pytest.raises(ValueError):
        CroppingConfiguration(
            origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio
        )


@pytest.mark.parametrize(
    "aspect_ratio",
    [
        AspectRatio.SQUARE,
        AspectRatio.THREE_TWO,
        AspectRatio.FOUR_THREE,
        AspectRatio.FIVE_FOUR,
        AspectRatio.SIXTEEN_NINE,
        AspectRatio.SIXTEEN_TEN,
    ],
)
def test_fail_default_cropping_configuration_with_height(aspect_ratio: AspectRatio):
    origin = Point(x=0, y=0)
    dimensions = Dimension(width=100, height=100)

    with pytest.raises(ValueError):
        CroppingConfiguration(
            origin=origin, dimensions=dimensions, aspect_ratio=aspect_ratio
        )


@pytest.fixture
def image():
    return open("tests/images/forest.jpg", "rb").read()


@pytest.mark.parametrize(
    "origin_x, origin_y, width, height, aspect_ratio, orientation",
    [
        (0, 0, 100, 100, AspectRatio.FREE.value, None),
        (0, 0, 100, None, AspectRatio.SQUARE.value, None),
        (0, 0, 100, None, AspectRatio.THREE_TWO.value, Orientation.PORTRAIT.value),
        (0, 0, 200, None, AspectRatio.THREE_TWO.value, Orientation.LANDSCAPE.value),
        (0, 0, 100, None, AspectRatio.FOUR_THREE.value, Orientation.PORTRAIT.value),
        (0, 0, 200, None, AspectRatio.FOUR_THREE.value, Orientation.LANDSCAPE.value),
        (0, 0, 100, None, AspectRatio.FIVE_FOUR.value, Orientation.PORTRAIT.value),
        (0, 0, 200, None, AspectRatio.FIVE_FOUR.value, Orientation.LANDSCAPE.value),
        (0, 0, 100, None, AspectRatio.SIXTEEN_NINE.value, Orientation.PORTRAIT.value),
        (0, 0, 200, None, AspectRatio.SIXTEEN_NINE.value, Orientation.LANDSCAPE.value),
        (0, 0, 100, None, AspectRatio.SIXTEEN_TEN.value, Orientation.PORTRAIT.value),
        (0, 0, 200, None, AspectRatio.SIXTEEN_TEN.value, Orientation.LANDSCAPE.value),
    ],
    ids=[
        "free_cropping",
        "square_cropping",
        "three_two_portrait_cropping",
        "three_two_landscape_cropping",
        "four_three_portrait_cropping",
        "four_three_landscape_cropping",
        "five_four_portrait_cropping",
        "five_four_landscape_cropping",
        "sixteen_nine_portrait_cropping",
        "sixteen_nine_landscape_cropping",
        "sixteen_ten_portrait_cropping",
        "sixteen_ten_landscape_cropping",
    ],
)
def test_pass_http_crop(
    image: bytes,
    origin_x: int,
    origin_y: int,
    width: int,
    height: int | None,
    aspect_ratio: str | None,
    orientation: str | None,
):
    data = {
        "origin_x": origin_x,
        "origin_y": origin_y,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "orientation": orientation,
    }

    response = client.post(
        url="/effects/crop",
        data=data,
        files={"image_file": ("image_bytes.jpg", image, "image/jpeg")},
    )

    assert response.status_code == 200
