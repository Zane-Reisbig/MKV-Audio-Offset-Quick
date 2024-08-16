from typing import overload


class Nix_Command:
    def __new__(cls, *args, **kwargs):
        cls.__is_command__ = True
        return cls

    def create(*args):
        pass

    @staticmethod
    def __format_string_command__(command: str, args: tuple = ()):
        return str(f"--{command} {" ".join(args)}")

    @staticmethod
    def __format_char_command__(command: str, args: tuple = ()):
        return str(f"-{command} {" ".join(args)}")


class Audio_Offset(Nix_Command):
    @staticmethod
    @overload
    def create(delay_ms: int): ...

    @staticmethod
    @overload
    def create(track: int, delay_ms: int): ...

    @staticmethod
    def create(*args):
        if len(args) == 1:
            track = 1
            delay_ms = args[0]

        elif len(args) == 2:
            track = args[0]
            delay_ms = args[1]

        return Nix_Command.__format_string_command__("sync", (f"{track}:{delay_ms}",))


class Track_Order:
    @staticmethod
    @overload
    def create(order: list[int]): ...

    @staticmethod
    @overload
    def create(video_track: int, order: list[int]): ...

    @staticmethod
    def create(*args):

        def _create(video_track: int, order: list[int]):
            if type(order) != list:
                order = [
                    order,
                ]

            order = ",".join([str(f"{video_track}:{_o}") for _o in order])
            return Nix_Command.__format_string_command__(
                "track-order", (f"{video_track}:0,{order}",)
            )

        if len(args) == 1:
            return _create(0, args[0])

        return _create(args[0], args[1])


if __name__ == "__main__":
    print(Track_Order.create([2, 1, 3]))
    pass
