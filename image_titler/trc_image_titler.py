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


def split_string_by_nearest_middle_space(input_string):
    """
    Splits a string by the nearest middle space.

    :param input_string: some string
    :type input_string: str
    :return: a pair of strings
    :rtype: tuple
    """
    index = len(input_string) // 2
    curr_char = input_string[index]
    n = 1
    while not curr_char.isspace():
        index += (-1) ** (n + 1) * n  # thanks wolfram alpha (1, -2, 3, -4, ...)
        curr_char = input_string[index]
        n += 1
    return input_string[:index], input_string[index + 1:]


def draw_text(image, title):
    """
    Draws text over an image.

    :param image: an image
    :type image: Image
    :param title: the image title
    :type title: str
    :return: the updated image
    :rtype: Image
    """
    cropped_img = image.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(cropped_img)
    font = ImageFont.truetype(FONT, FONT_SIZE)
    top_half, bottom_half = split_string_by_nearest_middle_space(title)
    top_width, top_height = draw.textsize(top_half, font)
    bottom_width, bottom_height = draw.textsize(bottom_half, font)
    draw.rectangle(
        (
            (IMAGE_WIDTH - top_width - X_OFFSET * 2, TOP_RECTANGLE_Y),
            (IMAGE_WIDTH, TOP_RECTANGLE_Y + RECTANGLE_HEIGHT)
        ),
        fill=RECTANGLE_FILL
    )
    draw.rectangle(
        (
            (IMAGE_WIDTH - bottom_width - X_OFFSET * 2, BOTTOM_RECTANGLE_Y),
            (IMAGE_WIDTH, BOTTOM_RECTANGLE_Y + RECTANGLE_HEIGHT)
        ),
        fill=RECTANGLE_FILL
    )
    draw.text(
        (IMAGE_WIDTH - top_width - X_OFFSET, TOP_TEXT_Y),
        top_half,
        fill=TEXT_FILL,
        font=font
    )
    draw.text(
        (IMAGE_WIDTH - bottom_width - X_OFFSET, BOTTOM_TEXT_Y),
        bottom_half,
        fill=TEXT_FILL,
        font=font
    )
    cropped_img.show()
    return cropped_img


def save_copy(og_image, edited_image, title, output_path=None):
    """
    A helper function for saving a copy of the image.

    :param og_image: the original image
    :type og_image: Image
    :param edited_image: the edited image
    :type edited_image: Image
    :param title: the title of the image
    :type title: str
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
    args = parser.parse_args()
    path = args.path  # type: str
    title = args.title  # type: str
    output_path = args.output_path
    if path is None:
        tkinter.Tk().withdraw()
        path = askopenfilename()
    if title is None:
        file_name = Path(path).resolve().stem
        title = titlecase(file_name.replace('-', ' '))
    img = Image.open(path)
    edited_image = draw_text(img, title)
    save_copy(img, edited_image, title, output_path)


if __name__ == '__main__':
    main()
