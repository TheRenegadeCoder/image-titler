"""
The commandline interface for the image-titler script.
"""

import tkinter
from tkinter.filedialog import askopenfilename, askdirectory
from typing import Optional

from titler.draw import process_images
from titler.parse import parse_input
from titler.store import save_copies
from titler.constants import *


def _request_input_path(**kwargs) -> Optional[str]:
    """
    A helper function which asks the user for an input path
    if one is not supplied on the command line. In this implementation,
    the type of request we make (e.g. file vs. folder) depends on the state of batch.

    :return: the input path after the request or None if the user does not select one
    """
    input_path = kwargs.get(KEY_PATH)
    batch = kwargs.get(KEY_BATCH)
    if not input_path:
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


def main() -> None:
    """
    The main function.

    :return: None
    """
    args = vars(parse_input())
    args[KEY_PATH] = _request_input_path(**args)
    if args[KEY_PATH]:
        images = process_images(**args)
        save_copies(images, **args)


if __name__ == '__main__':
    main()
