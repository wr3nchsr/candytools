from lib.version import __version__
import lib.log as log
from lib.cli.common import commands_parser, config

parser = commands_parser.add_parser(
    "version",
    help="candytools version",
    description="candytools version",
)


def main(args):
    log.info(f"candytools v{__version__}")
