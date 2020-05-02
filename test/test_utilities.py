import shutil
import sys
from pathlib import Path
from unittest import TestCase

import pkg_resources
from PIL import Image, ImageChops

from image_titler import utilities
from image_titler.utilities import save_copy, FONT

TRC_ICON_PATH = "icons/the-renegade-coder-sample-icon.png"
TRC_RED = (201, 2, 41, 255)

VF_ICON_PATH = "icons/virtual-flat-sample-icon.png"
VF_BLUE = (0, 164, 246, 255)

ASSETS = "assets/"
DEFAULT_IMAGE = "assets/23-tech-topics-to-tackle.jpg"
LOGO_RED_IMAGE = "assets/3-ways-to-check-if-a-list-is-empty-in-python.jpg"
LOGO_BLUE_IMAGE = "assets/hello-world-in-matlab.jpg"
FREE_IMAGE = "assets/columbus-drivers-are-among-the-worst.jpg"
PREMIUM_IMAGE = "assets/the-guide-to-causing-mass-panic.jpg"
SPECIAL_IMAGE = "assets/happy-new-year.jpg"
CUSTOM_FONT_IMAGE = "assets/reflecting-on-my-third-semester-of-teaching.jpg"
ONE_LINE_TITLE_IMAGE = "assets/minimalism.jpg"

TEST_DUMP = "test/dump"
TEST_SOLO_DUMP = TEST_DUMP + "/solo"
TEST_BATCH_DUMP = TEST_DUMP + "/batch"
SAMPLE_DUMP = "samples/v" + pkg_resources.require("image-titler")[0].version


class TestUtilities(TestCase):
    pass


class TestSaveCopy(TestUtilities):

    @classmethod
    def setUpClass(cls) -> None:
        try:
            shutil.rmtree(TEST_SOLO_DUMP)
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(SAMPLE_DUMP)
        except FileNotFoundError:
            pass

        Path(TEST_SOLO_DUMP).mkdir(parents=True, exist_ok=True)
        Path(SAMPLE_DUMP).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def generate_image(input_path, title, logo_path=None, tier="", font=FONT):
        test_image = utilities.process_image(
            input_path=input_path,
            title=title,
            logo_path=logo_path,
            tier=tier,
            font=font
        )
        test_file = save_copy(input_path, test_image, output_path=TEST_SOLO_DUMP, title=title)

        title = utilities.convert_file_name_to_title(input_path)
        sample_image = utilities.process_image(
            input_path=input_path,
            title=title,
            logo_path=logo_path,
            tier=tier,
            font=font
        )
        save_copy(input_path, sample_image, output_path=SAMPLE_DUMP)
        return test_file

    def test_default(self):
        test_file = self.generate_image(DEFAULT_IMAGE, title="Test Default")
        self.assertTrue(Path(test_file).exists())

    def test_logo_red(self):
        test_file = self.generate_image(LOGO_RED_IMAGE, title="Test Red Logo", logo_path=TRC_ICON_PATH)
        self.assertTrue(Path(test_file).exists())

    def test_logo_blue(self):
        self.generate_image(LOGO_BLUE_IMAGE, title="Test Blue Logo", logo_path=VF_ICON_PATH)

    def test_free_tier(self):
        self.generate_image(FREE_IMAGE, title="Test Free Tier", tier="free")

    def test_premium_tier(self):
        self.generate_image(PREMIUM_IMAGE, title="Test Premium Tier", tier="premium")

    def test_custom_font(self):
        self.generate_image(CUSTOM_FONT_IMAGE, title="Test Custom Font", font="test/fonts/arial.ttf")

    def test_custom_font_strange_height(self):
        self.generate_image(
            CUSTOM_FONT_IMAGE,
            title="Test Custom Font Strange Height",
            font="test/fonts/gadugi.ttf"
        )

    def test_special_chars_in_title(self):
        test_image = utilities.process_image(SPECIAL_IMAGE, title="Test Special Chars?")
        save_copy(SPECIAL_IMAGE, test_image, output_path=TEST_SOLO_DUMP, title="Test Special Chars?")

    def test_one_line_title(self):
        self.generate_image(ONE_LINE_TITLE_IMAGE, title="TestSingleLineFile")


class TestProcessImage(TestUtilities):

    def setUp(self) -> None:
        self.size = (1920, 960)
        self.input_image = Image.open(DEFAULT_IMAGE)
        self.default_image = utilities.process_image(DEFAULT_IMAGE, title="Test Default Image")
        self.different_title_image = utilities.process_image(DEFAULT_IMAGE, title="Test Different Logo Image")

    def test_default(self):
        self.assertEqual(self.size, self.default_image.size)
        self.assertIsNone(ImageChops.difference(self.default_image, self.default_image).getbbox())
        self.assertIsNotNone(ImageChops.difference(self.input_image, self.default_image).getbbox())

    def test_compare_all(self):
        images = [
            self.default_image,
            self.different_title_image
        ]
        for i1 in images:
            for i2 in images:
                if i1 is not i2:
                    self.assertIsNotNone(ImageChops.difference(i1, i2).getbbox())


class TestProcessBatch(TestUtilities):

    @classmethod
    def setUpClass(cls) -> None:
        try:
            shutil.rmtree(TEST_BATCH_DUMP)
        except FileNotFoundError:
            pass

        Path(TEST_BATCH_DUMP + "/default").mkdir(parents=True, exist_ok=True)
        Path(TEST_BATCH_DUMP + "/free-tier").mkdir(parents=True, exist_ok=True)
        Path(TEST_BATCH_DUMP + "/premium-tier").mkdir(parents=True, exist_ok=True)

    def test_batch_default(self):
        utilities.process_batch(ASSETS, output_path=TEST_BATCH_DUMP + "/default")

    def test_batch_free_tier(self):
        utilities.process_batch(ASSETS, tier="free", output_path=TEST_BATCH_DUMP + "/free-tier")

    def test_batch_premium_tier(self):
        utilities.process_batch(ASSETS, tier="premium", output_path=TEST_BATCH_DUMP + "/premium-tier")


class TestConvertFileNameToTitle(TestUtilities):

    def test_default(self):
        title = utilities.convert_file_name_to_title("how-to-loop-in-python.png")
        self.assertEqual(title, "How to Loop in Python")

    def test_custom_sep(self):
        title = utilities.convert_file_name_to_title("how.to.loop.in.python.png", ".")
        self.assertEqual("How to Loop in Python", title)


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


class TestParseInput(TestUtilities):

    def setUp(self) -> None:
        sys.argv = sys.argv[:1]  # clears args for each test

    def test_default(self):
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_title(self):
        sys.argv.append("-t")
        sys.argv.append("Hello World")
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, "Hello World")

    def test_path(self):
        sys.argv.append("-p")
        sys.argv.append("path/to/stuff")
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, "path/to/stuff")
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_output_path(self):
        sys.argv.append("-o")
        sys.argv.append("path/to/stuff")
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, "path/to/stuff")
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_logo_path(self):
        sys.argv.append("-l")
        sys.argv.append("path/to/stuff")
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, "path/to/stuff")
        self.assertEqual(args.title, None)

    def test_batch(self):
        sys.argv.append("-b")
        args = utilities.parse_input()
        self.assertEqual(args.batch, True)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_premium(self):
        sys.argv.append("-r")
        sys.argv.append("premium")
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "premium")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_free(self):
        sys.argv.append("-r")
        sys.argv.append("free")
        args = utilities.parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "free")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)
