import os

KEY_BATCH = "batch"
KEY_FONT = "font"
KEY_LOGO_PATH = "logo_path"
KEY_PATH = "path"
KEY_TIER = "tier"
KEY_TITLE = "title"
KEY_OUTPUT_PATH = "output_path"
KEY_SIZE = "size"

FILE_TYPES = [('image files', ('.png', '.jpg', '.jpeg'))]

SEPARATOR = "-"

DEFAULT_BATCH_MODE = False
DEFAULT_FONT = os.path.join(os.path.dirname(__file__), "assets/fonts/BERNHC.TTF")
DEFAULT_SIZE = "WordPress"

GOLD = (255, 215, 0)
SILVER = (211, 211, 211)

TIER_MAP = {
    "free": SILVER,
    "premium": GOLD
}

SIZE_MAP = {
    "DEV": (1000, 420),  # Cover image size according to: https://dev.to/p/editor_guide
    "Twitter": (1200, 628),  # Card size according to: https://louisem.com/217438/twitter-image-size
    "WordPress": (1200, 628),  # Thumbnail size according to: https://blog.snappa.com/youtube-thumbnail-size/
    "YouTube": (1280, 720)  # Featured image size according to: https://blog.snappa.com/wordpress-featured-image-size/
}

TRC_ICON = os.path.join(os.path.dirname(__file__), 'assets/icons/the-renegade-coder-sample-icon.png')
TRC_IMAGE = os.path.join(os.path.dirname(__file__), 'assets/images/welcome-to-the-image-titler-by-the-renegade-coder.jpg')
TRC_IMAGES = os.path.join(os.path.dirname(__file__), 'assets/images/')
