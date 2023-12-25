def crop(image, start_x, start_y, crop_width, crop_height):
    
    # Set minimum crop size
    min_crop_size = 16

    # Check if crop dimensions are large enough
    if crop_width < min_crop_size or crop_height < min_crop_size:
        raise ValueError(f"Crop dimensions {str(crop_width)} x {str(crop_height)} are too small: Use a crop size of {min_crop_size} pixels or larger.")

    # Calculate crop coordinates
    crop_x1 = start_x
    crop_x2 = crop_x1 + crop_width - 1
    crop_y1 = start_y
    crop_y2 = crop_y1 + crop_height - 1

    # Get image dimensions
    image_height, image_width, _ = image.shape

    # Check if crop coordinates are within image dimensions
    if crop_x1 > image_width - 1 or crop_y1 > image_height - 1:
        raise ValueError(f"Crop origin ({crop_x1},{crop_y1} is outside the image dimensions.")
    
    if crop_x2 > image_width - 1 or crop_y2 > image_height - 1:
        raise ValueError(f"Crop end ({crop_x2},{crop_y2} is outside the image dimensions.")
    
    # Crop image
    cropped_image = image[crop_y1:crop_y2, crop_x1:crop_x2]
    
    return cropped_image
