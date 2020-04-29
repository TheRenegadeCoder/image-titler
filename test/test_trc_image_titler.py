import os
import shutil
import sys
from unittest import TestCase

import pkg_resources
from PIL import Image

from image_titler import cmd

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


class TestImageTitler(TestCase):
    pass


class TestProcessImage(TestImageTitler):

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
        cmd.process_image(
            input_path=input_path,
            output_path=TEST_DUMP,
            title=title,
            logo_path=logo_path,
            tier=tier
        )
        cmd.process_image(
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
        cmd.process_image(SPECIAL_IMAGE, output_path=TEST_DUMP, title="Test Special Chars?")


class TestConvertFileNameToTitle(TestImageTitler):

    def test_default(self):
        title = cmd.convert_file_name_to_title("how-to-loop-in-python")
        self.assertEqual(title, "How to Loop in Python")

    def test_custom_sep(self):
        title = cmd.convert_file_name_to_title("how.to.loop.in.python", ".")
        self.assertEqual(title, "How to Loop in Python")


class TestGetBestTopColor(TestImageTitler):

    def test_renegade_coder_icon(self):
        img: Image.Image = Image.open(TRC_ICON_PATH)
        color = cmd.get_best_top_color(img)
        self.assertEqual(color, TRC_RED)
        img.close()

    def test_virtual_flat_icon(self):
        img: Image.Image = Image.open(VF_ICON_PATH)
        color = cmd.get_best_top_color(img)
        self.assertEqual(color, VF_BLUE)
        img.close()


class TestSplitString(TestImageTitler):

    def test_first_space(self):
        top, bottom = cmd.split_string_by_nearest_middle_space("Split first one")
        self.assertEqual(top, "Split")
        self.assertEqual(bottom, "first one")

    def test_middle_space(self):
        top, bottom = cmd.split_string_by_nearest_middle_space("Hello World")
        self.assertEqual(top, "Hello")
        self.assertEqual(bottom, "World")

    def test_last_space(self):
        top, bottom = cmd.split_string_by_nearest_middle_space("Split last opening")
        self.assertEqual(top, "Split last")
        self.assertEqual(bottom, "opening")


class TestParseInput(TestImageTitler):

    def setUp(self) -> None:
        sys.argv = sys.argv[:1]  # clears args for each test

    def test_default(self):
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_title(self):
        sys.argv.append("-t")
        sys.argv.append("Hello World")
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, "Hello World")

    def test_path(self):
        sys.argv.append("-p")
        sys.argv.append("path/to/stuff")
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, "path/to/stuff")
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_output_path(self):
        sys.argv.append("-o")
        sys.argv.append("path/to/stuff")
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, "path/to/stuff")
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_logo_path(self):
        sys.argv.append("-l")
        sys.argv.append("path/to/stuff")
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, "path/to/stuff")
        self.assertEqual(args.title, None)

    def test_batch(self):
        sys.argv.append("-b")
        args = cmd.parse_input()
        self.assertEqual(args.batch, True)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_premium(self):
        sys.argv.append("-r")
        sys.argv.append("premium")
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "premium")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_free(self):
        sys.argv.append("-r")
        sys.argv.append("free")
        args = cmd.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "free")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)
