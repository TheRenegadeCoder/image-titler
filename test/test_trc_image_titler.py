from unittest import TestCase

from image_titler import trc_image_titler


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


