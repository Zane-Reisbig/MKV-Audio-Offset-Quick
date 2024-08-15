import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from subprocess import check_output
from time import time


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


fileName = tkBrowser(askopenfilename).replace("/", "\\")
outFolder = tkBrowser(askdirectory).replace("/", "\\")


MKV_TOOLS_NIX_PATH = r"C:\\Program Files\\MKVToolNix"

while True:
    offset = int(input("Offset in ms (int)\n> "))

    _time = time()
    audioOffset(offset, fileName, outFolder)

    print(f"Remuxed in {time() - _time}")
