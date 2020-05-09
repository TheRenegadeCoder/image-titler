from pathlib import Path

import pathvalidate
import piexif
import piexif.helper
import pkg_resources
from PIL import Image
from utilities.constants import *


def save_copy(edited_image: Image.Image, **kwargs) -> str:
    """
    A helper function for saving a copy of the image.

    :param edited_image: the edited image
    :return: the path to the saved image
    """
    storage_path = _generate_image_output_path(**kwargs)
    exif = _generate_version_exif(edited_image)
    edited_image.save(storage_path, subsampling=0, quality=100, exif=exif)
    return storage_path


def _generate_version_exif(image: Image.Image) -> bytes:
    """
    Given an image and version, this function will place that vision in the EXIF data of the file.

    Currently, this function is limited to files that already have EXIF data. Naturally, not
    all files have EXIF data, so I'm not sure how useful this feature is. That said, it's
    a nice start!

    :param image: an image file
    :return: the exif data as a byte string (empty string for images that didn't already have data)
    """
    exif_data = b""
    version: str = pkg_resources.require("image-titler")[0].version
    version = version.replace(".", SEPARATOR)
    if exif := image.info.get('exif'):
        exif_dict = piexif.load(exif)
        exif_dict['Exif'][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(f'image-titler-v{version}')
        exif_data = piexif.dump(exif_dict)
    return exif_data


def _generate_image_output_path(**kwargs) -> str:
    """
    A helper function which generates image output paths from a series of strings.

    :return: the path of the file to be created
    """
    tag = "featured-image"
    version: str = pkg_resources.require("image-titler")[0].version
    version = version.replace(".", SEPARATOR)

    path = kwargs.get("path", "example.jpg")
    extension = Path(path).suffix

    if title := kwargs.get(KEY_TITLE):
        file_name = pathvalidate.sanitize_filename(title.lower().replace(" ", SEPARATOR))
    else:
        file_name = "example"

    storage_path = f'{file_name}-{tag}-v{version}.{extension}'
    if output_path := kwargs.get("output_path"):
        storage_path = f'{output_path}{os.sep}{storage_path}'
    return storage_path
