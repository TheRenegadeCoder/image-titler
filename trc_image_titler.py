from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

SOURCE = 'E:\\Documents\\Work\\The Renegade Coder\\Assets\\Featured Images\\Sources\\hello-world-in-swift.jpg'
TITLE = "Hello World in Swift"


def split_string_by_nearest_middle_space(input_string):
    index = len(input_string) // 2
    curr_char = input_string[index]
    n = 1
    while not curr_char.isspace():
        index += (-1)**(n + 1) * n  # thanks wolfram alpha (1, -2, 3, -4, ...)
        curr_char = input_string[index]
        n += 1
    return input_string[:index], input_string[index + 1:]

img = Image.open(SOURCE)
cropped_img = img.crop((0, 0, 1920, 1200))
draw = ImageDraw.Draw(cropped_img)
font = ImageFont.truetype("BERNHC.TTF", 114)
width, height = draw.textsize(TITLE, font)
print("Width: {0}, Height: {1}".format(width, height))
draw.text((1500, 200), TITLE, fill=(255, 255, 255), font=font)
cropped_img.show()

print(split_string_by_nearest_middle_space(TITLE))