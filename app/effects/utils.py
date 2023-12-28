from pydantic import BaseModel
from enum import Enum


class Point(BaseModel):
    x: int
    y: int


class Dimension(BaseModel):
    width: int
    height: int = 0


class Orientation(str, Enum):
    LANDSCAPE = 'landscape'
    PORTRAIT = 'portrait'


class AspectRatio(str, Enum):
    FREE = 'free'
    SQUARE = 'square'
    THREE_TWO = 'three-two'
    FOUR_THREE = 'four-three'
    FIVE_FOUR = 'five-four'
    SIXTEEN_NINE = 'sixteen-nine'
    SIXTEEN_TEN = 'sixteen-ten'
