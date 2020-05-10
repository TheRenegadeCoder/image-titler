"""
The commandline interface for the image-titler script.
"""

from titler.draw import process_images
from titler.parse import parse_input
from titler.store import save_copies


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
