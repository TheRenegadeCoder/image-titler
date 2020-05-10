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


def main() -> None:
    """
    The main function.

    :return: None
    """
    args = vars(parse_input())
    images = process_images(**args)
    save_copies(images, **args)


if __name__ == '__main__':
    main()
