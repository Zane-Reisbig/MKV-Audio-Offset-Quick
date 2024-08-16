from lib.NixTool.Command_Definitions import Audio_Offset, Track_Order
from lib.NixTool.Command_Builder import NixCommandBuilder, exec, create_full_command
from lib.TKinter_Wrapper import dir_name_picker

from pyperclip import copy

command = NixCommandBuilder()

command.add(Audio_Offset.create(1000))
command.add(Track_Order.create(2))

# cmd = create_full_command(command, dir_name_picker("FILE"), dir_name_picker("FOLDER"))
# print(cmd)
# copy(cmd)

exec(command, dir_name_picker("FILE"), dir_name_picker("FOLDER"))
