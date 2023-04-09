import requests
from PIL import Image
from io import BytesIO

def get_image(url: str) -> Image:
    """Return a image"""
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    return img