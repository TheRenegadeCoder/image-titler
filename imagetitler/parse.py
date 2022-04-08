import argparse

from imagetitler.constants import *


def parse_input() -> argparse.Namespace:
    """
    Parses the command line input.

    :return: the processed command line arguments
    """
    parser = argparse.ArgumentParser()
    _add_title_option(parser)
    _add_path_option(parser)
    _add_output_path_option(parser)
    _add_tier_option(parser)
    _add_logo_path_option(parser)
    _add_batch_option(parser)
    _add_font_option(parser)
    _add_custom_size_option(parser)
    args = parser.parse_args()
    return args


def _add_title_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the title settings for the parser.
    The title is then used to add a custom title to the image.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-t',
        f'--{KEY_TITLE}',
        help="add a custom title to the image"
    )


def _add_path_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the path settings for the parser.
    The path setting determines which file or folder is to be processed.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-p',
        f'--{KEY_PATH}',
        help="select an image file (or folder when batch processing)"
    )


def _add_output_path_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the output path settings for the parser.
    The output path setting determines where the file will be stored.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-o',
        f'--{KEY_OUTPUT_PATH}',
        help="select an output path for the processed image"
    )


def _add_tier_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the tier setting for the parser.
    The tier setting determines the border color of the title bars.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-r',
        f'--{KEY_TIER}',
        choices=TIER_MAP.keys(),
        help="select an image tier"
    )


def _add_logo_path_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the logo path setting for the parser.
    The logo path setting is used to display a logo on the image.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-l',
        f'--{KEY_LOGO_PATH}',
        help="select a logo file for addition to the processed image"
    )


def _add_batch_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the batch settings for the parser.
    The batch is then used to determine the type of image processing performed.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-b',
        f'--{KEY_BATCH}',
        default=DEFAULT_BATCH_MODE,
        action='store_true',
        help="turn on batch processing"
    )


def _add_font_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the font settings for the parser.
    The font is then used to change the appearance of the title.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        '-f',
        f'--{KEY_FONT}',
        default=DEFAULT_FONT,
        help="change the default font by path (e.g. 'arial.ttf')"
    )


def _add_custom_size_option(parser: argparse.ArgumentParser) -> None:
    """
    A helper function which sets up the size options for the parser.
    The size is then used to resize and crop input images.

    :param parser: an argument parser
    :return: None
    """
    parser.add_argument(
        "-s",
        f'--{KEY_SIZE}',
        choices=SIZE_MAP.keys(),  # [f'{k} {v}' for k, v in SIZE_MAP.items()]
        help="change the default size of the output image"
    )
