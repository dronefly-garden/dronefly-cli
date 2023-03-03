#!/usr/bin/env python
import os
import sys
import readline

from dronefly.core import Commands, Format
from dronefly.core.models.user import User
from dronefly.core.commands import Context
from rich.console import Console


console = Console()
commands = Commands(format=Format.rich)
histfile = os.path.expanduser("~/.dronefly_history")
histfile_size = 1000


def do_command(command_str: str, ctx: Context, *args):
    try:
        command = getattr(commands, command_str, None)
        if not callable(command):
            raise (NameError(command_str))
        if not args:
            raise (ValueError("No arguments"))
        console.print(command(ctx, *args))
    except NameError:
        console.print(f"No such command: {command_str}")
    except ValueError as err:
        console.print(err)


def get_context():
    user = User(
        id=1,
        inat_user_id=os.environ.get("INAT_USER_ID"),
        inat_place_id=os.environ.get("INAT_PLACE_ID") or 97394,  # North America
    )
    ctx = Context(author=user)
    return ctx


def read_history(histfile):
    if os.path.exists(histfile):
        readline.read_history_file(histfile)


def write_history(histfile, histfile_size):
    readline.set_history_length(histfile_size)
    readline.write_history_file(histfile)


def start_command_loop(ctx, histfile, histfile_size):
    try:
        read_history(histfile)

        while True:
            console.print("[bold gold1](=)[/bold gold1]", end="")
            _line = console.input(" ").rstrip()
            if not _line:
                continue
            if _line.lower() in ("q", "quit"):
                write_history(histfile, histfile_size)
                break
            args = _line.split(" ")
            command = args[0]
            args.remove(command)
            do_command(command, ctx, *args)
    except (KeyboardInterrupt, EOFError):
        write_history(histfile, histfile_size)
        console.print()


def main():
    ctx = get_context()

    if len(sys.argv) == 1:
        start_command_loop(ctx, histfile, histfile_size)
    else:
        command = sys.argv[1]
        args = sys.argv[2:]
        do_command(command, ctx, *args)


if __name__ == "__main__":
    main()
