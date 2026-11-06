"""Command registry.

Each command module exposes two functions:

    add_parser(subparsers)   # register the sub-command and its arguments
    handle(args, store)      # run it; return a process exit code (int)

To add a new command, create a module here and list it in ``COMMANDS``.
Follow the shape of the existing commands (add, list, delete).
"""

from . import add, delete, export, list_cmd

COMMANDS = [add, list_cmd, delete, export]
