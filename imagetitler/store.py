from pathlib import Path
from typing import List

import pathvalidate
import piexif
import piexif.helper
import pkg_resources
from PIL import Image

from imagetitler.constants import *


def save_copies(edited_images: List[Image.Image], **kwargs) -> List[str]:
    """
    Saves a list of Pillow images as image files. The typical list of options
    apply and determine what the output file name will look like. For example,
    the title keyword will apply that title to all images in the list. Meanwhile,
    if the title keyword is not present but the filename attribute of edited_image
    is present, then that attribute will be used. Otherwise, a generic file name
    is given (image-titler).

    Note: the batch setting must be present to process more than one image.

    Currently, image files are given the following name format:

    {title}-featured-image-{software version}.{extension}

    :param edited_images: a list of edited images
    :param kwargs: a set of keyword arguments (see parse_input for options)
    :return: a list of storage paths
    """
    storage_paths = list()
    if not kwargs.get(KEY_BATCH):  # batch must be turned on to process multiple images
        edited_images = edited_images[:1]
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


def _get_file_name(edited_image: Image.Image, **kwargs) -> str:
    """
    Retrieve the underlying file name from the edited_image or
    the set of kwargs. Priority goes as follows:

    1. title option
    2. original file name
    3. path option
    4. fallback (e.g. image-titler)

    :param edited_image: the edited image
    :param kwargs: the set of options
    :return: the file name without the extension (e.g. image-titler)
    """
    if title := kwargs.get(KEY_TITLE):
        file_name = pathvalidate.sanitize_filename(title.lower().replace(" ", SEPARATOR))
    elif hasattr(edited_image, 'filename'):
        file_name = Path(edited_image.filename).stem
    elif path := kwargs.get(KEY_PATH):
        file_name = Path(path).stem if Path(path).is_file() else "image-titler"
    else:
        file_name = "image-titler"
    return file_name


def _get_extension(edited_image: Image.Image) -> str:
    """
    Gets the extension for the new image.

    :param edited_image: the edited image
    :return: the file extension with the dot (e.g. ".jpg")
    """
    extension = ".jpg"
    if hasattr(edited_image, 'filename'):
        extension = Path(edited_image.filename).suffix
    return extension


def _get_index(index: int, **kwargs) -> str:
    """
    Gets the index of the output path given the index and some options.
    This returns "-i{index}" iff the batch and title options are truthy.
    Otherwise, it generates an empty string.

    :param index: the current index of the image
    :param kwargs: a set of options
    :return: a string in the form of a file name tag (e.g. -i17) or an empty string
    """
    i = ""
    if kwargs.get(KEY_BATCH) and kwargs.get(KEY_TITLE):
        i = f'-i{index}'
    return i


def _get_version() -> str:
    """
    Gets the version of the image-titler and places in a string as follows: -v{version}

    :return: the package version as a string (e.g. -v2.0.1)
    """
    version = pkg_resources.require("image-titler")[0].version
    version = version.replace(".", SEPARATOR)
    return f'-v{version}'


def _get_output_path(**kwargs) -> str:
    """
    Gets the output path option if it exists. Otherwise, returns an empty string.

    :param kwargs: a set of options
    :return: the output path or an emtpy string
    """
    if not (output_path := kwargs.get("output_path")):
        output_path = ""
    if output_path:
        output_path += "/"
    return output_path


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
    version: str = _get_version()
    file_name = _get_file_name(edited_image, **kwargs)
    extension = _get_extension(edited_image)
    index = _get_index(index, **kwargs)
    output_path = _get_output_path(**kwargs)
    storage_path = f'{output_path}{file_name}{version}{index}{extension}'
    return storage_path
