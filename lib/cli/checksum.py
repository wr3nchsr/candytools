import os
import argparse
import lib.log as log

from lib.checksum import gen_hashes, gen_diff
from lib.cli.common import commands_parser

parser = commands_parser.add_parser(
    "checksum",
    help="Compute and differentiate checksum files",
    description="Compute and differentiate checksum files",
)

subcommands = parser.add_subparsers(dest="subcommand")

gen = subcommands.add_parser(
    "comp",
    help="Compute files' checksum recursively for a directory",
    description="Compute files' checksum recursively for a directory",
)

gen.add_argument(
    "-d",
    "--dir",
    metavar="directory",
    help="Input directory",
    type=str,
    required=True
)

gen.add_argument(
    "-o",
    "--output",
    metavar="file",
    help="Output checksum file",
    type=argparse.FileType("w"),
    required=True,
)


diff = subcommands.add_parser(
    "diff",
    help="Differentiate between two checksum files",
    description="Differentiate between two checksum files",
)

diff.add_argument(
    "-old",
    metavar="file",
    help="Old version of checksum file",
    type=argparse.FileType("r"),
    required=True,
)

diff.add_argument(
    "-new",
    metavar="file",
    help="New version of checksum file",
    type=argparse.FileType("r"),
    required=True,
)

diff.add_argument(
    "-o",
    "--output",
    metavar="file",
    help="Output diff file",
    type=argparse.FileType("w"),
    required=True,
)


def main(args):
    if args.subcommand == "comp":
        path = args.dir
        if not os.path.isdir(path):
            log.critical(
                f'The provided path "{path}" is not a valid directory'
                )
            exit(1)

        hashes = gen_hashes(path)
        for p in hashes:
            args.output.write(f"{p},{hashes[p]}\n")
        args.output.close()
        log.success("Computed checksums saved")

    if args.subcommand == "diff":
        res = gen_diff(args.old, args.new)
        args.output.write(res)
        args.output.close()
        log.success("Diffing results saved")
