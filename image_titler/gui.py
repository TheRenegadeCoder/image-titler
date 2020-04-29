import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk

from image_titler.utilities import process_image, convert_file_name_to_title, save_copy


class ImageTitlerMain(tk.Tk):
    def __init__(self):
        super().__init__()
        self.menu = ImageTitlerMenuBar(self)
        self.gui = ImageTitlerGUI(self)
        #self.geometry("1920x960+0+0")


class ImageTitlerGUI(tk.Frame):

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.preview = ImageTitlerPreviewPane(self)
        self.option_pane = ImageTitlerOptionPane(self)
        self.set_layout()
        self.pack()

    def set_layout(self):
        self.option_pane.pack(side="left", fill="both", expand="yes")
        self.preview.pack(side="right", fill="both", expand="yes")


class ImageTitlerPreviewPane(tk.Label):

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)


class ImageTitlerOptionPane(tk.Frame):

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.init_option_pane()
        self.pack()

    def init_option_pane(self):
        label = tk.Label(self, text="Title")
        label.pack()


class ImageTitlerMenuBar(tk.Menu):

    def __init__(self, parent: ImageTitlerMain):
        super().__init__(parent)
        self.parent = parent
        self.image_path = None
        self.current_edit = None
        self.file_menu = None
        self.init_menu()

    def init_menu(self):
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)

        self.file_menu = tk.Menu(menu, tearoff=0, postcommand=self.save_as_enabled)
        self.file_menu.add_command(label="New Image", command=self.new_image)
        self.file_menu.add_command(label="Save As", command=self.save_as)

        menu.add_cascade(label="File", menu=self.file_menu)

    def new_image(self):
        self.image_path = tk.filedialog.askopenfilename()
        if self.image_path:
            title = convert_file_name_to_title(self.image_path)
            self.current_edit = process_image(self.image_path, title)
            image = ImageTk.PhotoImage(self.current_edit)
            self.parent.gui.preview.config(image=image)
            self.parent.gui.preview.image = image
            self.parent.gui.set_layout()

    def save_as(self):
        output_path = tk.filedialog.askdirectory()
        save_copy(self.image_path, self.current_edit, output_path=output_path)

    def save_as_enabled(self):
        if self.current_edit:
            self.file_menu.entryconfig(1, state=tk.NORMAL)
        else:
            self.file_menu.entryconfig(1, state=tk.DISABLED)


def main():
    ImageTitlerMain().mainloop()


if __name__ == '__main__':
    main()
