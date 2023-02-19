import os
import shutil

import lib.log as log
from lib.util.process import run


def _unpack(config, img):
    success, output = run([config["unpack_64"], img], cwd=config["aik"])
    if len(output) > 0:
        log.debug(output.replace("\x1b[H\x1b[2J\x1b[3J", ""))
    return success


def _move_output(aik, img, outdir):
    output = os.path.join(outdir, img.split(".")[0])
    if not os.path.exists(output):
        os.mkdir(output)

    for i in ["ramdisk", "split_img"]:
        p = os.path.join(output, i)
        if os.path.exists(p):
            shutil.rmtree(p)

        shutil.move(os.path.join(aik, i), output)


def unpack(config, img_path, outdir):
    if not os.path.isdir(config["aik"]):
        log.critical(
            "AIK is not installed. Please install it or change its location in default.conf"
        )
        return

    _, img = os.path.split(img_path)
    log.info(f"Unpacking {img}")

    shutil.copy(img_path, config["aik"])
    if not _unpack(config, img):
        log.failure(f"Failed to unpack {img}")

    else:
        log.success(f"{img} unpacked successfully")
        log.info(f"Moving unpacked results to {outdir}")
        _move_output(config["aik"], img, outdir)

    log.info("Cleanup after kernel image unpacking")
    os.remove(os.path.join(config["aik"], img))
