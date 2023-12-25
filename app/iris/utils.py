from pydantic import BaseModel
from enum import Enum, auto

class Coordinate(BaseModel):
    x: int
    y: int

class Dimension(BaseModel):
    width: int
    height: int

class Orientation(str, Enum):
    LANDSCAPE = auto()
    PORTRAIT = auto()

class AspectRatio(str , Enum):
    CUSTOM = auto()
    SQUARE = auto()
    THREE_TWO = auto()
    FOUR_THREE = auto()
    FIVE_FOUR = auto()
    SIXTEEN_NINE = auto()
    SIXTEEN_TEN = auto()