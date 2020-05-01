import argparse
import tkinter
from tkinter.filedialog import askopenfilename, askdirectory
from typing import Optional

from image_titler.utilities import process_batch, process_image, TIER_MAP, FILE_TYPES, save_copy, \
    convert_file_name_to_title


def _request_input_path(path: str, batch: bool) -> Optional[str]:
    """
    A helper function which asks the user for an input path
    if one is not supplied on the command line. In this implementation,
    the type of request we make (e.g. file vs. folder) depends on the state of batch.

    :param path: a folder or file path
    :param batch: tells us if we are in batch mode or not
    :return: the input path after the request or None if the user does not select one
    """
    input_path = path
    if not path:
        tkinter.Tk().withdraw()
        if not batch:
            input_path = askopenfilename(
                title="Select an Image File",
                filetypes=FILE_TYPES
            )
        else:
            input_path = askdirectory(
                title="Select a Folder of Images"
            )
    return input_path


def parse_input() -> argparse.Namespace:
    """
    Creates and executes a parser on the command line inputs.

    :return: the processed command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', help="add a custom title to the image (no effect when batch processing)")
    parser.add_argument('-p', '--path', help="select an image file")
    parser.add_argument('-o', '--output_path', help="select an output path for the processed image")
    parser.add_argument('-r', '--tier', default="", choices=TIER_MAP.keys(),
                        help="select an image tier")
    parser.add_argument('-l', '--logo_path', help="select a logo file for addition to the processed image")
    parser.add_argument('-b', '--batch', default=False, action='store_true', help="turn on batch processing")
    args = parser.parse_args()
    return args


def title_image(args: argparse.Namespace) -> None:
    """
    Titles an image based on a set of arguments.

    :param args: a set of arguments
    :return: None
    """
    path: str = args.path
    batch: bool = args.batch
    tier: str = args.tier
    logo_path: str = args.logo_path
    output_path: str = args.output_path
    title: str = args.title
    input_path = _request_input_path(path, batch)
    if input_path:
        if args.batch:
            process_batch(input_path, tier, logo_path, output_path)
        else:
            title = convert_file_name_to_title(input_path, title=title)
            edited_image = process_image(
                input_path,
                title,
                tier=tier,
                logo_path=logo_path,
            )
            edited_image.show()
            save_copy(input_path, edited_image, output_path=output_path, title=title)


def main() -> None:
    """
    The main function.

    :return: None
    """
    args = parse_input()
    title_image(args)


if __name__ == '__main__':
    main()
