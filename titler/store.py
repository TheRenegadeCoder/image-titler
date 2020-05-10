from pathlib import Path
from typing import List

import pathvalidate
import piexif
import piexif.helper
import pkg_resources
from PIL import Image

from titler.constants import *


def save_copies(edited_images: List[Image.Image], **kwargs) -> List[str]:
    """
    Saves a list of Pillow images as image files. The typical list of options
    apply and determine what the output file name will look like. For example,
    the title keyword will apply that title to all images in the list. Meanwhile,
    if the title keyword is not present but the filename attribute of edited_image
    is present, then that attribute will be used. Otherwise, a generic file name
    is given (image-titler).

    Currently, image files are given the following name format:

    {title}-featured-image-{software version}.{extension}

    :param edited_images: a list of edited images
    :param kwargs: a set of keyword arguments (see parse_input for options)
    :return: a list of storage paths
    """
    storage_paths = list()
    for index, edited_image in enumerate(edited_images):
        storage_path = _generate_image_output_path(edited_image, index, **kwargs)
        exif = _generate_version_exif(edited_image)
        edited_image.save(storage_path, subsampling=0, quality=100, exif=exif)
        storage_paths.append(storage_path)
    return storage_paths


def _generate_version_exif(image: Image.Image) -> bytes:
    """
    Given an image and version, this function will place that vision in the EXIF data of the file.

    Currently, this function is limited to files that already have EXIF data. Naturally, not
    all files have EXIF data, so I'm not sure how useful this feature is. That said, titler's
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


def _generate_image_output_path(edited_image: Image.Image, index: int, **kwargs) -> str:
    """
    A helper function which generates an image output path from an image and its options.
    If a title exists, this method will use the title as the file name.
    If the image has the filename attribute, that will be used instead.
    Otherwise, a generic file name is created.

    :param edited_image: an image to be stored
    :param index: the index of this image in a set
    :return: the path of the file to be created
    """
    version: str = pkg_resources.require("image-titler")[0].version
    version = version.replace(".", SEPARATOR)
    extension = ".jpg"

    # File name logic
    if title := kwargs.get(KEY_TITLE):
        file_name = pathvalidate.sanitize_filename(title.lower().replace(" ", SEPARATOR))
    elif hasattr(edited_image, 'filename'):
        file_name = Path(edited_image.filename).stem
    else:
        file_name = "image-titler"

    # Extension logic
    if hasattr(edited_image, 'filename'):
        extension = Path(edited_image.filename).suffix

    storage_path = f'{file_name}-v{version}-i{index}{extension}'
    if output_path := kwargs.get("output_path"):
        storage_path = f'{output_path}{os.sep}{storage_path}'
    return storage_path
