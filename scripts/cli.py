"""
The commandline interface for the image-titler script.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        os.pardir
    )
)
sys.path.append(PROJECT_ROOT)

from imagetitler.draw import process_images
from imagetitler.parse import parse_input
from imagetitler.store import save_copies


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
