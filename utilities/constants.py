import os

KEY_BATCH = "batch"
KEY_FONT = "font"
KEY_LOGO_PATH = "logo_path"
KEY_PATH = "path"
KEY_TIER = "tier"
KEY_TITLE = "title"
KEY_OUTPUT_PATH = "output_path"

FILE_TYPES = [('image files', ('.png', '.jpg', '.jpeg'))]

SEPARATOR = "-"

DEFAULT_BATCH_MODE = False
DEFAULT_FONT = os.path.join(os.path.dirname(__file__), "BERNHC.TTF")

GOLD = (255, 215, 0)
SILVER = (211, 211, 211)

TIER_MAP = {
    "free": SILVER,
    "premium": GOLD
}
