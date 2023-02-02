#!/usr/bin/env python
import os
import sys

from dronefly.core import Commands, Format
from dronefly.core.models.user import User
from dronefly.core.commands import Context
from rich.console import Console

console = Console()

user = User()
user.id = 1
user.inat_user_id = os.environ.get("INAT_USER_ID")
user.inat_place_id = os.environ.get("INAT_PLACE_ID") or 97394  # North America
ctx = Context()
ctx.author = user

commands = Commands(format=Format.rich)


def do_command(command_str: str, ctx: Context, *args):
    command = getattr(commands, command_str, None)
    if not callable(command):
        raise (NameError(command_str))
    if not args:
        raise (ValueError("No arguments"))
    console.print(command(ctx, *args))


if len(sys.argv) == 1:
    try:
        while True:
            _line = console.input("[bold gold1](=)[/bold gold1] ").rstrip()
            if not _line:
                continue
            if _line.lower() in ("q", "quit"):
                break
            args = _line.split(" ")
            command = args[0]
            args.remove(command)
            try:
                do_command(command, ctx, *args)
            except NameError:
                console.print(f"No such command: {command}")
            except ValueError as err:
                console.print(err)
    except (KeyboardInterrupt, EOFError):
        console.print()
else:
    command = sys.argv[1]
    args = sys.argv[2:]
    try:
        do_command(command, ctx, *args)
    except ValueError as err:
        console.print(err)
