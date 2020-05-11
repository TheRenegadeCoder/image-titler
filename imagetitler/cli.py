"""
The commandline interface for the image-titler script.
"""

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
