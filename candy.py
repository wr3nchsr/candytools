#!/usr/bin/env python3

import sys
import platform

from lib.cli.common import parser
from lib.cli import prep
from lib.cli import unpack
from lib.cli import convert
from lib.cli import extract
from lib.cli import decompile
from lib.cli import checksum
from lib.cli import version


commands = {
    "prep": prep.main,
    "unpack": unpack.main,
    "convert": convert.main,
    "extract": extract.main,
    "decompile": decompile.main,
    "checksum": checksum.main,
    "version": version.main,
}


def main():
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit()
    args = parser.parse_args()
    commands[args.command](args)


if __name__ == "__main__":
    if platform.system().lower() != "linux":
        sys.stdout.write("Needs to be run on linux\n")
        sys.exit(1)
    elif sys.version_info < (3, 7):
        sys.stdout.write("Python 3.7 or higher is required\n")
        sys.exit(1)
    main()
