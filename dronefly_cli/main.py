#!/usr/bin/env python
import asyncio
import os
import sys
import readline
from inspect import getmembers, isroutine

from dronefly.core import Commands, Format
from dronefly.core.models import Config, User
from dronefly.core.commands import ArgumentError, CommandError, Context
from dronefly.core.constants import INAT_USER_DEFAULT_PARAMS
from rich.console import Console
from rich.markdown import Markdown


console = Console()
histfile = os.path.expanduser("~/.dronefly_history")
histfile_size = 1000


async def help(ctx, *args):
    """Show help
    Usage:
                 help             Show help index
                 help <command>   Show help for command"""  # noqa: E501

    def format_help_index_command(command, command_width):
        command_help = f"{command[0].replace('_',' ').ljust(command_width)}"
        if command[1].__doc__:
            command_help += "    " + command[1].__doc__.splitlines()[0]
        return command_help

    if len(args) == 0:
        commands = [
            *(
                member
                for member in getmembers(Commands, predicate=isroutine)
                if member[0][0] != "_"
            ),
            ("help", help),
        ]
        commands.sort(key=lambda x: x[0])
        longest = max(len(member[0]) for member in commands)
        response = "\n".join(
            format_help_index_command(command, longest) for command in commands
        )
        return response
    command_name = "_".join(args)
    if command_name[0] != "_":
        if command_name == "help":
            command = help
        else:
            command = getattr(Commands, command_name, None)
        if callable(command):
            return f"Command:     {command_name.replace('_', ' ')}\nDescription: {command.__doc__}"
    return f"No help for: {' '.join(args)}"


async def do_command(commands, command_str: str, ctx: Context, *args):
    try:
        command = None
        _args = [*args]
        if len(_args) > 0:
            subcommand = "_".join([command_str, _args[0]])
            command = getattr(commands, subcommand, None)
            if command:
                _args.pop(0)
        if command_str == "help":
            command = help
        if not command:
            command = getattr(commands, command_str, None)
        if not callable(command):
            raise CommandError(f"No such command: {command_str}")
        # TODO: Use command signatures to provide argument validation and conversion.
        if (command_str not in ["life", "next", "prev", "page", "help"]) and not _args:
            raise ArgumentError("No arguments")
        if command_str in ["next", "prev"] and _args:
            raise ArgumentError("No argument expected")
        if command_str in ["page"] and len(_args) > 1:
            raise ArgumentError("Too many arguments")
        # Argument conversion, if necessary:
        if command_str in ["page", "sel"] and len(_args):
            response = await command(ctx, int(_args[0]))
        else:
            response = await command(ctx, *_args)
        if isinstance(response, list):
            console.print(*response)
        else:
            console.print(response)
    except (ArgumentError, CommandError, LookupError) as err:
        if commands.format == Format.rich:
            console.print(Markdown(str(err)))
        else:
            console.print(err)


def get_context():
    default_user_id = 1
    config = Config()
    user_config = config.user(default_user_id)
    user_params = {"id": default_user_id}
    for param in ("inat_user_id", *INAT_USER_DEFAULT_PARAMS):
        param_value = None
        if user_config:
            param_value = user_config.get(param)
        if not param_value:
            param_value = os.environ.get(param.upper())
            if param_value and param_value.isnumeric():
                param_value = int(param_value)
        if param_value:
            user_params[param] = param_value
    user = User(**user_params)
    ctx = Context(author=user)
    return ctx


def read_history(histfile):
    if os.path.exists(histfile):
        readline.read_history_file(histfile)


def write_history(histfile, histfile_size):
    readline.set_history_length(histfile_size)
    readline.write_history_file(histfile)


async def start_command_loop(commands, ctx, histfile, histfile_size):
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
            await do_command(commands, command, ctx, *args)
    except (KeyboardInterrupt, EOFError):
        write_history(histfile, histfile_size)
        console.print()


async def start():
    ctx = get_context()

    loop = asyncio.get_running_loop()
    commands = Commands(loop=loop, format=Format.rich)
    if len(sys.argv) == 1:
        ctx.per_page = 20
        await start_command_loop(commands, ctx, histfile, histfile_size)
    else:
        ctx.per_page = 0
        command = sys.argv[1]
        args = sys.argv[2:]
        await do_command(commands, command, ctx, *args)


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
