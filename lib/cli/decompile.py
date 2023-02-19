from lib.decompile import *
from lib.cli.common import commands_parser, config

parser = commands_parser.add_parser(
    "decompile",
    help="Decompile applications recursively",
    description="Decompile applications recursively",
)

parser.add_argument(
    "-i",
    "--indir",
    metavar="directory",
    help="Input directory (extracted system image)",
    type=str,
    required=True,
)

parser.add_argument(
    "-o",
    "--outdir",
    metavar="directory",
    help="Output directory",
    type=str,
    required=True,
)

parser.add_argument(
    "-a",
    "--android",
    metavar="version",
    help="Android version",
    type=float,
    required=True,
)


def main(args):
    indir = args.indir
    outdir = args.outdir
    android = args.android
    if not os.path.isdir(indir):
        log.critical("Supplied input path is not a directory")
        exit(1)
    if not os.path.isdir(outdir):
        log.critical("Supplied output path is not a directory")
        exit(1)
    if android >= 8:
        log.critical("VDEX is not yet implemented")
        exit(1)

    decompile(config["decompile"], indir, outdir)
