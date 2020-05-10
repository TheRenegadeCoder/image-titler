import shutil
import sys
from pathlib import Path
from unittest import TestCase

import pkg_resources
from PIL import Image, ImageChops

from titler.constants import KEY_TITLE, KEY_OUTPUT_PATH
from titler.draw import _convert_file_name_to_title, _process_batch, _process_image, \
    _get_best_top_color, _split_string_by_nearest_middle_space, process_images
from titler.parse import parse_input
from titler.store import save_copies

TRC_ICON_PATH = "assets/icons/the-renegade-coder-sample-icon.png"
TRC_RED = (201, 2, 41, 255)

VF_ICON_PATH = "assets/icons/virtual-flat-sample-icon.png"
VF_BLUE = (0, 164, 246, 255)

ASSETS = "assets/images"
DEFAULT_IMAGE = "assets/images/23-tech-topics-to-tackle.jpg"
LOGO_RED_IMAGE = "assets/images/3-ways-to-check-if-a-list-is-empty-in-python.jpg"
LOGO_BLUE_IMAGE = "assets/images/hello-world-in-matlab.jpg"
FREE_IMAGE = "assets/images/columbus-drivers-are-among-the-worst.jpg"
PREMIUM_IMAGE = "assets/images/the-guide-to-causing-mass-panic.jpg"
SPECIAL_IMAGE = "assets/images/happy-new-year.jpg"
CUSTOM_FONT_IMAGE = "assets/images/reflecting-on-my-third-semester-of-teaching.jpg"
ONE_LINE_TITLE_IMAGE = "assets/images/minimalism.jpg"

TEST_IMAGES = [
    Image.open(path) for path in
    [
        DEFAULT_IMAGE,
        LOGO_RED_IMAGE,
        LOGO_BLUE_IMAGE,
        FREE_IMAGE,
        PREMIUM_IMAGE,
        SPECIAL_IMAGE,
        CUSTOM_FONT_IMAGE,
        ONE_LINE_TITLE_IMAGE
    ]
]

TEST_DUMP = "tests/dump"
TEST_SOLO_DUMP = TEST_DUMP + "/solo"
TEST_BATCH_DUMP = TEST_DUMP + "/batch"
SAMPLE_DUMP = "samples/v" + pkg_resources.require("image-titler")[0].version


class TestUtilities(TestCase):
    pass


class TestParseInput(TestUtilities):

    def setUp(self) -> None:
        sys.argv = sys.argv[:1]  # clears args for each tests

    def test_default(self):
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, None)
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_title(self):
        sys.argv.append("-t")
        sys.argv.append("Hello World")
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, None)
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, "Hello World")

    def test_path(self):
        sys.argv.append("-p")
        sys.argv.append("path/to/stuff")
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, "path/to/stuff")
        self.assertEqual(args.tier, None)
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_output_path(self):
        sys.argv.append("-o")
        sys.argv.append("path/to/stuff")
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, None)
        self.assertEqual(args.output_path, "path/to/stuff")
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_logo_path(self):
        sys.argv.append("-l")
        sys.argv.append("path/to/stuff")
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, None)
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, "path/to/stuff")
        self.assertEqual(args.title, None)

    def test_batch(self):
        sys.argv.append("-b")
        args = parse_input()
        self.assertEqual(args.batch, True)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, None)
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_premium(self):
        sys.argv.append("-r")
        sys.argv.append("premium")
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "premium")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)

    def test_tier_free(self):
        sys.argv.append("-r")
        sys.argv.append("free")
        args = parse_input()
        self.assertEqual(args.batch, False)
        self.assertEqual(args.path, None)
        self.assertEqual(args.tier, "free")
        self.assertEqual(args.output_path, None)
        self.assertEqual(args.logo_path, None)
        self.assertEqual(args.title, None)


class TestSaveCopies(TestUtilities):
    """
    A test class for the store.py file which consists of a single
    exposed function: save_copies().
    """

    def setUp(self) -> None:
        """
        Resets the list of paths.

        :return: None
        """
        self.paths = list()

    def verify_existence_and_delete(self) -> None:
        """
        Verifies that a file exists and deletes it.

        :return: None
        """
        for path in self.paths:
            p = Path(path)
            self.assertTrue(p.exists(), f"{p} does not exist")
            p.unlink()

    def test_zero_images(self):
        """
        Tests the scenario when no images are passed to this function.
        It should return an empty list (since there were no files
        to process).

        :return: None
        """
        self.paths.extend(save_copies(list()))
        self.assertEqual(list(), self.paths)

    def test_one_image(self):
        """
        Tests the scenario when a single image is passed to this function.
        It should save that image and return a list which contains a single
        path to that image.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES[:1]))
        self.verify_existence_and_delete()

    def test_many_images(self):
        """
        Tests the scenario when multiple images are passed to this function.
        It should save each image to a unique path and return those paths
        in a list.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES))
        self.verify_existence_and_delete()

    def test_many_title(self):
        """
        Tests the scenario when multiple images are passed to this function with
        the title option provided. It should save each image to a unique path
        regardless of the fact they they'll all have the same core filename.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES, title="Test Many With Title Option"))
        self.verify_existence_and_delete()


class TestProcessImages(TestUtilities):

    def setUp(self) -> None:
        self.images = list()

    def test_zero_images(self):
        self.images.extend(process_images())
        self.assertEqual(1, len(self.images))

    def test_one_image(self):
        self.images.extend(process_images(path=DEFAULT_IMAGE))
        self.assertEqual(1, len(self.images))


# Everything below this line needs to be removed


class TestIntegration(TestUtilities):

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
    def generate_image(**kwargs):
        kwargs[KEY_OUTPUT_PATH] = TEST_SOLO_DUMP
        test_image = _process_image(**kwargs)
        test_file = save_copies([test_image], **kwargs)

        kwargs[KEY_OUTPUT_PATH] = SAMPLE_DUMP
        kwargs[KEY_TITLE] = None
        kwargs[KEY_TITLE] = _convert_file_name_to_title(**kwargs)
        sample_image = _process_image(**kwargs)
        save_copies([sample_image], **kwargs)

        return test_file[0]

    def test_custom_title(self):
        test_file = self.generate_image(path=DEFAULT_IMAGE, title="Test Default")
        self.assertTrue(Path(test_file).exists())

    def test_logo_red(self):
        test_file = self.generate_image(path=LOGO_RED_IMAGE, title="Test Red Logo", logo_path=TRC_ICON_PATH)
        self.assertTrue(Path(test_file).exists())

    def test_logo_blue(self):
        self.generate_image(path=LOGO_BLUE_IMAGE, title="Test Blue Logo", logo_path=VF_ICON_PATH)

    def test_free_tier(self):
        self.generate_image(path=FREE_IMAGE, title="Test Free Tier", tier="free")

    def test_premium_tier(self):
        self.generate_image(path=PREMIUM_IMAGE, title="Test Premium Tier", tier="premium")

    def test_custom_font(self):
        self.generate_image(path=CUSTOM_FONT_IMAGE, title="Test Custom Font", font="assets/fonts/arial.ttf")

    def test_custom_font_strange_height(self):
        self.generate_image(
            path=CUSTOM_FONT_IMAGE,
            title="Test Custom Font Strange Height",
            font="assets/fonts/gadugi.ttf"
        )

    def test_special_chars_in_title(self):
        test_image = _process_image(path=SPECIAL_IMAGE, title="Test Special Chars?")
        save_copies([test_image], path=SPECIAL_IMAGE, output_path=TEST_SOLO_DUMP, title="Test Special Chars?")

    def test_one_line_title(self):
        self.generate_image(path=ONE_LINE_TITLE_IMAGE, title="TestSingleLineFile")


class TestProcessImage(TestUtilities):

    def setUp(self) -> None:
        self.size = (1920, 960)
        self.input_image = Image.open(DEFAULT_IMAGE)
        self.default_image = _process_image(path=DEFAULT_IMAGE, title="Test Default Image")
        self.different_title_image = _process_image(path=DEFAULT_IMAGE, title="Test Different Logo Image")

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
        _process_batch(path=ASSETS, output_path=TEST_BATCH_DUMP + "/default")

    def test_batch_free_tier(self):
        _process_batch(path=ASSETS, tier="free", output_path=TEST_BATCH_DUMP + "/free-tier")

    def test_batch_premium_tier(self):
        _process_batch(path=ASSETS, tier="premium", output_path=TEST_BATCH_DUMP + "/premium-tier")


class TestConvertFileNameToTitle(TestUtilities):

    def test_default(self):
        title = _convert_file_name_to_title()
        self.assertEqual(None, title)

    def test_custom_title(self):
        title = _convert_file_name_to_title(title="How to Loop in Python")
        self.assertEqual("How to Loop in Python", title)

    def test_custom_path(self):
        title = _convert_file_name_to_title(path="how-to-loop-in-python.png")
        self.assertEqual("How to Loop in Python", title)

    def test_custom_separator(self):
        title = _convert_file_name_to_title(path="how.to.loop.in.python.png", separator=".")
        self.assertEqual("How to Loop in Python", title)


class TestGetBestTopColor(TestUtilities):

    def test_renegade_coder_icon(self):
        img: Image.Image = Image.open(TRC_ICON_PATH)
        color = _get_best_top_color(img)
        self.assertEqual(color, TRC_RED)
        img.close()

    def test_virtual_flat_icon(self):
        img: Image.Image = Image.open(VF_ICON_PATH)
        color = _get_best_top_color(img)
        self.assertEqual(color, VF_BLUE)
        img.close()


class TestSplitString(TestUtilities):

    def test_first_space(self):
        top, bottom = _split_string_by_nearest_middle_space("Split first one")
        self.assertEqual(top, "Split")
        self.assertEqual(bottom, "first one")

    def test_middle_space(self):
        top, bottom = _split_string_by_nearest_middle_space("Hello World")
        self.assertEqual(top, "Hello")
        self.assertEqual(bottom, "World")

    def test_last_space(self):
        top, bottom = _split_string_by_nearest_middle_space("Split last opening")
        self.assertEqual(top, "Split last")
        self.assertEqual(bottom, "opening")
