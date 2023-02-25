import os
import lib.log as log

from lib.extract import extract
from lib.cli.common import commands_parser

parser = commands_parser.add_parser(
    "extract",
    help="Extract system images",
    description="Extract system images",
)

parser.add_argument(
    "-i",
    "--img",
    metavar="image",
    help="Ext4 image to extract",
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
    extract(img_path, output)
