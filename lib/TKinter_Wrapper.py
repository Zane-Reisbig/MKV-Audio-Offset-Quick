from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename

from typing import Literal


class tk:
    root = None

    def __enter__(self):
        self.root = Tk()
        self.root.attributes("-alpha", 0.01)
        self.root.attributes("-topmost", True)
        self.root.tk.eval(f"tk::PlaceWindow {self.root._w} center")
        self.root.withdraw()
        return self.root

    def __exit__(self, *args, **kwargs):
        self.root.destroy()

    @staticmethod
    def new():
        return tk()


def dir_name_picker(which: Literal["FOLDER", "FILE"]):
    which = {"FOLDER": askdirectory, "FILE": askopenfilename}[which]

    ret: str = None
    with tk.new():
        ret = which()

    return ret.replace("/", "\\")


if __name__ == "__main__":
    print("axdcdd")
    print()

    print(dir_name_picker("FILE"))
    print(dir_name_picker("FOLDER"))
