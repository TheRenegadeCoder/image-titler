from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

SOURCE = 'E:\\Documents\\Work\\The Renegade Coder\\Assets\\Featured Images\\Sources\\hello-world-in-swift.jpg'
TITLE = "A Wild World Ahead Boy"
FONT = "BERNHC.TTF"

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
        index += (-1)**(n + 1) * n  # thanks wolfram alpha (1, -2, 3, -4, ...)
        curr_char = input_string[index]
        n += 1
    return input_string[:index], input_string[index + 1:]


def draw_text(image, title):
    cropped_img = image.crop((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(cropped_img)
    font = ImageFont.truetype(FONT, FONT_SIZE)
    top_half, bottom_half = split_string_by_nearest_middle_space(title)
    top_width, top_height = draw.textsize(top_half, font)
    bottom_width, bottom_height = draw.textsize(bottom_half, font)
    print(top_height, bottom_height)
    draw.rectangle(((IMAGE_WIDTH - top_width - X_OFFSET * 2, TOP_RECTANGLE_Y), (IMAGE_WIDTH, TOP_RECTANGLE_Y + RECTANGLE_HEIGHT)), fill="red")
    draw.rectangle(((IMAGE_WIDTH - bottom_width - X_OFFSET * 2, BOTTOM_RECTANGLE_Y), (IMAGE_WIDTH, BOTTOM_RECTANGLE_Y + RECTANGLE_HEIGHT)), fill="red")
    draw.text((IMAGE_WIDTH - top_width - X_OFFSET, TOP_TEXT_Y), top_half, fill=(255, 255, 255), font=font)
    draw.text((IMAGE_WIDTH - bottom_width - X_OFFSET, BOTTOM_TEXT_Y), bottom_half, fill=(255, 255, 255), font=font)
    cropped_img.show()


def main():
    img = Image.open(SOURCE)
    draw_text(img, TITLE)


if __name__ == '__main__':
    main()

