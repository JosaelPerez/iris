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

def crop_square(image, start_x, start_y, crop_size):
    cropped_image = crop(image, start_x, start_y, crop_size, crop_size)
    return cropped_image

def crop_3_2_landscape(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 3:2 ratio
    crop_height = int(crop_width * 2 / 3)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_3_2_portrait(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 3:2 ratio
    crop_height = int(crop_width * 3 / 2)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_4_3_landscape(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 4:3 ratio
    crop_height = int(crop_width * 3 / 4)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_4_3_portrait(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 4:3 ratio
    crop_height = int(crop_width * 4 / 3)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_5_4_landscape(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 5:4 ratio
    crop_height = int(crop_width * 4 / 5)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_5_4_portrait(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 5:4 ratio
    crop_height = int(crop_width * 5 / 4)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_16_9_landscape(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 16:9 ratio
    crop_height = int(crop_width * 9 / 16)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_16_9_portrait(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 16:9 ratio
    crop_height = int(crop_width * 16 / 9)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_16_10_landscape(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 16:10 ratio
    crop_height = int(crop_width * 10 / 16)
    return crop(image, start_x, start_y, crop_width, crop_height)

def crop_16_10_portrait(image, start_x, start_y, crop_width):
    # Calculate corresponding height for 16:10 ratio
    crop_height = int(crop_width * 16 / 10)
    return crop(image, start_x, start_y, crop_width, crop_height)