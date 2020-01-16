from __app__.utils.storage.images import (
    save_image as new_save_image,
    get_image as new_get_image,
)

def save_image(image: str, url: str) -> str:
    return new_save_image(image, url)


def get_image(url: str) -> str:
    new_get_image(url)
