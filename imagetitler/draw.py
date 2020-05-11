"""
The functional backend to the image-titler script.
"""
from pathlib import Path
from typing import Optional, List

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from titlecase import titlecase

from imagetitler.constants import *

TEXT_FILL = (255, 255, 255)
RECTANGLE_FILL = (201, 2, 41)
WHITE = (255, 255, 255, 0)

FONT_SIZE = 114
TOP_RECTANGLE_Y = 30
BOTTOM_RECTANGLE_Y = TOP_RECTANGLE_Y + 180
BOTTOM_TEXT_Y = BOTTOM_RECTANGLE_Y + 5
RECTANGLE_HEIGHT = 145
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 960
X_OFFSET = 30
LOGO_SIZE = (RECTANGLE_HEIGHT, RECTANGLE_HEIGHT)
LOGO_PADDING = 30


def process_images(**kwargs) -> List[Image.Image]:
    """
    The main entry point for any image editing. This function
    will never return an empty list. If no settings are provided,
    this function will return a default image with a default title.

    :return: None
    """
    is_batch: bool = kwargs.get(KEY_BATCH)
    images = list()
    if is_batch:
        kwargs[KEY_PATH] = kwargs.get(KEY_PATH) if kwargs.get(KEY_PATH) else TRC_IMAGES
        images = _process_batch(**kwargs)
    else:
        kwargs[KEY_PATH] = kwargs.get(KEY_PATH) if kwargs.get(KEY_PATH) else TRC_IMAGE
        kwargs[KEY_TITLE] = kwargs.get(KEY_TITLE) if kwargs.get(KEY_TITLE) else _convert_file_name_to_title(**kwargs)
        images.append(_process_image(**kwargs))
    return images


def _process_batch(**kwargs) -> List[Image.Image]:
    """
    Processes a batch of images.

    :pre: kwargs.get(KEY_PATH) != None
    :return: None
    """
    edited_images = list()
    input_path = kwargs.get(KEY_PATH)
    for path in os.listdir(input_path):
        absolute_path = os.path.join(input_path, path)
        image_kwargs = kwargs.copy()
        image_kwargs[KEY_PATH] = absolute_path
        image_kwargs[KEY_TITLE] = kwargs.get(KEY_TITLE) if kwargs.get(KEY_TITLE) else _convert_file_name_to_title(**image_kwargs)
        edited_image = _process_image(**image_kwargs)
        edited_images.append(edited_image)
    return edited_images


def _process_image(**kwargs) -> Optional[Image.Image]:
    """
    Processes a single image.

    :pre: kwargs.get(KEY_PATH) != None and kwargs.get(KEY_TITLE) != None
    :return: the edited image or None
    """
    input_path = kwargs.get(KEY_PATH)
    img = Image.open(input_path)
    cropped_img: Image = img.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
    cropped_img.filename = img.filename  # Ensures filename data is transferred to updated copy
    color = RECTANGLE_FILL
    if logo_path := kwargs.get(KEY_LOGO_PATH):
        logo: Image.Image = Image.open(logo_path)
        color = _get_best_top_color(logo)
        _draw_logo(cropped_img, logo)
    edited_image = _draw_overlay(
        cropped_img,
        color,
        **kwargs
    )
    return edited_image


def _convert_file_name_to_title(**kwargs) -> Optional[str]:
    """
    A helper method which converts file names into titles. If the necessary arguments aren't supplied,
    this function returns None.

    :return: a title string or None
    """
    title: Optional[str] = kwargs.get(KEY_TITLE)
    path: Optional[str] = kwargs.get(KEY_PATH)
    if not title and path:
        file_path = Path(path).resolve().stem
        title = titlecase(file_path.replace(kwargs.get("separator", SEPARATOR), ' '))
    return title


def _draw_rectangle(
        draw: ImageDraw,
        position: int,
        width: int,
        tier: str,
        color: tuple = RECTANGLE_FILL
):
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
        outline=TIER_MAP.get(tier, None),
        width=7
    )


def _draw_text(draw: ImageDraw, position: tuple, text: str, font: ImageFont):
    """
    Draws text on the image.

    :param draw: the picture to edit
    :param position: the position of the text as an (x, y) tuple
    :param text: the text
    :param font: the font of the text
    :return: nothing
    """
    draw.text(
        position,
        text,
        fill=TEXT_FILL,
        font=font
    )


def _get_text_position(text_width, text_height, text_ascent, y_offset) -> tuple:
    """
    A helper function which places the text safely within the title block.

    A lot of work went into making sure this function behaved properly.

    :param text_width: the width of the text bounding box
    :param text_height: the height of the text without the ascent
    :param text_ascent: the height of the ascent
    :param y_offset: the y location of the title block
    :return: a tuple containing the x, y pixel coordinates of the text
    """
    return (
        IMAGE_WIDTH - text_width - X_OFFSET,
        y_offset - text_ascent + (RECTANGLE_HEIGHT - text_height) / 2
    )


def _get_text_metrics(text: str, font: ImageFont):
    """
    Returns some useful metrics about the font.

    :param text: the text to be displayed
    :param font: the font object
    :return: a tuple consisting of four sections of the text (top offset, text, bottom offset)
    """
    ascent, descent = font.getmetrics()
    (width, _), (_, offset_y) = font.font.getsize(text)
    return width, offset_y, ascent - offset_y, descent


def _draw_overlay(image: Image.Image, color: tuple, **kwargs) -> Image:
    """
    Draws text over an image.

    :param image: an image
    :return: the updated image
    """
    draw = ImageDraw.Draw(image)
    font = kwargs.get(KEY_FONT, DEFAULT_FONT)
    font = font if font else DEFAULT_FONT
    font = ImageFont.truetype(font, FONT_SIZE)

    if title := kwargs.get(KEY_TITLE):
        # Detect space (precondition for split)
        if len(title.split()) > 1:
            top_half_text, bottom_half_text = _split_string_by_nearest_middle_space(title)
        else:
            top_half_text, bottom_half_text = title, None

        # Draw top
        width, top_offset, height, _ = _get_text_metrics(top_half_text, font)
        top_position = _get_text_position(width, height, top_offset, TOP_RECTANGLE_Y)
        _draw_rectangle(draw, TOP_RECTANGLE_Y, width, kwargs.get(KEY_TIER, ""), color)
        _draw_text(draw, top_position, top_half_text, font)

        # Draw bottom
        if bottom_half_text:
            width, top_offset, height, _ = _get_text_metrics(bottom_half_text, font)
            bottom_position = _get_text_position(width, height, top_offset, BOTTOM_RECTANGLE_Y)
            _draw_rectangle(draw, BOTTOM_RECTANGLE_Y, width, kwargs.get(KEY_TIER, ""), color)
            _draw_text(draw, bottom_position, bottom_half_text, font)

    return image


def _draw_logo(img: Image.Image, logo: Image.Image):
    """
    Adds a logo to the image if a path is provided.

    :param img: an image to be modified
    :param logo: the logo file to be added
    :return: nothing
    """
    logo.thumbnail(LOGO_SIZE)
    _, height = img.size
    img.paste(logo, (LOGO_PADDING, height - LOGO_SIZE[1] - LOGO_PADDING), logo)


def _split_string_by_nearest_middle_space(input_string: str) -> tuple:
    """
    Splits a string by the nearest middle space. Assumes space is in string.

    :param input_string: some string
    :return: a pair of strings
    """
    index = len(input_string) // 2
    curr_char = input_string[index]
    count = 1
    while not curr_char.isspace():
        index += (-1) ** (count + 1) * count  # thanks wolfram alpha (1, -2, 3, -4, ...)
        curr_char = input_string[index]
        count += 1
    return input_string[:index], input_string[index + 1:]


def _get_best_top_color(image: Image.Image) -> tuple:
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
