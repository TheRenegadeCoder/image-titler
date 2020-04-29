import os
import shutil
from unittest import TestCase

import pkg_resources
from PIL import Image

from image_titler import utilities

TRC_ICON_PATH = "icons/the-renegade-coder-sample-icon.png"
TRC_RED = (201, 2, 41, 255)

VF_ICON_PATH = "icons/virtual-flat-sample-icon.png"
VF_BLUE = (0, 164, 246, 255)

DEFAULT_IMAGE = "assets/23-tech-topics-to-tackle.jpg"
LOGO_RED_IMAGE = "assets/3-ways-to-check-if-a-list-is-empty-in-python.jpg"
LOGO_BLUE_IMAGE = "assets/hello-world-in-matlab.jpg"
FREE_IMAGE = "assets/columbus-drivers-are-among-the-worst.jpg"
PREMIUM_IMAGE = "assets/the-guide-to-causing-mass-panic.jpg"
SPECIAL_IMAGE = "assets/happy-new-year.jpg"

TEST_DUMP = "test/dump"
SAMPLE_DUMP = "samples/v" + pkg_resources.require("image-titler")[0].version


class TestUtilities(TestCase):
    pass


class TestProcessImage(TestUtilities):

    @classmethod
    def setUpClass(cls) -> None:
        try:
            shutil.rmtree(TEST_DUMP)
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(SAMPLE_DUMP)
        except FileNotFoundError:
            pass
        
        os.mkdir(TEST_DUMP)
        os.mkdir(SAMPLE_DUMP)

    @staticmethod
    def generate_image(input_path, title=None, logo_path=None, tier=""):
        utilities.process_image(
            input_path=input_path,
            output_path=TEST_DUMP,
            title=title,
            logo_path=logo_path,
            tier=tier
        )
        utilities.process_image(
            input_path=input_path,
            output_path=SAMPLE_DUMP,
            logo_path=logo_path,
            tier=tier
        )

    def test_default(self):
        TestProcessImage.generate_image(DEFAULT_IMAGE)

    def test_title(self):
        TestProcessImage.generate_image(DEFAULT_IMAGE, title="Test Title")

    def test_logo_red(self):
        TestProcessImage.generate_image(LOGO_RED_IMAGE, title="Test Red Logo", logo_path=TRC_ICON_PATH)

    def test_logo_blue(self):
        TestProcessImage.generate_image(LOGO_BLUE_IMAGE, title="Test Blue Logo", logo_path=VF_ICON_PATH)

    def test_free_tier(self):
        TestProcessImage.generate_image(FREE_IMAGE, title="Test Free Tier", tier="free")

    def test_premium_tier(self):
        TestProcessImage.generate_image(PREMIUM_IMAGE, title="Test Premium Tier", tier="premium")

    def test_special_chars_in_title(self):
        utilities.process_image(SPECIAL_IMAGE, output_path=TEST_DUMP, title="Test Special Chars?")


class TestConvertFileNameToTitle(TestUtilities):

    def test_default(self):
        title = utilities.convert_file_name_to_title("how-to-loop-in-python")
        self.assertEqual(title, "How to Loop in Python")

    def test_custom_sep(self):
        title = utilities.convert_file_name_to_title("how.to.loop.in.python", ".")
        self.assertEqual(title, "How to Loop in Python")


class TestGetBestTopColor(TestUtilities):

    def test_renegade_coder_icon(self):
        img: Image.Image = Image.open(TRC_ICON_PATH)
        color = utilities.get_best_top_color(img)
        self.assertEqual(color, TRC_RED)
        img.close()

    def test_virtual_flat_icon(self):
        img: Image.Image = Image.open(VF_ICON_PATH)
        color = utilities.get_best_top_color(img)
        self.assertEqual(color, VF_BLUE)
        img.close()


class TestSplitString(TestUtilities):

    def test_first_space(self):
        top, bottom = utilities.split_string_by_nearest_middle_space("Split first one")
        self.assertEqual(top, "Split")
        self.assertEqual(bottom, "first one")

    def test_middle_space(self):
        top, bottom = utilities.split_string_by_nearest_middle_space("Hello World")
        self.assertEqual(top, "Hello")
        self.assertEqual(bottom, "World")

    def test_last_space(self):
        top, bottom = utilities.split_string_by_nearest_middle_space("Split last opening")
        self.assertEqual(top, "Split last")
        self.assertEqual(bottom, "opening")
