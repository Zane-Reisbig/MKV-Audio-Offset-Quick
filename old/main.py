import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from subprocess import check_output
from time import time

from json import load, dump


class Config:

    def __init__(self, **kwargs) -> None:
        self.keys = ["last_src" "last_dest" "use_last"]
        self.last_src: bool = None
        self.last_dest: bool = None
        self.use_last: str = None

        [setattr(self, key, kwargs[key]) for key in kwargs.keys()]

    def serial(self):
        serial = dict()
        [serial.update({key: getattr(self, key)} for key in self.keys)]

        return serial


def getConfig():
    ret = None

    with open("./config.json") as f:
        ret = load(f)

    return Config(**ret)


def setConfig(config: Config):
    with open("./config.json", "w") as f:
        dump(config.serial(), f)


def audioOffset(amountms, onFileFullPath, outFileNoBaseName=None):
    outFile = None

    if not outFileNoBaseName:
        outFile = os.path.dirname(onFileFullPath)
    else:
        fileName = os.path.basename(onFileFullPath)
        outFile = os.path.join(outFileNoBaseName, fileName)

    assert outFile != None, "No outfile specified"

    check_output(
        " ".join(
            [
                "mkvmerge.exe",
                f'-o "{outFile}"',
                f"--sync 2:{amountms}",
                f'"{onFileFullPath}"',
                "--track-order 0:0,0:2,0:1",
            ]
        ),
        shell=True,
        cwd=MKV_TOOLS_NIX_PATH,
    )


def setDefaultTrack(trackID, onFileFullPath, outFileNoBaseName=None):
    outFile = None

    if not outFileNoBaseName:
        outFile = os.path.dirname(onFileFullPath)
    else:
        fileName = os.path.basename(onFileFullPath)
        outFile = os.path.join(outFileNoBaseName, fileName)

    assert outFile != None, "No outfile specified"

    check_output(
        " ".join(
            [
                "mkvmerge.exe",
                f'-o "{outFile}"',
                f"--track-order 0:0,0:{trackID}",
                f'"{onFileFullPath}"',
            ]
        ),
        shell=True,
        cwd=MKV_TOOLS_NIX_PATH,
    )


def tkBrowser(which):
    root = Tk()
    root.attributes("-alpha", 0.01)
    root.attributes("-topmost", True)
    root.tk.eval(f"tk::PlaceWindow {root._w} center")
    root.withdraw()
    filename = which()
    root.destroy()

    return filename


MKV_TOOLS_NIX_PATH = r"C:\\Program Files\\MKVToolNix"

while True:
    con = getConfig()

    if not con.use_last:
        fileName = tkBrowser(askopenfilename).replace("/", "\\")
        outFolder = tkBrowser(askdirectory).replace("/", "\\")

        con.last_src = fileName
        con.last_dest = outFolder
        con.use_last = True

        setConfig(con)
    else:
        fileName = tkBrowser(
            lambda: askopenfilename(initialdir=os.path.dirname(con.last_src))
        ).replace("/", "\\")
        outFolder = con.last_dest

    while True:
        offset = input("Offset in ms (int)\n> ")
        if offset == "new":
            break
        elif offset == "exit":
            os._exit(0)

        offset = 0 if offset == "" else int(offset)

        _time = time()
        audioOffset(offset, fileName, outFolder)

        print(f"Remuxed in {time() - _time}")
