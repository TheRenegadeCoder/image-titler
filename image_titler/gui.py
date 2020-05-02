"""
The GUI interface for the image-titler script.
"""

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from typing import Optional

import pkg_resources
from PIL import ImageTk, Image
from matplotlib import font_manager

from image_titler.utilities import process_image, convert_file_name_to_title, save_copy, TIER_MAP, FILE_TYPES, FONT

TRC_ICON = os.path.join(os.path.dirname(__file__), '../icons/the-renegade-coder-sample-icon.png')

FONTS = {f.name: f.fname for f in font_manager.fontManager.ttflist}

FILE_TAB_LABEL = "File"
NEW_IMAGE_LABEL = "New Image"
NEW_LOGO_LABEL = "New Logo"
SAVE_AS_LABEL = "Save As"
TITLE_OPTION_LABEL = "Title:"
TIER_OPTION_LABEL = "Tier:"
LOGO_OPTION_LABEL = "Logo:"

COLUMN_WIDTH = 8


class ImageTitlerMain(tk.Tk):
    """
    The main window. This overrides the root class of tk, so we can make a menu.
    The remainder of the GUI is contained within a frame.
    """

    def __init__(self):
        super().__init__()
        self.menu = ImageTitlerMenuBar(self)
        self.gui = ImageTitlerGUI(self, self.menu)
        self.gui.pack(anchor=tk.W)

    def update_view(self) -> None:
        """
        Updates what's happening visually in the app.

        :return: None
        """
        self.gui.update_view()

    def save_as(self) -> None:
        """
        A save method which saves our preview. This has to exist because the menu
        has no concept of title. As a result, this method needed to be pulled up
        into main window. That way, we at least decouple the child to parent
        relationship (i.e. children have to concept of siblings, etc.).

        :return: None
        """
        title = convert_file_name_to_title(
            self.menu.image_path,
            title=self.gui.option_pane.title_value.get()
        )
        save_copy(
            self.menu.image_path,
            self.menu.current_edit,
            output_path=self.menu.output_path,
            title=title
        )


class ImageTitlerGUI(ttk.Frame):
    """
    The main content of the GUI. This contains the preview pane and the option pane.
    """

    def __init__(self, parent, menu, **kw):
        super().__init__(parent, **kw)
        self.menu = menu
        self.preview = ImageTitlerPreviewPane(self, text=f"Select a file using '{FILE_TAB_LABEL}' > '{NEW_IMAGE_LABEL}'")
        self.option_pane = ImageTitlerOptionPane(self)
        self.logo_path = None
        self.set_layout()

    def set_layout(self) -> None:
        """
        Sets the layout of the window. Specifically, this function places the option pane
        on the left and the preview pane on the right.

        :return: None
        """
        self.preview.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)
        self.option_pane.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)

    def update_view(self, *_) -> None:
        """
        Updates this frame visually by controlling what is happening in children components.

        :return: None
        """
        if self.menu.image_path:
            title = None
            tier = ""
            logo_path = None
            text_font = FONT
            if self.option_pane.title_state.get() == 1:
                title = self.option_pane.title_value.get()
            if self.option_pane.tier_state.get() == 1:
                tier = self.option_pane.tier_value.get()
            if self.option_pane.logo_state.get() == 1:
                logo_path = self.menu.logo_path
            if self.option_pane.font_state.get() == 1:
                text_font = FONTS.get(self.option_pane.font_value.get())
            self._render_preview(title, tier=tier, logo_path=logo_path, text_font=text_font)
        self._render_logo(self.menu.logo_path)

    def _render_preview(self, title, tier="", logo_path=None, text_font=FONT) -> None:
        """
        Renders a preview of the edited image in the child preview pane.

        :param title: the title of the image
        :param tier: the tier of the image
        :param logo_path: the path to the logo for the image
        :return: None
        """
        title = convert_file_name_to_title(self.menu.image_path, title=title)
        self.menu.current_edit = process_image(
            self.menu.image_path,
            title,
            tier=tier,
            logo_path=logo_path,
            font=text_font
        )
        maxsize = (1028, 1028)
        small_image = self.menu.current_edit.copy()
        small_image.thumbnail(maxsize, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(small_image)
        self.preview.config(image=image)
        self.preview.image = image

    def _render_logo(self, logo_path: Optional[str]) -> None:
        """
        Renders a preview of the logo in the options pane.

        :param logo_path: the path to a logo
        :return: None
        """
        if logo_path and logo_path != self.logo_path:
            self.logo_path = logo_path
            maxsize = (50, 50)
            small_image = Image.open(logo_path)
            small_image.thumbnail(maxsize, Image.ANTIALIAS)
            image = ImageTk.PhotoImage(small_image)
            self.option_pane.logo_value.config(image=image)
            self.option_pane.logo_value.image = image


class ImageTitlerPreviewPane(ttk.Label):
    """
    The preview pane is a simple label which contains a preview of the
    image currently being edited.
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)


class ImageTitlerOptionPane(ttk.Frame):
    """
    The option pane contains a set of options that can be controlled when editing the image.
    Changes are reflected in the preview pane.
    """

    def __init__(self, parent: ImageTitlerGUI, **kw):
        super().__init__(parent, **kw)
        self.parent = parent
        self.title_state: tk.IntVar = tk.IntVar()
        self.title_value: tk.StringVar = tk.StringVar()
        self.tier_state: tk.IntVar = tk.IntVar()
        self.tier_value: tk.StringVar = tk.StringVar()
        self.logo_state: tk.IntVar = tk.IntVar()
        self.logo_value: Optional[ttk.Label] = None
        self.font_state: tk.IntVar = tk.IntVar()
        self.font_value: tk.StringVar = tk.StringVar()
        self.init_option_pane()

    def init_option_pane(self) -> None:
        """
        Initializes the option pane by generating rows of settings.

        :return: None
        """
        rows = list()
        rows.append(self.init_title_frame())
        rows.append(self.init_tier_frame())
        rows.append(self.init_logo_frame())
        rows.append(self.init_font_frame())
        for row in rows:
            self._layout_option_row(*row)

    def init_title_frame(self) -> tuple:
        """
        Initializes the row for title information.

        :return: a tuple containing the title container and its two children (see layout_option_row for order)
        """
        title_frame = ttk.Frame(self)
        title_label = ttk.Checkbutton(
            title_frame,
            text=TITLE_OPTION_LABEL,
            variable=self.title_state,
            command=self.parent.update_view,
            width=COLUMN_WIDTH
        )
        self.title_value.trace(tk.W, self.parent.update_view)
        title_entry = tk.Entry(title_frame, textvariable=self.title_value)
        return title_frame, title_label, title_entry

    def init_tier_frame(self) -> tuple:
        """
        Initializes the row for tier information.

        :return: a tuple containing the tier container and its two children (see layout_option_row for order)
        """
        tier_frame = ttk.Frame(self)
        tier_label = ttk.Checkbutton(
            tier_frame,
            text=TIER_OPTION_LABEL,
            variable=self.tier_state,
            command=self.parent.update_view,
            width=COLUMN_WIDTH
        )
        self.tier_value.set(list(TIER_MAP.keys())[0])
        tier_option_menu = ttk.Combobox(
            tier_frame,
            textvariable=self.tier_value,
            values=list(TIER_MAP.keys()),
            state="readonly"
        )
        tier_option_menu.bind("<<ComboboxSelected>>", self.parent.update_view)
        return tier_frame, tier_label, tier_option_menu

    def init_logo_frame(self) -> tuple:
        """
        Initializes the row for logo information.

        :return: a tuple containing the logo container and its two children (see layout_option_row for order)
        """
        logo_frame = ttk.Frame(self)
        logo_label = ttk.Checkbutton(
            logo_frame,
            text=LOGO_OPTION_LABEL,
            variable=self.logo_state,
            command=self.parent.update_view,
            width=COLUMN_WIDTH
        )
        self.logo_value = ttk.Label(logo_frame, text=f"Select a logo using '{FILE_TAB_LABEL}' > '{NEW_LOGO_LABEL}'")
        return logo_frame, logo_label, self.logo_value

    def init_font_frame(self) -> tuple:
        """
        Initializes the row for font information.

        :return: a tuple containing the font container and its two children (see layout_option_row for order)
        """
        font_frame = ttk.Frame(self)
        font_label = ttk.Checkbutton(
            font_frame,
            text="Font:",
            variable=self.font_state,
            command=self.parent.update_view,
            width=COLUMN_WIDTH
        )
        font_list = sorted(FONTS.keys())
        self.font_value.set(font_list[0])
        font_menu = ttk.Combobox(
            font_frame,
            textvariable=self.font_value,
            values=font_list,
            state="readonly"
        )
        font_menu.bind("<<ComboboxSelected>>", self.parent.update_view)
        return font_frame, font_label, font_menu

    @staticmethod
    def _layout_option_row(frame, label, value) -> None:
        """
        Sets up consistent packing for a row of the option pane.

        :param frame: a row object
        :param label: a row label
        :param value: a row value
        :return: None
        """
        frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5, expand=tk.YES, fill=tk.X)
        label.pack(side=tk.LEFT)
        value.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)


class ImageTitlerMenuBar(tk.Menu):
    """
    The menu bar for interactions like loading files and logos.
    """

    def __init__(self, parent: ImageTitlerMain):
        super().__init__(parent)
        self.parent = parent
        self.image_path = None
        self.logo_path = None
        self.output_path = None
        self.current_edit = None
        self.file_menu = None
        self.init_menu()

    def init_menu(self) -> None:
        """
        Sets up the menu items.

        :return: None
        """
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)

        self.file_menu = tk.Menu(menu, tearoff=0, postcommand=self.save_as_enabled)
        self.file_menu.add_command(label=NEW_IMAGE_LABEL, command=self.new_image)
        self.file_menu.add_command(label=NEW_LOGO_LABEL, command=self.new_logo)
        self.file_menu.add_command(label=SAVE_AS_LABEL, command=self.save_as)
        menu.add_cascade(label=FILE_TAB_LABEL, menu=self.file_menu)

    def new_image(self) -> None:
        """
        Specifies behavior for when a user selects the "New Image" option.

        :return: None
        """
        self.image_path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        self.parent.update_view()

    def new_logo(self) -> None:
        """
        Specifies the behavior when a user selects the "New Logo" option.

        :return: None
        """
        self.logo_path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        self.parent.update_view()

    def save_as(self) -> None:
        """
        Specifies the behavior when a user selects the "Save As" option.

        :return: None
        """
        self.output_path = filedialog.askdirectory()
        self.parent.save_as()

    def save_as_enabled(self) -> None:
        """
        Enables/disables the "Save As" option.

        :return: None
        """
        if self.current_edit:
            self.file_menu.entryconfig(2, state=tk.NORMAL)  # TODO: make this not hardcoded
        else:
            self.file_menu.entryconfig(2, state=tk.DISABLED)


def main():
    """
    The GUI main function.

    :return: None
    """
    root = ImageTitlerMain()
    version = pkg_resources.require("image-titler")[0].version
    root.title(f"The Renegade Coder Image Titler {version}")
    root.iconphoto(False, tk.PhotoImage(file=TRC_ICON))
    root.mainloop()


if __name__ == '__main__':
    main()
