import shutil
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import pkg_resources
from PIL import Image
from imagetitler import cli

from imagetitler.draw import process_images
from imagetitler.parse import parse_input
from imagetitler.store import save_copies

CUSTOM_FONT = "imagetitler/assets/fonts/arial.ttf"
CUSTOM_FONT_TALL = "imagetitler/assets/fonts/gadugi.ttf"

TRC_ICON_PATH = "imagetitler/assets/icons/the-renegade-coder-sample-icon.png"
TRC_RED = (201, 2, 41, 255)

VF_ICON_PATH = "imagetitler/assets/icons/virtual-flat-sample-icon.png"
VF_BLUE = (0, 164, 246, 255)

IMAGE_FOLDER = "imagetitler/assets/images"
DEFAULT_IMAGE = "imagetitler/assets/images/welcome-to-the-image-titler-by-the-renegade-coder.jpg"
LOGO_RED_IMAGE = "imagetitler/assets/images/23-tech-topics-to-tackle.jpg"
LOGO_BLUE_IMAGE = "imagetitler/assets/images/hello-world-in-matlab.jpg"
FREE_IMAGE = "imagetitler/assets/images/columbus-drivers-are-among-the-worst.jpg"
PREMIUM_IMAGE = "imagetitler/assets/images/the-guide-to-causing-mass-panic.jpg"
SPECIAL_IMAGE = "imagetitler/assets/images/happy-new-year.jpg"
CUSTOM_FONT_IMAGE = "imagetitler/assets/images/reflecting-on-my-third-semester-of-teaching.jpg"
ONE_LINE_TITLE_IMAGE = "imagetitler/assets/images/minimalism.jpg"
YOUTUBE_IMAGE = "imagetitler/assets/images/the-art-of-simplification.jpg"
TRAILING_SPACE_IMAGE = "imagetitler/assets/images/how-to-iterate-over-multiple-lists-at-the-same-time-in-python.jpg"

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
        ONE_LINE_TITLE_IMAGE,
        YOUTUBE_IMAGE,
        TRAILING_SPACE_IMAGE
    ]
]

TEST_DUMP = "imagetitler/tests/dump"
TEST_SOLO_DUMP = TEST_DUMP + "/solo"
TEST_BATCH_DUMP = TEST_DUMP + "/batch"
SAMPLE_DUMP = "samples/v" + pkg_resources.require("image-titler")[0].version


class TestUtilities(TestCase):
    pass


class TestIntegration(TestUtilities):
    """
    An integration test class which the three core functions in series.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up storage paths for testing.

        :return: None
        """
        try:
            shutil.rmtree(TEST_SOLO_DUMP)
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(TEST_BATCH_DUMP)
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(SAMPLE_DUMP)
        except FileNotFoundError:
            pass

        Path(TEST_SOLO_DUMP).mkdir(parents=True, exist_ok=True)
        Path(TEST_BATCH_DUMP).mkdir(parents=True, exist_ok=True)
        Path(SAMPLE_DUMP).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _generate_images(command: list) -> None:
        """
        Generates a set of images from a command list.

        :param command: a spliced up command as a list
        :return: None
        """
        with patch.object(sys, "argv", command):
            cli.main()

    @staticmethod
    def _generate_solo_test_image(command: list) -> None:
        """
        Generates a test image by appending the output path option
        for the TEST_SOLO_DUMP path.

        :param command: a splice up command as a list
        :return: None
        """
        test_command = command.copy()
        test_command.extend(["-o", TEST_SOLO_DUMP])
        TestIntegration._generate_images(test_command)

    @staticmethod
    def _generate_batch_test_images(command: list) -> None:
        """
        Generates a test image set by appending the output path option
        for the TEST_BATCH_DUMP path.

        :param command: a splice up command as a list
        :return: None
        """
        test_command = command.copy()
        test_command.extend(["-o", TEST_BATCH_DUMP])
        TestIntegration._generate_images(test_command)

    @staticmethod
    def _generate_sample_image(command: list) -> None:
        """
        Generates a sample image by appending the output path option
        for the SAMPLE_DUMP path.

        :param command: a splice up command as a list
        :return: None
        """
        sample_command = command.copy()
        sample_command.extend(["-o", SAMPLE_DUMP])
        TestIntegration._generate_images(sample_command)

    def test_default(self) -> None:
        """
        Tests the following command: image-titler

        The resulting image should be the default image.

        :return: None
        """
        default = ["image-titler"]
        TestIntegration._generate_solo_test_image(default)
        TestIntegration._generate_sample_image(default)

    def test_custom_title(self) -> None:
        """
        Tests the following command: image-titler -t "Test Custom Title"

        The resulting image should have the custom title on the default image.

        :return: None
        """
        custom_title = ["image-titler", "--title", "Test Custom Title"]
        TestIntegration._generate_solo_test_image(custom_title)

    def test_custom_path(self) -> None:
        """
        Tests the following command: image-titler -p DEFAULT_IMAGE -t "Test Custom Path"

        The resulting image should have a title built from the file name.

        :return: None
        """
        custom_path = ["image-titler", "--path", DEFAULT_IMAGE, "--title", "Test Custom Path"]
        TestIntegration._generate_solo_test_image(custom_path)
        TestIntegration._generate_sample_image(custom_path[:-2])

    def test_free_tier(self) -> None:
        """
        Tests the following command: image-titler -p FREE_IMAGE -r free -t "Test Free Tier"

        The resulting image should have a silver border around the title bar.

        :return: None
        """
        free_tier = ["image-titler", "--path", FREE_IMAGE, "--tier", "free", "--title", "Test Free Tier"]
        TestIntegration._generate_solo_test_image(free_tier)
        TestIntegration._generate_sample_image(free_tier[:-2])

    def test_premium_tier(self) -> None:
        """
        Tests the following command: image-titler -p PREMIUM_IMAGE -r premium -t "Test Premium Tier"

        The resulting image should have a gold border around the title bar.

        :return: None
        """
        premium_tier = ["image-titler", "--path", PREMIUM_IMAGE, "--tier", "premium", "--title", "Test Premium Tier"]
        TestIntegration._generate_solo_test_image(premium_tier)
        TestIntegration._generate_sample_image(premium_tier[:-2])

    def test_red_logo(self) -> None:
        """
        Tests the following command: image-titler -p LOGO_RED_IMAGE -l TRC_ICON_PATH -t "Test Red Logo"

        The resulting image should have a red logo in the lower left corner.

        :return: None
        """
        red_logo = ["image-titler", "--path", LOGO_RED_IMAGE, "--logo_path", TRC_ICON_PATH, "--title", "Test Red Logo"]
        TestIntegration._generate_solo_test_image(red_logo)
        TestIntegration._generate_sample_image(red_logo[:-2])

    def test_blue_logo(self) -> None:
        """
        Tests the following command: image-titler -p LOGO_BLUE_IMAGE -l VF_ICON_PATH -t "Test Blue Logo"

        The resulting image should have a blue logo in the lower left corner (and blue title bars)

        :return: None
        """
        blue_logo = ["image-titler", "--path", LOGO_BLUE_IMAGE, "--logo_path", VF_ICON_PATH, "--title", "Test Blue Logo"]
        TestIntegration._generate_solo_test_image(blue_logo)
        TestIntegration._generate_sample_image(blue_logo[:-2])

    def test_custom_font(self) -> None:
        """
        Tests the following command: image-titler -p CUSTOM_FONT_IMAGE -f CUSTOM_FONT -t "Test Custom Font"

        The resulting image should have a title in arial font.

        :return: None
        """
        custom_font = ["image-titler", "--path", CUSTOM_FONT_IMAGE, "--font", CUSTOM_FONT, "--title", "Test Custom Font"]
        TestIntegration._generate_solo_test_image(custom_font)
        TestIntegration._generate_sample_image(custom_font[:-2])

    def test_one_line_title(self) -> None:
        """
        Tests the following command: image-titler -p ONE_LINE_TITLE_IMAGE -t "OneLineTitle"

        The resulting image should have a single line title.

        :return: None
        """
        one_line_title = ["image-titler", "--path", ONE_LINE_TITLE_IMAGE, "--title", "OneLineTitle"]
        TestIntegration._generate_solo_test_image(one_line_title)
        TestIntegration._generate_sample_image(one_line_title[:-2])

    def test_batch_default(self) -> None:
        """
        Tests the following command: image-titler -b

        The resulting images should be generated from a default location.

        :return: None
        """
        batch = ["image-titler", "-b"]
        TestIntegration._generate_batch_test_images(batch)

    def test_size_youtube(self) -> None:
        """
        Tests the following command: image-titler -p YOUTUBE_IMAGE -s "YouTube" -t "Test YouTube Size"

        The resulting image should have the dimensions of a YouTube thumbnail.

        :return: None
        """
        size = ["image-titler", "--path", YOUTUBE_IMAGE, "-s", "YouTube", "--title", "Test YouTube Size"]
        TestIntegration._generate_solo_test_image(size)
        TestIntegration._generate_sample_image(size[:-2])

    def test_trailing_spaces(self) -> None:
        """
        Tests the following command: image-titler -p -t "Test Trailing Spaces   "

        :return: None
        """
        trailing_spaces = ["image-titler", "--path", TRAILING_SPACE_IMAGE, "--title", "Test Trailing Spaces"]
        TestIntegration._generate_solo_test_image(trailing_spaces)
        TestIntegration._generate_sample_image(trailing_spaces[:-2])


class TestParseInput(TestUtilities):
    """
    A test class for the parse.py file—specifically, the parse_input() function.
    """

    def test_default(self) -> None:
        """
        Tests that all the defaults are in a falsey state.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_title(self) -> None:
        """
        Tests that the title is properly stored.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-t", "Hello World"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, "Hello World")

    def test_path(self) -> None:
        """
        Tests that the input path is properly stored.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-p", "path/to/stuff"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, "path/to/stuff")
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_output_path(self) -> None:
        """
        Tests that the output path is properly stored.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-o", "path/to/stuff"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, "path/to/stuff")
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_logo_path(self) -> None:
        """
        Tests that the logo path is properly stored.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-l", "path/to/stuff"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, "path/to/stuff")
            self.assertEqual(args.title, None)

    def test_batch(self) -> None:
        """
        Tests that the batch setting is properly set to True.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-b"]):
            args = parse_input()
            self.assertEqual(args.batch, True)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_tier_premium(self) -> None:
        """
        Tests that the premium tier is properly stored.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-r", "premium"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, "premium")
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_tier_free(self) -> None:
        """
        Tests that the free tier is properly stored.

        :return: None
        """
        with patch.object(sys, "argv", ["image-titler", "-r", "free"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, "free")
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)


class TestProcessImages(TestUtilities):
    """
    A test class for the draw.py file—specifically the only exposed function, process_images.
    """

    def setUp(self) -> None:
        """
        Prepares an empty list of images for each test.

        :return:
        """
        self.images = list()

    def test_zero_images(self) -> None:
        """
        Tests that a default image is properly returned when no files are passed.

        :return: None
        """
        self.images.extend(process_images())
        self.assertEqual(1, len(self.images))

    def test_one_image(self) -> None:
        """
        Tests the single image processing feature.

        :return: None
        """
        self.images.extend(process_images(path=DEFAULT_IMAGE))
        self.assertEqual(1, len(self.images))

    def test_many_images(self) -> None:
        """
        Tests the batch processing feature.

        :return: None
        """
        self.images.extend(process_images(path=IMAGE_FOLDER, batch=True))
        self.assertEqual(len(TEST_IMAGES), len(self.images))

    def test_one_line_title(self) -> None:
        """
        Tests that the split text algorithm properly handles single term titles.

        :return: None
        """
        self.images.extend(process_images(title="TestSingleLineFile"))
        self.assertEqual(1, len(self.images))

    def test_red_logo(self) -> None:
        """
        Tests the rendering of a logo.

        :return: None
        """
        self.images.extend(process_images(title="Test Red Logo", logo_path=TRC_ICON_PATH))

    def test_logo_blue(self) -> None:
        """
        Tests the rendering of the blue logo while also testing the color detection algorithm.

        :return: None
        """
        self.images.extend(process_images(title="Test Blue Logo", logo_path=VF_ICON_PATH))

    def test_free_tier(self) -> None:
        """
        Tests the rendering of the free tier on the title bar.

        :return: None
        """
        self.images.extend(process_images(title="Test Free Tier", tier="free"))

    def test_premium_tier(self) -> None:
        """
        Tests the rendering of the premium tier on the title bar.

        :return: None
        """
        self.images.extend(process_images(title="Test Premium Tier", tier="premium"))

    def test_custom_font(self) -> None:
        """
        Tests the rendering of a custom font on the title bar.

        :return: None
        """
        self.images.extend(process_images(title="Test Custom Font", font=CUSTOM_FONT))
        self.assertEqual(1, len(self.images))

    def test_custom_font_strange_height(self) -> None:
        """
        Tests the vertical alignment of the text placement algorithm for customs fonts with a strange height.

        :return: None
        """
        self.images.extend(process_images(title="Test Custom Font Strange Height", font=CUSTOM_FONT_TALL))
        self.assertEqual(1, len(self.images))


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

    def tearDown(self) -> None:
        """
        Deletes all files in paths list.

        :return: None
        """
        for path in self.paths:
            Path(path).unlink()

    def verify_existence(self) -> None:
        """
        Verifies that a file exists and deletes it.

        :return: None
        """
        for path in self.paths:
            p = Path(path)
            self.assertTrue(p.exists(), f"{p} does not exist")

    def test_zero_images(self) -> None:
        """
        Tests the scenario when no images are passed to this function.
        It should return an empty list (since there were no files
        to process).

        :return: None
        """
        self.paths.extend(save_copies(list()))
        self.assertEqual(0, len(self.paths))
        self.assertEqual(list(), self.paths)

    def test_one_image(self) -> None:
        """
        Tests the scenario when a single image is passed to this function.
        It should save that image and return a list which contains a single
        path to that image.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES))
        self.assertEqual(1, len(self.paths))
        self.verify_existence()

    def test_many_images(self) -> None:
        """
        Tests the scenario when multiple images are passed to this function.
        It should save each image to a unique path and return those paths
        in a list.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES))
        self.assertEqual(1, len(self.paths))
        self.verify_existence()

    def test_many_title(self) -> None:
        """
        Tests the scenario when multiple images are passed to this function with
        the title option provided. It should save each image to a unique path
        regardless of the fact they they'll all have the same core filename.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES, title="Test Many With Title Option", batch=True))
        self.assertEqual(len(TEST_IMAGES), len(self.paths))
        self.verify_existence()

    def test_special_characters_in_title(self) -> None:
        """
        Tests the scenario when a title is provided with a special character in it.
        It should save that file with all the special characters removed.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES, title="Test Special Chars?"))
        self.assertEqual(1, len(self.paths))
        self.verify_existence()
