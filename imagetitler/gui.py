"""
The GUI interface for the image-titler script.
"""

import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog
from typing import Optional, List

import pkg_resources
from PIL import ImageTk, Image
from matplotlib import font_manager

from imagetitler.constants import *
from imagetitler.draw import process_images
from imagetitler.parse import parse_input
from imagetitler.store import save_copies

FONTS = {
    f"{f.name} ({f.style}, {f.variant}, {f.weight}, {f.stretch})": f.fname
    for f in font_manager.fontManager.ttflist
}

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

    def __init__(self, options):
        super().__init__()
        self.options = options
        self.menu = ImageTitlerMenuBar(self, self.options)
        self.gui = ImageTitlerGUI(self, self.menu, self.options)
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
        save_copies(
            self.menu.current_edit,
            **self.options
        )


class ImageTitlerGUI(ttk.Frame):
    """
    The main content of the GUI. This contains the preview pane and the option pane.
    """

    def __init__(self, parent, menu, options, **kw):
        super().__init__(parent, **kw)
        self.menu = menu
        self.options = options
        self.logo_path = None
        self.option_pane = ImageTitlerOptionPane(self, self.options)
        self.preview = ImageTitlerPreviewPane(self,
                                              text=f"Select a file using '{FILE_TAB_LABEL}' > '{NEW_IMAGE_LABEL}'")
        self._set_layout()
        self.update_view()

    def update_view(self, *_) -> None:
        """
        Updates this frame visually by controlling what is happening in children components.

        :return: None
        """
        if self.options[KEY_PATH]:
            self._render_preview()
        self._render_logo()

    def _set_layout(self) -> None:
        """
        Sets the layout of the window. Specifically, this function places the option pane
        on the left and the preview pane on the right.

        :return: None
        """
        self.preview.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)
        self.option_pane.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)

    def _render_preview(self) -> None:
        """
        Renders a preview of the edited image in the child preview pane.

        :return: None
        """
        self.menu.current_edit = process_images(**self.options)
        maxsize = (1028, 1028)
        small_image = self.menu.current_edit[0].copy()
        small_image.thumbnail(maxsize, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(small_image)
        self.preview.config(image=image)
        self.preview.image = image

    def _render_logo(self) -> None:
        """
        Renders a preview of the logo in the options pane.

        :return: None
        """
        logo_path = self.options.get(KEY_LOGO_PATH)
        if logo_path and logo_path != self.logo_path:
            self.logo_path = logo_path
            maxsize = (50, 50)
            small_image = Image.open(logo_path)
            small_image.thumbnail(maxsize, Image.ANTIALIAS)
            image = ImageTk.PhotoImage(small_image)
            self.option_pane.logo_value.config(image=image)
            self.option_pane.logo_value.image = image
            self.option_pane.logo_value.logo_path = self.logo_path
            self.option_pane.logo_state.set(1)


class ImageTitlerPreviewPane(ttk.Label):
    """
    The preview pane is a simple label which contains a preview of the
    image currently being edited.
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)


class ImageTitlerMenuBar(tk.Menu):
    """
    The menu bar for interactions like loading files and logos.
    """

    def __init__(self, parent: ImageTitlerMain, options: dict):
        super().__init__(parent)
        self.parent: ImageTitlerMain = parent
        self.options: dict = options
        self.current_edit: Optional[List] = None
        self.file_menu: Optional[tk.Menu] = None
        self._init_menu()

    def _init_menu(self) -> None:
        """
        Sets up the menu items.

        :return: None
        """
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)

        self.file_menu = tk.Menu(menu, tearoff=0, postcommand=self._save_as_enabled)
        self.file_menu.add_command(label=NEW_IMAGE_LABEL, command=self._new_image)
        self.file_menu.add_command(label=NEW_LOGO_LABEL, command=self._new_logo)
        self.file_menu.add_command(label=SAVE_AS_LABEL, command=self._save_as)
        menu.add_cascade(label=FILE_TAB_LABEL, menu=self.file_menu)

    def _new_image(self) -> None:
        """
        Specifies behavior for when a user selects the "New Image" option.

        :return: None
        """
        self.options[KEY_PATH] = filedialog.askopenfilename(filetypes=FILE_TYPES)
        self.parent.update_view()

    def _new_logo(self) -> None:
        """
        Specifies the behavior when a user selects the "New Logo" option.

        :return: None
        """
        self.options["logo_path"] = filedialog.askopenfilename(filetypes=FILE_TYPES)
        self.parent.update_view()

    def _save_as(self) -> None:
        """
        Specifies the behavior when a user selects the "Save As" option.

        :return: None
        """
        self.options[KEY_OUTPUT_PATH] = filedialog.askdirectory()
        self.parent.save_as()

    def _save_as_enabled(self) -> None:
        """
        Enables/disables the "Save As" option.

        :return: None
        """
        if self.current_edit:
            self.file_menu.entryconfig(2, state=tk.NORMAL)  # TODO: make this not hardcoded
        else:
            self.file_menu.entryconfig(2, state=tk.DISABLED)


class ImageTitlerOptionPane(ttk.Frame):
    """
    The option pane contains a set of options that can be controlled when editing the image.
    Changes are reflected in the preview pane.
    """

    def __init__(self, parent: ImageTitlerGUI, options: dict, **kw):
        super().__init__(parent, **kw)
        self.parent = parent
        self.options = options
        self.title_state: tk.IntVar = tk.IntVar()
        self.title_value: tk.StringVar = tk.StringVar()
        self.tier_state: tk.IntVar = tk.IntVar()
        self.tier_value: tk.StringVar = tk.StringVar()
        self.logo_path: Optional[str] = None
        self.logo_state: tk.IntVar = tk.IntVar()
        self.logo_value: Optional[ttk.Label] = None
        self.font_state: tk.IntVar = tk.IntVar()
        self.font_value: tk.StringVar = tk.StringVar()
        self.size_state: tk.IntVar = tk.IntVar()
        self.size_value: tk.StringVar = tk.StringVar()
        self.rows = list()
        self._init_vars()
        self._init_option_pane()

    def _init_vars(self) -> None:
        """
        Initializes the options pane based on any initial options.

        :return: None
        """
        # TODO: remove this method and add each section to each initialization method
        title = self.options.get(KEY_TITLE)
        ImageTitlerOptionPane._populate_option(title, self.title_value, self.title_state, "")
        tier = self.options.get(KEY_TIER)
        ImageTitlerOptionPane._populate_option(tier, self.tier_value, self.tier_state, list(TIER_MAP.keys())[0])
        font = self.options.get(KEY_FONT)
        self.font_value.set(sorted(list(FONTS.keys()))[0])
        if font != DEFAULT_FONT:
            font = next(k for k, v in FONTS.items() if Path(v).name == font)
            ImageTitlerOptionPane._populate_option(font, self.font_value, self.font_state)
        logo = self.options.get(KEY_LOGO_PATH)
        self.logo_state.set(1 if logo else 0)
        size = self.options.get(KEY_SIZE)
        ImageTitlerOptionPane._populate_option(size, self.size_value, self.size_state, sorted(SIZE_MAP.keys())[0])

    def _init_option_pane(self) -> None:
        """
        Initializes the option pane by generating rows of settings.

        :return: None
        """
        self.rows.append(self._init_title_frame())
        self.rows.append(self.init_font_frame())
        self.rows.append(self._init_size_frame())
        self.rows.append(self._init_tier_frame())
        self.rows.append(self.init_logo_frame())
        for row in self.rows:
            self._layout_option_row(*row[:3])

    def _init_title_frame(self) -> tuple:
        """
        Initializes the row for title information.

        :return: a tuple containing the title container and its two children (see layout_option_row for order)
        """
        title_frame = ttk.Frame(self)
        title_label = ttk.Checkbutton(
            title_frame,
            text=TITLE_OPTION_LABEL,
            variable=self.title_state,
            command=self._update_title,
            width=COLUMN_WIDTH
        )
        title_label.variable = self.title_state
        self.title_value.trace(tk.W, self._update_title)
        title_entry = tk.Entry(title_frame, textvariable=self.title_value)
        return title_frame, title_label, title_entry, "title"

    def _update_title(self, *_) -> None:
        """
        A helper method which serves as the update title functionality.
        This should be triggered when the title is changed.

        :return: None
        """
        if self.title_state.get():
            self.options[KEY_TITLE] = self.title_value.get()
        else:
            self.options[KEY_TITLE] = None
        self.parent.update_view()

    def _init_tier_frame(self) -> tuple:
        """
        Initializes the row for tier information.

        :return: a tuple containing the tier container and its two children (see layout_option_row for order)
        """
        tier_frame = ttk.Frame(self)
        tier_label = ttk.Checkbutton(
            tier_frame,
            text=TIER_OPTION_LABEL,
            variable=self.tier_state,
            command=self._update_tier,
            width=COLUMN_WIDTH
        )
        tier_label.variable = self.tier_state
        tier_option_menu = ttk.Combobox(
            tier_frame,
            textvariable=self.tier_value,
            values=list(TIER_MAP.keys()),
            state="readonly"
        )
        tier_option_menu.bind("<<ComboboxSelected>>", self._update_tier)
        return tier_frame, tier_label, tier_option_menu, KEY_TIER

    def _update_tier(self, *_) -> None:
        """
        A helper method which serves as the update tier functionality.
        This should be triggered when the tier is changed.

        :return: None
        """
        if self.tier_state.get():
            self.options[KEY_TIER] = self.tier_value.get()
        else:
            self.options[KEY_TIER] = None
        self.parent.update_view()

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
            command=self._update_logo,
            width=COLUMN_WIDTH
        )
        logo_label.variable = self.logo_state
        self.logo_value = ttk.Label(logo_frame, text=f"Select a logo using '{FILE_TAB_LABEL}' > '{NEW_LOGO_LABEL}'")
        return logo_frame, logo_label, self.logo_value, KEY_LOGO_PATH

    def _update_logo(self) -> None:
        """
        Renders a preview of the logo in the options pane.

        :return: None
        """
        if self.logo_state.get() and hasattr(self.logo_value, "logo_path"):
            self.options[KEY_LOGO_PATH] = self.logo_value.logo_path
        else:
            self.options[KEY_LOGO_PATH] = None
        self.parent.update_view()

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
            command=self._update_font,
            width=COLUMN_WIDTH
        )
        font_label.variable = self.font_state
        font_list = sorted(FONTS.keys())
        font_menu = ttk.Combobox(
            font_frame,
            textvariable=self.font_value,
            values=font_list,
            state="readonly",
            width=40
        )
        font_menu.bind("<<ComboboxSelected>>", self._update_font)
        return font_frame, font_label, font_menu, KEY_FONT

    def _update_font(self, *_) -> None:
        """
        A helper method which serves as the update font functionality.
        This should be triggered when the font is changed.

        :return: None
        """
        if self.font_state.get():
            self.options[KEY_FONT] = FONTS.get(self.font_value.get())
        else:
            self.options[KEY_FONT] = None
        self.parent.update_view()

    def _init_size_frame(self) -> tuple:
        """
        Initializes the row for size information.

        :return: a tuple containing the size container and its two children (see layout_option_row for order)
        """
        size_frame = ttk.Frame(self)
        size_label = ttk.Checkbutton(
            size_frame,
            text="Size:",
            variable=self.size_state,
            command=self._update_size,
            width=COLUMN_WIDTH
        )
        size_label.variable = self.size_state
        size_menu = ttk.Combobox(
            size_frame,
            textvariable=self.size_value,
            values=sorted(SIZE_MAP.keys()),
            state="readonly"
        )
        size_menu.bind("<<ComboboxSelected>>", self._update_size)
        return size_frame, size_label, size_menu, KEY_SIZE

    def _update_size(self, *_):
        """
        A helper method which serves as the update size functionality.
        This should be triggered when the size is changed.

        :return: None
        """
        if self.size_state.get():
            self.options[KEY_SIZE] = self.size_value.get()
        else:
            self.options[KEY_SIZE] = None
        self.parent.update_view()

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

    @staticmethod
    def _populate_option(option: str, value: tk.StringVar, state: tk.IntVar, default_option: str = None):
        if option:
            value.set(option)
            state.set(1)
        else:
            value.set(default_option)
            state.set(0)


def main():
    """
    The GUI main function.

    :return: None
    """
    options: dict = vars(parse_input())
    root = ImageTitlerMain(options)
    version = pkg_resources.require("image-titler")[0].version
    root.title(f"The Renegade Coder Image Titler {version}")
    root.iconphoto(False, tk.PhotoImage(file=TRC_ICON))
    root.mainloop()


if __name__ == '__main__':
    main()
