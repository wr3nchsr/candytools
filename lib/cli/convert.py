import os

import lib.log as log
from lib.convert import convert
from lib.cli.common import commands_parser, config

parser = commands_parser.add_parser(
    "convert",
    help="Convert system images",
    description="Convert system images",
)

parser.add_argument(
    "-i",
    "--indir",
    metavar="directory",
    help="Input directory containing the system image",
    type=str,
    required=True,
)

parser.add_argument(
    "-o",
    "--output",
    metavar="image",
    help="Output image path",
    type=str,
    required=True,
)


def main(args):
    indir = args.indir
    output = args.output
    if not os.path.isdir(indir):
        log.critical("Supplied input path is not a directory")
        exit(1)
    if os.path.exists(output):
        log.critical("Supplied output path already exists")
        exit(1)
    convert(config["convert"], indir, output)
