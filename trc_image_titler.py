from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

SOURCE = 'E:\\Documents\\Work\\The Renegade Coder\\Assets\\Featured Images\\Sources\\hello-world-in-swift.jpg'
TITLE = "Hello World in Swift"

img = Image.open(SOURCE)
cropped_img = img.crop((0, 0, 1920, 1200))
draw = ImageDraw.Draw(cropped_img)
font = ImageFont.truetype("BERNHC.TTF", 114)
width, height = draw.textsize(TITLE, font)
print("Width: {0}, Height: {1}".format(width, height))
draw.text((1500, 200), TITLE, fill=(255, 255, 255), font=font)
cropped_img.show()
