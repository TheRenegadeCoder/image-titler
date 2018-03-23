from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

SOURCE = 'E:\\Documents\\Work\\The Renegade Coder\\Assets\\Featured Images\\Sources\\hello-world-in-swift.jpg'
TITLE = "A Wild World Ahead"


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
    cropped_img = image.crop((0, 0, 1920, 1200))
    draw = ImageDraw.Draw(cropped_img)
    font = ImageFont.truetype("BERNHC.TTF", 114)
    top_half, bottom_half = split_string_by_nearest_middle_space(title)
    top_width, top_height = draw.textsize(top_half, font)
    bottom_width, bottom_height = draw.textsize(bottom_half, font)
    draw.rectangle(((1920 - top_width - 60, 150), (1920, 150 + top_height + 20)), fill="red")
    draw.rectangle(((1920 - bottom_width - 60, 325), (1920, 325 + bottom_height + 20)), fill="red")
    draw.text((1920 - top_width - 30, 150), top_half, fill=(255, 255, 255), font=font)
    draw.text((1920 - bottom_width - 30, 325), bottom_half, fill=(255, 255, 255), font=font)
    cropped_img.show()


def main():
    img = Image.open(SOURCE)
    draw_text(img, TITLE)


if __name__ == '__main__':
    main()

