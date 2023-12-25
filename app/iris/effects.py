from pydantic import BaseModel
from app.iris.utils import Coordinate, Dimension, Orientation, AspectRatio

class CroppingConfiguration(BaseModel):
    origin: Coordinate
    dimensions: Dimension
    orientation : Orientation
    aspect_ratio: AspectRatio

def _crop(image, origin: Coordinate, dimensions: Dimension):
    
    # Set minimum crop size
    min_crop_size = 16

    # Check if crop dimensions are large enough
    if dimensions.width < min_crop_size or dimensions.height < min_crop_size:
        raise ValueError(f"Crop dimensions {str(dimensions.width)} x {str(dimensions.height)} are too small: Use a crop size of {min_crop_size} pixels or larger.")

    # Calculate crop origins
    crop_x1 = origin.x
    crop_x2 = crop_x1 + dimensions.width - 1
    crop_y1 = origin.y
    crop_y2 = crop_y1 + dimensions.height - 1

    # Get image dimensions
    image_height, image_width, _ = image.shape

    # Check if crop origins are within image dimensions
    if crop_x1 > image_width - 1 or crop_y1 > image_height - 1:
        raise ValueError(f"Crop origin ({crop_x1},{crop_y1} is outside the image dimensions.")
    
    if crop_x2 > image_width - 1 or crop_y2 > image_height - 1:
        raise ValueError(f"Crop end ({crop_x2},{crop_y2} is outside the image dimensions.")
    
    # Crop image
    cropped_image = image[crop_y1:crop_y2, crop_x1:crop_x2]
    
    return cropped_image

class EffectsFactory:

    @staticmethod
    def create_cropping_function(configuration):
        aspect_ratio = configuration.aspect_ratio
        orientation = configuration.orientation

       # Calculate crop height based on aspect ratio and orientation using match-case statement
        match (aspect_ratio, orientation):
            case (AspectRatio.CUSTOM, None):
                crop_height = configuration.dimensions.height

            case (AspectRatio.SQUARE, None):
                crop_height = configuration.dimensions.width

            case (AspectRatio.THREE_TWO, Orientation.LANDSCAPE):
                crop_height = int(configuration.dimensions.width * 2 / 3)

            case (AspectRatio.THREE_TWO, Orientation.PORTRAIT):
                crop_height = int(configuration.dimensions.width * 3 / 2)

            case (AspectRatio.FOUR_THREE, Orientation.LANDSCAPE):
                crop_height = int(configuration.dimensions.width * 3 / 4)

            case (AspectRatio.FOUR_THREE, Orientation.PORTRAIT):
                crop_height = int(configuration.dimensions.width * 4 / 3)

            case (AspectRatio.FIVE_FOUR, Orientation.LANDSCAPE):
                crop_height = int(configuration.dimensions.width * 4 / 5)

            case (AspectRatio.FIVE_FOUR, Orientation.PORTRAIT):
                crop_height = int(configuration.dimensions.width * 5 / 4)

            case (AspectRatio.SIXTEEN_NINE, Orientation.LANDSCAPE):
                crop_height = int(configuration.dimensions.width * 9 / 16)

            case (AspectRatio.SIXTEEN_NINE, Orientation.PORTRAIT):
                crop_height = int(configuration.dimensions.width * 16 / 9)

            case (AspectRatio.SIXTEEN_TEN, Orientation.LANDSCAPE):
                crop_height = int(configuration.dimensions.width * 10 / 16)

            case (AspectRatio.SIXTEEN_TEN, Orientation.PORTRAIT):
                crop_height = int(configuration.dimensions.width * 16 / 10)

            case _:
                raise ValueError("Invalid aspect ratio or orientation.")
        
        if crop_height <= 0:
            raise ValueError("Calculated crop height is invalid.")

        # Create a lambda function to perform the cropping operation based on the calculated crop height
        cropping_function = lambda image, origin, dimensions: _crop(image, origin, Dimension(width=dimensions.width, height=crop_height))

        return cropping_function