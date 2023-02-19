from lib.unpack import *
from lib.extract import *
from lib.decompile import *
from lib.convert import *
from lib.checksum import *
from lib.cli.common import commands_parser, config

parser = commands_parser.add_parser(
    "prep",
    help="Prepare an OTA update for analysis",
    description="Prepare an OTA update for analysis",
)

parser.add_argument(
    "-i",
    "--indir",
    metavar="directory",
    help="Input directory (OTA update)",
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
    "-d",
    "--no-decompile",
    help="Don't decompile applicaitons from the resulting system",
    action="store_true",
)


def main(args):
    indir = args.indir
    outdir = args.outdir
    no_decompile = args.no_decompile

    if not os.path.isdir(indir):
        log.critical("Supplied input path is not a directory")
        exit(1)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    hashes = {}

    boot_img = os.path.join(indir, "boot.img")
    if os.path.exists(boot_img):
        unpack(config["unpack"], boot_img, outdir)

        boot_path = os.path.join(outdir, "boot")
        hashes.update(gen_hashes(boot_path))

    recovery_img = os.path.join(indir, "recovery.img")
    if os.path.exists(recovery_img):
        unpack(config["unpack"], recovery_img, outdir)

        recovery_path = os.path.join(outdir, "recovery")
        hashes.update(gen_hashes(recovery_path))

    system_img = os.path.join(outdir, "system.img")
    if os.path.exists(system_img):
        os.remove(system_img)
    convert(config["convert"], indir, system_img)

    if os.path.exists(system_img):
        system_path = os.path.join(outdir, "system")
        extract(system_img, outdir)
        hashes.update(gen_hashes(system_path))

    save_hashes(hashes, os.path.join(outdir, "checksum.txt"))

    if os.path.exists(system_path) and not no_decompile:
        decompile(config["decompile"], system_path, outdir)
