import os
import lib.log as log
from lib.unpack import unpack
from lib.cli.common import commands_parser, config

parser = commands_parser.add_parser(
    "unpack",
    help="Unpack kernel image",
    description="Unpack kernel image",
)

parser.add_argument(
    "-i",
    "--img",
    metavar="image",
    help="Kernel image to unpack",
    type=str,
    required=True,
)

parser.add_argument(
    "-o",
    "--output",
    metavar="directory",
    help="Output directory",
    type=str,
    required=True,
)


def main(args):
    img_path = args.img
    output = args.output
    if not os.path.isfile(img_path):
        log.critical("Supplied image path is not a file")
        exit(1)
    if not os.path.isdir(output):
        log.critical("Supplied output path is not a directory")
        exit(1)
    unpack(config["unpack"], img_path, output)
