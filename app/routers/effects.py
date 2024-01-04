from fastapi import APIRouter, UploadFile, HTTPException, Depends, status
from fastapi.responses import Response
from app.effects import cropping

router = APIRouter(prefix="/effects", tags=["effects"])


@router.post("/crop")
async def crop(
    image_file: UploadFile,
    configuration: cropping.CroppingConfiguration = Depends(
        cropping.get_cropping_configuration
    ),
):
    # Read uploaded image file
    image_bytes = await image_file.read()

    try:
        cropped_image_bytes = cropping.crop(image_bytes, configuration=configuration)
        return Response(
            content=cropped_image_bytes, media_type="image/jpeg", status_code=200
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
