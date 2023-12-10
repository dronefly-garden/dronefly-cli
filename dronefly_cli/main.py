#!/usr/bin/env python
import os
import sys
import readline

from dronefly.core import Commands, Format
from dronefly.core.models.user import User
from dronefly.core.commands import ArgumentError, CommandError, Context
from dronefly.core.constants import INAT_USER_DEFAULT_PARAMS
from rich.console import Console


console = Console()
commands = Commands(format=Format.rich)
histfile = os.path.expanduser("~/.dronefly_history")
histfile_size = 1000


def do_command(command_str: str, ctx: Context, *args):
    try:
        command = getattr(commands, command_str, None)
        if not callable(command):
            raise CommandError(f"No such command: {command_str}")
        # TODO: Use command signatures to provide argument validation and conversion.
        if (command_str not in ["life", "next", "prev", "page"]) and not args:
            raise ArgumentError("No arguments")
        if command_str in ["next", "prev"] and args:
            raise ArgumentError("No argument expected")
        if command_str in ["page"] and len(args) > 1:
            raise ArgumentError("Too many arguments")
        # Argument conversion, if necessary:
        if command_str in ["page", "sel"] and len(args):
            response = command(ctx, int(args[0]))
        else:
            response = command(ctx, *args)
        if isinstance(response, list):
            console.print(*response)
        else:
            console.print(response)
    except (ArgumentError, CommandError) as err:
        console.print(err)


def get_context():
    user_params = {"id": 1}
    for param in ("inat_user_id", *INAT_USER_DEFAULT_PARAMS):
        param_env = os.environ.get(param.upper())
        if param_env:
            user_params[param] = int(param_env) if param_env.isnumeric() else param_env
    user = User(**user_params)
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
                if not ctx.page_formatter:
                    continue
                _line = "next"
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
        ctx.per_page = 20
        start_command_loop(ctx, histfile, histfile_size)
    else:
        ctx.per_page = 0
        command = sys.argv[1]
        args = sys.argv[2:]
        do_command(command, ctx, *args)


if __name__ == "__main__":
    main()
