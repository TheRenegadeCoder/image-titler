from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

img = Image.open('E:\\Documents\\Work\\The Renegade Coder\\Assets\\Featured Images\\Sources\\hello-world-in-swift.jpg')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("BERNHC.TTF", 160)
draw.text((0, 0), "Sample Text", fill=(255, 255, 255), font=font)
img.show()
