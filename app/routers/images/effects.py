from fastapi import APIRouter, UploadFile
from app.iris.effects import EffectsFactory, CroppingConfiguration

router = APIRouter(prefix="/images/effects", tags=["effects"] )

@router.post("/crop")
async def crop(image_file: UploadFile, configuration: CroppingConfiguration):
    # Read uploaded image file
    image = await image_file.read()

    cropping_function = EffectsFactory.create_cropping_function(configuration)
    cropping_function(image, configuration.origin, configuration.dimensions)

    # Return a success message or the cropped image data
    return {"data": "Image cropped successfully with the provided configuration"}