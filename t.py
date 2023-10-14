from PIL import Image, ImageFilter, ImageOps
import requests
from io import BytesIO

def process_image(img):
    # Desired ratio
    desired_ratio = 16/9
    current_ratio = img.width / img.height

    if current_ratio > desired_ratio:
        # Too wide
        new_width = img.height * desired_ratio
        offset = (img.width - new_width) / 2
        cropped = img.crop((offset, 0, offset + new_width, img.height))
    elif current_ratio < desired_ratio:
        # Too tall
        new_height = img.width / desired_ratio
        offset = (img.height - new_height) / 2
        cropped = img.crop((0, offset, img.width, offset + new_height))
    else:
        cropped = img

    # Blur the original image
    blurred = img.filter(ImageFilter.BLUR)

    # Paste the cropped image onto the blurred image
    x_offset = (blurred.width - cropped.width) // 2
    y_offset = (blurred.height - cropped.height) // 2

    blurred.paste(cropped, (x_offset, y_offset))

    return blurred

# URL to the image
image_url = "https://cdn36.hipicbeta.com/2023/photo/20230906/9180525875200664f8134bb3143.jpg"

# Download the image content
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# Process and display the image
image = process_image(img)
image.show()
