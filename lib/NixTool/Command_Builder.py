from subprocess import check_output
from os.path import dirname, basename, join

from .Command_Definitions import Nix_Command


class NixCommandBuilder:

    def __init__(self) -> None:
        self.command_accum = []

    def add(self, command: Nix_Command):
        self.command_accum.append(command)

    def as_command_string(self):
        return f'{" ".join(self.command_accum)}'


def create_full_command(cls: NixCommandBuilder, file_path: str, out_folder_path: str):
    # def create_full_command(cls: NixCommandBuilder, on: str, out: str):
    file_name = basename(file_path)

    out_folder = out_folder_path or dirname(file_path)
    out_folder = join(out_folder, file_name)
    return f'mkvmerge.exe -o "{out_folder}" {cls.as_command_string()} "{file_path}"'


def exec(
    cls: NixCommandBuilder,
    on: str,
    out_folder: str = None,
    nix_path=r"C:\Program Files\MKVToolNix",
):

    try:
        return check_output(
            create_full_command(cls, on, out_folder),
            shell=True,
            cwd=nix_path,
        )
    except Exception as e:
        print(e)
        return 1
