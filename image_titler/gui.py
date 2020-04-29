import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk

from image_titler.utilities import process_image, convert_file_name_to_title


class ImageTitlerGUI(tk.Tk):

    def __init__(self, **kw):
        super().__init__()
        self.menu = ImageTitlerMenuBar(self)


class ImageTitlerMenuBar(tk.Menu):

    def __init__(self, parent: ImageTitlerGUI):
        super().__init__(parent)
        self.parent = parent
        self.init_menu()

    def init_menu(self):
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New Image", command=self.new_image)

        menu.add_cascade(label="File", menu=file_menu)

    def new_image(self):
        image_path = askopenfilename()
        title = convert_file_name_to_title(image_path)
        image = ImageTk.PhotoImage(process_image(image_path, title))
        panel = tk.Label(self.parent, image=image)
        panel.pack(side="bottom", fill="both", expand="yes")


if __name__ == '__main__':
    ImageTitlerGUI().mainloop()
