import cv2 as cv
import numpy as np
from pydantic import BaseModel, field_validator, model_validator
from app.iris.utils import Point, Dimension, Orientation, AspectRatio
from fastapi import Form, HTTPException, status

# Set minimum crop size
minimun_cropping_size = 16

def get_cropping_configuration(
    origin_x: int = Form(...),
    origin_y: int = Form(...),
    width: int = Form(...),
    height: int | None = Form(None),
    aspect_ratio: str = Form(...),
    orientation: str | None = Form(None)
) -> 'CroppingConfiguration':
    try:
        if height:
            return CroppingConfiguration(
                origin=Point(x=origin_x, y=origin_y),
                dimensions=Dimension(
                    width=width, height=height),
                aspect_ratio=AspectRatio(aspect_ratio),
                orientation=Orientation(
                    orientation) if orientation is not None else None
            )
        else:
            return CroppingConfiguration(
                origin=Point(x=origin_x, y=origin_y),
                dimensions=Dimension(width=width),
                aspect_ratio=AspectRatio(aspect_ratio),
                orientation=Orientation(
                    orientation) if orientation is not None else None
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class CroppingConfiguration(BaseModel):
    origin: Point
    dimensions: Dimension
    aspect_ratio: AspectRatio
    orientation: Orientation | None = None

    @field_validator('origin')
    @classmethod
    def check_origin(cls, origin: Point) -> 'Point':
        if origin.x < 0 or origin.y < 0:
            raise ValueError(f"Origin point ({origin.x},{origin.y}) must be greater or equal to 0.")
        return origin

    @model_validator(mode='after')
    def check_configuration(self) -> 'CroppingConfiguration':
        if self.aspect_ratio == AspectRatio.FREE:
            if not self.dimensions.width or not self.dimensions.height:
                raise ValueError(f"Free cropping requires both width and height dimensions.")

            if self.dimensions.width < minimun_cropping_size or self.dimensions.height < minimun_cropping_size:
                raise ValueError(f"Dimensions = {self.dimensions.width}x{self.dimensions.height} must be greater or equal to {minimun_cropping_size}x{minimun_cropping_size} pixels.")

        else:
            if self.dimensions.height:
                raise ValueError(f"Default aspect ratio '{self.aspect_ratio.value}' cannot be used with a custom height.")

            if self.dimensions.width < minimun_cropping_size:
                raise ValueError(f"Width dimension = '{self.dimensions.width}' must be greater or equal to {minimun_cropping_size} pixels.")

            if self.aspect_ratio == AspectRatio.SQUARE:
                if self.orientation is not None:
                    raise ValueError(f"Default aspect ratio '{self.aspect_ratio.value}' cannot be used with an orientation.")

                self.dimensions.height = self.dimensions.width

            else:
                if self.orientation is None:
                    raise ValueError(f"Default aspect ratio '{self.aspect_ratio.value}' requires an orientation.")

                # Calculate crop self.dimensions.height based on aspect ratio and self.orientation
                match (self.aspect_ratio, self.orientation):
                    case (AspectRatio.THREE_TWO, self.orientation.LANDSCAPE):
                        self.dimensions.height = int(
                            self.dimensions.width * 2 / 3)

                    case (AspectRatio.THREE_TWO, self.orientation.PORTRAIT):
                        self.dimensions.height = int(
                            self.dimensions.width * 3 / 2)

                    case (AspectRatio.FOUR_THREE, self.orientation.LANDSCAPE):
                        self.dimensions.height = int(
                            self.dimensions.width * 3 / 4)

                    case (AspectRatio.FOUR_THREE, self.orientation.PORTRAIT):
                        self.dimensions.height = int(
                            self.dimensions.width * 4 / 3)

                    case (AspectRatio.FIVE_FOUR, self.orientation.LANDSCAPE):
                        self.dimensions.height = int(
                            self.dimensions.width * 4 / 5)

                    case (AspectRatio.FIVE_FOUR, self.orientation.PORTRAIT):
                        self.dimensions.height = int(
                            self.dimensions.width * 5 / 4)

                    case (AspectRatio.SIXTEEN_NINE, self.orientation.LANDSCAPE):
                        self.dimensions.height = int(
                            self.dimensions.width * 9 / 16)

                    case (AspectRatio.SIXTEEN_NINE, self.orientation.PORTRAIT):
                        self.dimensions.height = int(
                            self.dimensions.width * 16 / 9)

                    case (AspectRatio.SIXTEEN_TEN, self.orientation.LANDSCAPE):
                        self.dimensions.height = int(
                            self.dimensions.width * 10 / 16)

                    case (AspectRatio.SIXTEEN_TEN, self.orientation.PORTRAIT):
                        self.dimensions.height = int(
                            self.dimensions.width * 16 / 10)

                    case _:
                        raise ValueError(f"Aspect ratio '{self.aspect_ratio.value}' with orientation '{self.orientation}' is not supported.")

                if self.dimensions.height < minimun_cropping_size:
                    raise ValueError(f"Height dimension = '{self.dimensions.height}' must be greater or equal to {minimun_cropping_size} pixels.")

        return self


def crop(image_bytes: bytes, configuration: CroppingConfiguration) -> bytes:

    # Load image
    image = cv.imdecode(np.frombuffer(image_bytes, np.uint8), cv.IMREAD_COLOR)

    # Calculate crop start and end points (diagonal)
    crop_x1 = configuration.origin.x
    crop_x2 = crop_x1 + configuration.dimensions.width - 1
    crop_y1 = configuration.origin.y
    crop_y2 = crop_y1 + configuration.dimensions.height - 1

    # Get image dimensions
    image_height, image_width, _ = image.shape

    # Check if crop origins are within image dimensions
    if crop_x1 > image_width - 1 or crop_y1 > image_height - 1:
        raise ValueError(
            f"Crop origin ({crop_x1},{crop_y1} is outside the image dimensions.")

    if crop_x2 > image_width - 1 or crop_y2 > image_height - 1:
        raise ValueError(
            f"Crop end ({crop_x2},{crop_y2} is outside the image dimensions.")

    # Crop image
    cropped_image = image[crop_y1:crop_y2, crop_x1:crop_x2]

    return cv.imencode(".jpg", cropped_image)[1].tobytes()
