import base64
from io import BytesIO
from PIL import Image

def image_to_base64(image_path, image_format):
    '''
    Convert an image to base64 format.

    Parameters:
    image_path (str): The path to the image.
    image_format (str): The format of the image.

    Returns:
    str: The image in base64 format.
    '''
    pil_image = Image.open(image_path)
    image_file = BytesIO()
    pil_image.save(image_file, format=image_format)
    image_base64 = base64.b64encode(image_file.getvalue()).decode()

    return f'data:image/{image_format};base64,{image_base64}'
