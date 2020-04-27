from unittest import TestCase

from image_titler import trc_image_titler
import sys


class TestImageTitler(TestCase):
    pass


class TestSplitString(TestImageTitler):

    def test_first_space(self):
        top, bottom = trc_image_titler.split_string_by_nearest_middle_space("Split first one")
        self.assertEqual("Split", top)
        self.assertEqual("first one", bottom)

    def test_middle_space(self):
        top, bottom = trc_image_titler.split_string_by_nearest_middle_space("Hello World")
        self.assertEqual("Hello", top)
        self.assertEqual("World", bottom)

    def test_last_space(self):
        top, bottom = trc_image_titler.split_string_by_nearest_middle_space("Split last opening")
        self.assertEqual("Split last", top)
        self.assertEqual("opening", bottom)


class TestParseInput(TestImageTitler):

    def test_default(self):
        args = trc_image_titler.parse_input()
        self.assertEqual(False, args.batch)
        self.assertEqual(None, args.path)
        self.assertEqual("", args.tier)
        self.assertEqual(None, args.output_path)
        self.assertEqual(None, args.logo_path)
        self.assertEqual(None, args.title)

    def test_title(self):
        sys.argv.append("-t")
        sys.argv.append("Hello World")
        args = trc_image_titler.parse_input()
        self.assertEqual(False, args.batch)
        self.assertEqual(None, args.path)
        self.assertEqual("", args.tier)
        self.assertEqual(None, args.output_path)
        self.assertEqual(None, args.logo_path)
        self.assertEqual("Hello World", args.title)

