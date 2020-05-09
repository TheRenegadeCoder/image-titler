"""
The commandline interface for the image-titler script.
"""

import tkinter
from tkinter.filedialog import askopenfilename, askdirectory

from image_titler.utilities import *


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


def _title_image(**kwargs) -> None:
    """
    Titles an image based on a set of arguments.

    :return: None
    """
    path: Optional[str] = kwargs.get("path")
    batch: bool = kwargs.get("batch")
    input_path = _request_input_path(path, batch)
    kwargs["path"] = input_path
    if input_path:
        if batch:
            process_batch(**kwargs)
        else:
            edited_image = process_image(**kwargs)
            edited_image.show()
            save_copy(edited_image, **kwargs)


def main() -> None:
    """
    The main function.

    :return: None
    """
    args = parse_input()
    _title_image(**vars(args))


if __name__ == '__main__':
    main()
