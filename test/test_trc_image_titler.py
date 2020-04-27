import sys
from unittest import TestCase

from PIL import Image

from image_titler import trc_image_titler

TRC_ICON_PATH = "../icons/the-renegade-coder-sample-icon.png"
TRC_RED = (201, 2, 41, 255)

VF_ICON_PATH = "../icons/virtual-flat-sample-icon.png"
VF_BLUE = (0, 164, 246, 255)


class TestImageTitler(TestCase):
    pass


class TestConvertFileNameToTitle(TestImageTitler):

    def test_default(self):
        title = trc_image_titler.convert_file_name_to_title("how-to-loop-in-python")
        self.assertEqual(title, "How to Loop in Python")


class TestGetBestTopColor(TestImageTitler):

    def test_renegade_coder_icon(self):
        img: Image.Image = Image.open(TRC_ICON_PATH)
        color = trc_image_titler.get_best_top_color(img)
        self.assertEqual(color, TRC_RED)
        img.close()

    def test_virtual_flat_icon(self):
        img: Image.Image = Image.open(VF_ICON_PATH)
        color = trc_image_titler.get_best_top_color(img)
        self.assertEqual(color, VF_BLUE)
        img.close()


class TestSplitString(TestImageTitler):

    def test_first_space(self):
        top, bottom = trc_image_titler.split_string_by_nearest_middle_space("Split first one")
        self.assertEqual(top, "Split")
        self.assertEqual(bottom, "first one")

    def test_middle_space(self):
        top, bottom = trc_image_titler.split_string_by_nearest_middle_space("Hello World")
        self.assertEqual(top, "Hello")
        self.assertEqual(bottom, "World")

    def test_last_space(self):
        top, bottom = trc_image_titler.split_string_by_nearest_middle_space("Split last opening")
        self.assertEqual(top, "Split last")
        self.assertEqual(bottom, "opening")


class TestParseInput(TestImageTitler):

    def setUp(self) -> None:
        sys.argv = sys.argv[:1]  # clears args for each test

    def test_default(self):
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_title(self):
        sys.argv.append("-t")
        sys.argv.append("Hello World")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, "Hello World")

    def test_path(self):
        sys.argv.append("-p")
        sys.argv.append("path/to/stuff")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, "path/to/stuff")
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_output_path(self):
        sys.argv.append("-o")
        sys.argv.append("path/to/stuff")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, "path/to/stuff")
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_logo_path(self):
        sys.argv.append("-l")
        sys.argv.append("path/to/stuff")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, "path/to/stuff")
        self.assertEqual(args.title, None)

    def test_batch(self):
        sys.argv.append("-b")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, True)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_premium(self):
        sys.argv.append("-r")
        sys.argv.append("premium")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "premium")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_free(self):
        sys.argv.append("-r")
        sys.argv.append("free")
        args = trc_image_titler.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "free")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)
