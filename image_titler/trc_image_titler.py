import argparse
import os
import tkinter
from tkinter.filedialog import askopenfilename
from pathlib import Path
from titlecase import titlecase

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

FONT = os.path.join(os.path.dirname(__file__), "BERNHC.TTF")
TEXT_FILL = (255, 255, 255)
RECTANGLE_FILL = (201, 2, 41)

FONT_SIZE = 114
TOP_RECTANGLE_Y = 145
BOTTOM_RECTANGLE_Y = TOP_RECTANGLE_Y + 180
TOP_TEXT_Y = TOP_RECTANGLE_Y + 5
BOTTOM_TEXT_Y = BOTTOM_RECTANGLE_Y + 5
RECTANGLE_HEIGHT = 145
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1200
X_OFFSET = 30
GOLD = (255, 215, 0)
SILVER = (211, 211, 211)

TIER_MAP = {
    "free": SILVER,
    "premium": GOLD
}


def split_string_by_nearest_middle_space(input_string: str) -> tuple:
    """
    Splits a string by the nearest middle space.

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


def draw_rectangle(draw: ImageDraw, position: int, width: int, tier: str):
    """
    Draws a rectangle over the image given a ImageDraw object and the intended
    position, width, and tier.

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
        fill=RECTANGLE_FILL,
        outline=TIER_MAP.get(tier.lower(), None),
        width=7
    )


def draw_text(draw: ImageDraw, position: int, width: int, text: str, font: ImageFont):
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


def draw_overlay(image: Image, title: str, tier: str) -> Image:
    """
    Draws text over an image.

    :param image: an image
    :param title: the image title
    :param tier: the image tier
    :return: the updated image
    """
    cropped_img = image.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(cropped_img)
    font = ImageFont.truetype(FONT, FONT_SIZE)
    top_half, bottom_half = split_string_by_nearest_middle_space(title)
    top_width, top_height = draw.textsize(top_half, font)
    bottom_width, bottom_height = draw.textsize(bottom_half, font)
    draw_rectangle(draw, TOP_RECTANGLE_Y, top_width, tier)
    draw_rectangle(draw, BOTTOM_RECTANGLE_Y, bottom_width, tier)
    draw_text(draw, TOP_TEXT_Y, top_width, top_half, font)
    draw_text(draw, BOTTOM_TEXT_Y, bottom_width, bottom_half, font)
    cropped_img.show()
    return cropped_img


def save_copy(og_image: Image, edited_image: Image, title: str, output_path: str = None):
    """
    A helper function for saving a copy of the image.

    :param og_image: the original image
    :param edited_image: the edited image
    :param title: the title of the image
    :param output_path: the path to dump the picture
    :return: nothing
    """
    file_name = title.lower().replace(" ", "-")
    format_path = "{0}{1}{2}-featured-image.{3}"
    if output_path is None:
        storage_path = format_path.format("", "", file_name, og_image.format)
    else:
        storage_path = format_path.format(output_path, os.sep, file_name, og_image.format)
    edited_image.save(storage_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title')
    parser.add_argument('-p', '--path')
    parser.add_argument('-o', '--output_path')
    parser.add_argument('-r', '--tier', default="")
    args = parser.parse_args()
    path = args.path  # type: str
    title = args.title  # type: str
    tier = args.tier  # type: str
    output_path = args.output_path  # type: str
    if path is None:
        tkinter.Tk().withdraw()
        path = askopenfilename()
    if title is None:
        file_name = Path(path).resolve().stem
        title = titlecase(file_name.replace('-', ' '))
    img = Image.open(path)
    edited_image = draw_overlay(img, title, tier)
    save_copy(img, edited_image, title, output_path)


if __name__ == '__main__':
    main()
