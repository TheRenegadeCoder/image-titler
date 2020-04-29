import os
from pathlib import Path
from typing import Optional

import pathvalidate
import piexif
import piexif.helper
import pkg_resources
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from titlecase import titlecase

FONT = os.path.join(os.path.dirname(__file__), "BERNHC.TTF")
TEXT_FILL = (255, 255, 255)
RECTANGLE_FILL = (201, 2, 41)
WHITE = (255, 255, 255, 0)

FONT_SIZE = 114
TOP_RECTANGLE_Y = 30
BOTTOM_RECTANGLE_Y = TOP_RECTANGLE_Y + 180
TOP_TEXT_Y = TOP_RECTANGLE_Y + 5
BOTTOM_TEXT_Y = BOTTOM_RECTANGLE_Y + 5
RECTANGLE_HEIGHT = 145
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 960
X_OFFSET = 30
GOLD = (255, 215, 0)
SILVER = (211, 211, 211)
LOGO_SIZE = (RECTANGLE_HEIGHT, RECTANGLE_HEIGHT)
LOGO_PADDING = 30
SEPARATOR = "-"

TIER_MAP = {
    "free": SILVER,
    "premium": GOLD
}

FILE_TYPES = [('image files', ('.png', '.jpg', '.jpeg'))]


def _draw_rectangle(draw: ImageDraw, position: int, width: int, tier: str, color: tuple = RECTANGLE_FILL):
    """
    Draws a rectangle over the image given a ImageDraw object and the intended
    position, width, and tier.

    :param color: the color of the overlay bar
    :param draw: an picture we're editing
    :param position: the position of the rectangle to be added
    :param width: the width of the rectangle to be added
    :param tier: the tier which determines the outline
    :return: nothing
    """
    draw.rectangle(
        (
            (IMAGE_WIDTH - width - X_OFFSET * 2, position),
            (IMAGE_WIDTH, position + RECTANGLE_HEIGHT)
        ),
        fill=color,
        outline=TIER_MAP.get(tier.lower(), None),
        width=7
    )


def _draw_text(draw: ImageDraw, position: int, width: int, text: str, font: ImageFont):
    """
    Draws text on the image.

    :param draw: the picture to edit
    :param position: the position of the text
    :param width: the width of the text
    :param text: the text
    :param font: the font of the text
    :return: nothing
    """
    draw.text(
        (IMAGE_WIDTH - width - X_OFFSET, position),
        text,
        fill=TEXT_FILL,
        font=font
    )


def _draw_overlay(image: Image.Image, title: str, tier: str, color: tuple = RECTANGLE_FILL) -> Image:
    """
    Draws text over an image.

    :param color: the color of the overlay bar
    :param image: an image
    :param title: the image title
    :param tier: the image tier
    :return: the updated image
    """
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, FONT_SIZE)

    # Detect space (precondition for split)
    if len(title.split()) > 1:
        top_half, bottom_half = split_string_by_nearest_middle_space(title)
    else:
        top_half, bottom_half = title, None

    # Draw top
    top_width, top_height = draw.textsize(top_half, font)
    _draw_rectangle(draw, TOP_RECTANGLE_Y, top_width, tier, color)
    _draw_text(draw, TOP_TEXT_Y, top_width, top_half, font)

    # Draw bottom
    if bottom_half:
        bottom_width, bottom_height = draw.textsize(bottom_half, font)
        _draw_rectangle(draw, BOTTOM_RECTANGLE_Y, bottom_width, tier, color)
        _draw_text(draw, BOTTOM_TEXT_Y, bottom_width, bottom_half, font)

    return image


def _draw_logo(img: Image.Image, logo: Image.Image):
    """
    Adds a logo to the image if a path is provided.

    :param img: an image to be modified
    :param logo: the logo file to be added
    :return: nothing
    """
    logo.thumbnail(LOGO_SIZE)
    width, height = img.size
    img.paste(logo, (LOGO_PADDING, height - LOGO_SIZE[1] - LOGO_PADDING), logo)


def _add_version_to_exif(image: Image.Image, version: str) -> bytes:
    """
    Given an image and version, this function will place that vision in the EXIF data of the file.

    Currently, this function is limited to files that already have EXIF data. Naturally, not
    all files have EXIF data, so I'm not sure how useful this feature is. That said, it's
    a nice start!

    :param image: an image file
    :param version: the software version (e.g. 1.9.0)
    :return: the exif data as a byte string (empty string for images that didn't already have data)
    """
    if exif := image.info.get('exif'):
        exif_dict = piexif.load(exif)
        exif_dict['Exif'][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(f'image-titler-v{version}')
        return piexif.dump(exif_dict)
    else:
        return b""


def _generate_image_output_path(extension: str, output_path: Optional[str], title: str, version: str) -> str:
    """
    A helper function which generates image output paths from a series of strings.

    :param extension: the file extension (e.g. png, jpg, etc.)
    :param output_path: the directory where the file is to be stored (e.g. path/to/folder)
    :param title: the title given to the image (e.g. How to Write a Loop in Python)
    :param version: the software version (e.g. 1.9.0)
    :return: the path of the file to be created
    """
    tag = "featured-image"
    file_name = pathvalidate.sanitize_filename(title.lower().replace(" ", SEPARATOR))
    storage_path = f'{file_name}-{tag}-v{version}.{extension}'
    if output_path:
        storage_path = f'{output_path}{os.sep}{storage_path}'
    return storage_path


def split_string_by_nearest_middle_space(input_string: str) -> tuple:
    """
    Splits a string by the nearest middle space. Assumes space is in string.

    :param input_string: some string
    :return: a pair of strings
    """
    index = len(input_string) // 2
    curr_char = input_string[index]
    n = 1
    while not curr_char.isspace():
        index += (-1) ** (n + 1) * n  # thanks wolfram alpha (1, -2, 3, -4, ...)
        curr_char = input_string[index]
        n += 1
    return input_string[:index], input_string[index + 1:]


def save_copy(input_path: str, edited_image: Image.Image, title: Optional[str] = None,
              output_path: Optional[str] = None):
    """
    A helper function for saving a copy of the image.

    :param input_path: the path to the original image
    :param edited_image: the edited image
    :param title: the title of the image
    :param output_path: the path to dump the picture
    :return: nothing
    """
    og_image = Image.open(input_path)
    title = convert_file_name_to_title(input_path, title=title)
    version: str = pkg_resources.require("image-titler")[0].version
    version = version.replace(".", SEPARATOR)
    storage_path = _generate_image_output_path(og_image.format, output_path, title, version)
    exif = _add_version_to_exif(og_image, version)
    edited_image.save(storage_path, subsampling=0, quality=100, exif=exif)


def process_batch(input_path: str, tier: str = "", logo_path: str = None, output_path: str = None) -> None:
    """
    Processes a batch of images.

    :param input_path: the path to a folder of images
    :param tier: the image tier (free or premium)
    :param logo_path: the path to a logo
    :param output_path: the output path of the processed images
    :return: None
    """
    for path in os.listdir(input_path):
        absolute_path = os.path.join(input_path, path)
        title = convert_file_name_to_title(absolute_path)
        edited_image = process_image(
            absolute_path,
            title,
            tier=tier,
            logo_path=logo_path
        )
        save_copy(absolute_path, edited_image, output_path=output_path)


def convert_file_name_to_title(file_path: str, separator: str = SEPARATOR, title: Optional[str] = None) -> str:
    """
    A helper method which converts file names into titles.

    :param title: the requested title of the image, if provided
    :param separator: the word separator (default "-")
    :param file_path: the path to an image file
    :return: a title string
    """
    if not title:
        file_path = Path(file_path).resolve().stem
        title = titlecase(file_path.replace(separator, ' '))
    return title


def process_image(input_path: str, title: str, tier: str = "", logo_path: Optional[str] = None) -> Image.Image:
    """
    Processes a single image.

    :param input_path: the path of an image
    :param tier: the image tier (free or premium)
    :param logo_path: the path to a logo
    :param title: the title of the processed image
    :return: the edited image
    """
    img = Image.open(input_path)
    cropped_img: Image = img.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
    color = RECTANGLE_FILL
    if logo_path:
        logo: Image.Image = Image.open(logo_path)
        color = get_best_top_color(logo)
        _draw_logo(cropped_img, logo)
    edited_image = _draw_overlay(cropped_img, title, tier, color)
    return edited_image


def get_best_top_color(image: Image.Image) -> tuple:
    """
    Computes the most popular non-white color from an image.

    :param image: an image file
    :return: the most dominant color as a tuple
    """
    top_colors = sorted(image.getcolors(image.size[0] * image.size[1]), reverse=True)
    curr_color = iter(top_colors)
    while (color := next(curr_color)[1]) == WHITE:
        pass
    return color
