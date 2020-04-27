import argparse
import os
import tkinter
from pathlib import Path
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

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

TIER_MAP = {
    "free": SILVER,
    "premium": GOLD
}


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


def draw_rectangle(draw: ImageDraw, position: int, width: int, tier: str, color: tuple):
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
        fill=color,
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


def draw_overlay(image: Image.Image, title: str, tier: str, color: tuple) -> Image:
    """
    Draws text over an image.

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
    draw_rectangle(draw, TOP_RECTANGLE_Y, top_width, tier, color)
    draw_text(draw, TOP_TEXT_Y, top_width, top_half, font)

    # Draw bottom
    if bottom_half:
        bottom_width, bottom_height = draw.textsize(bottom_half, font)
        draw_rectangle(draw, BOTTOM_RECTANGLE_Y, bottom_width, tier, color)
        draw_text(draw, BOTTOM_TEXT_Y, bottom_width, bottom_half, font)

    return image


def draw_logo(img: Image.Image, logo: Image.Image):
    """
    Adds a logo to the image if a path is provided.

    :param img: an image to be modified
    :param logo: the logo file to be added
    :return: nothing
    """
    logo.thumbnail(LOGO_SIZE)
    width, height = img.size
    img.paste(logo, (LOGO_PADDING, height - LOGO_SIZE[1] - LOGO_PADDING), logo)


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
    tag = "featured-image"
    version: str = pkg_resources.require("image-titler")[0].version
    version = version.replace(".", "-")
    if output_path is None:
        storage_path = f'{file_name}-{tag}-v{version}.{og_image.format}'
    else:
        storage_path = f'{output_path}{os.sep}{file_name}-{tag}-v{version}.{og_image.format}'
    edited_image.save(storage_path, subsampling=0, quality=100)  # Improved quality


def parse_input() -> argparse.Namespace:
    """
    Creates and executes a parser on the command line inputs.

    :return: the processed command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', help="Adds a custom title to the image")
    parser.add_argument('-p', '--path', help="Selects an image file")
    parser.add_argument('-o', '--output_path', help="Selects an output path for the processed image")
    parser.add_argument('-r', '--tier', default="", help="Selects a image tier (free or premium)")
    parser.add_argument('-l', '--logo_path', help="Selects a logo file for addition to the processed image")
    parser.add_argument('-b', '--batch', default=False, action='store_true', help="Turns on batch processing")
    args = parser.parse_args()
    return args


def request_input_path(path: str, batch: bool) -> str:
    """
    A helper function which asks the user for an input path
    if one is not supplied on the command line. In this implementation,
    the type of request we make (e.g. file vs. folder) depends on the state of batch.

    :param path: a folder or file path
    :param batch: tells us if we are in batch mode or not
    :return: the input path after the request
    """
    input_path = path
    if not path:
        tkinter.Tk().withdraw()
        if not batch:
            input_path = askopenfilename()
        else:
            input_path = askdirectory()
    return input_path


def process_batch(input_path: str, tier: str = None, logo_path: str = None, output_path: str = None):
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
        process_image(absolute_path, tier, logo_path, output_path)


def process_image(input_path: str, tier: str = None, logo_path: str = None, output_path: str = None,
                  title: str = None) -> Image.Image:
    """
    Processes a single image.

    :param input_path: the path of an image
    :param tier: the image tier (free or premium)
    :param logo_path: the path to a logo
    :param output_path: the output path of the processed image
    :param title: the title of the processed image
    :return: the edited image
    """
    if not title:
        file_name = Path(input_path).resolve().stem
        title = titlecase(file_name.replace('-', ' '))
    img = Image.open(input_path)
    cropped_img: Image = img.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
    color = RECTANGLE_FILL
    if logo_path:
        logo: Image.Image = Image.open(logo_path)
        color = get_best_top_color(logo)
        draw_logo(cropped_img, logo)
    edited_image = draw_overlay(cropped_img, title, tier, color)
    save_copy(img, edited_image, title, output_path)
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


def main():
    args = parse_input()
    path: str = args.path
    batch: bool = args.batch
    tier: str = args.tier
    logo_path: str = args.logo_path
    output_path: str = args.output_path
    title: str = args.title
    input_path = request_input_path(path, batch)
    if input_path:
        if args.batch:
            process_batch(input_path, tier, logo_path, output_path)
        else:
            process_image(input_path, tier, logo_path, output_path, title).show()


if __name__ == '__main__':
    main()
