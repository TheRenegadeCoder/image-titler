import shutil
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import pkg_resources
from PIL import Image

from titler.draw import process_images
from titler.parse import parse_input
from titler.store import save_copies

TRC_ICON_PATH = "assets/icons/the-renegade-coder-sample-icon.png"
TRC_RED = (201, 2, 41, 255)

VF_ICON_PATH = "assets/icons/virtual-flat-sample-icon.png"
VF_BLUE = (0, 164, 246, 255)

IMAGE_FOLDER = "assets/images"
DEFAULT_IMAGE = "assets/images/23-tech-topics-to-tackle.jpg"
LOGO_RED_IMAGE = "assets/images/welcome-to-the-image-titler-by-the-renegade-coder.jpg"
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

    def setUp(self) -> None:
        sys.argv = list()

    @staticmethod
    def _generate_images(command: list):
        with patch.object(sys, "argv", command):
            args = vars(parse_input())
            images = process_images(**args)
            save_copies(images, **args)

    @staticmethod
    def _generate_test_images(command: list):
        test_command = command.copy()
        test_command.extend(["-o", TEST_SOLO_DUMP])
        TestIntegration._generate_images(test_command)

    @staticmethod
    def _generate_sample_images(command: list):
        sample_command = command.copy()
        sample_command.extend(["-o", SAMPLE_DUMP])
        TestIntegration._generate_images(sample_command)

    def test_default(self):
        TestIntegration._generate_test_images(["image-titler"])

    def test_custom_path(self):
        TestIntegration._generate_test_images(["image-titler", "--path", DEFAULT_IMAGE])

    def test_custom_title(self):
        TestIntegration._generate_test_images(["image-titler", "--title", "Test Custom Title"])

    def test_free_tier(self):
        TestIntegration._generate_test_images(["image-titler", "--title", "Test Free Tier", "--tier", "free"])

    def test_premium_tier(self):
        TestIntegration._generate_test_images(["image-titler", "--title", "Test Premium Tier", "--tier", "premium"])


class TestParseInput(TestUtilities):

    def test_default(self):
        with patch.object(sys, "argv", ["image-titler"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_title(self):
        with patch.object(sys, "argv", ["image-titler", "-t", "Hello World"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, "Hello World")

    def test_path(self):
        with patch.object(sys, "argv", ["image-titler", "-p", "path/to/stuff"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, "path/to/stuff")
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_output_path(self):
        with patch.object(sys, "argv", ["image-titler", "-o", "path/to/stuff"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, "path/to/stuff")
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_logo_path(self):
        with patch.object(sys, "argv", ["image-titler", "-l", "path/to/stuff"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, "path/to/stuff")
            self.assertEqual(args.title, None)

    def test_batch(self):
        with patch.object(sys, "argv", ["image-titler", "-b"]):
            args = parse_input()
            self.assertEqual(args.batch, True)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, None)
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_tier_premium(self):
        with patch.object(sys, "argv", ["image-titler", "-r", "premium"]):
            args = parse_input()
            self.assertEqual(args.batch, False)
            self.assertEqual(args.path, None)
            self.assertEqual(args.tier, "premium")
            self.assertEqual(args.output_path, None)
            self.assertEqual(args.logo_path, None)
            self.assertEqual(args.title, None)

    def test_tier_free(self):
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
        self.images.extend(process_images(title="Test Custom Font", font="assets/fonts/arial.ttf"))
        self.assertEqual(1, len(self.images))

    def test_custom_font_strange_height(self) -> None:
        """
        Tests the vertical alignment of the text placement algorithm for customs fonts with a strange height.

        :return: None
        """
        self.images.extend(process_images(title="Test Custom Font Strange Height", font="assets/fonts/gadugi.ttf"))
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

    def verify_existence_and_delete(self) -> None:
        """
        Verifies that a file exists and deletes it.

        :return: None
        """
        for path in self.paths:
            p = Path(path)
            self.assertTrue(p.exists(), f"{p} does not exist")
            p.unlink()

    def test_zero_images(self) -> None:
        """
        Tests the scenario when no images are passed to this function.
        It should return an empty list (since there were no files
        to process).

        :return: None
        """
        self.paths.extend(save_copies(list()))
        self.assertEqual(list(), self.paths)

    def test_one_image(self) -> None:
        """
        Tests the scenario when a single image is passed to this function.
        It should save that image and return a list which contains a single
        path to that image.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES[:1]))
        self.verify_existence_and_delete()

    def test_many_images(self) -> None:
        """
        Tests the scenario when multiple images are passed to this function.
        It should save each image to a unique path and return those paths
        in a list.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES))
        self.verify_existence_and_delete()

    def test_many_title(self) -> None:
        """
        Tests the scenario when multiple images are passed to this function with
        the title option provided. It should save each image to a unique path
        regardless of the fact they they'll all have the same core filename.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES, title="Test Many With Title Option"))
        self.verify_existence_and_delete()

    def test_special_characters_in_title(self) -> None:
        """
        Tests the scenario when a title is provided with a special character in it.
        It should save that file with all the special characters removed.

        :return: None
        """
        self.paths.extend(save_copies(TEST_IMAGES, title="Test Special Chars?"))
        self.verify_existence_and_delete()
