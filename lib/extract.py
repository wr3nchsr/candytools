import os
import shutil

import lib.log as log
from lib.util.process import run


def extract(ext4, output):
    log.info(f"Extracting {ext4}")
    path = os.path.join(output, "system")
    if os.path.exists(path):
        shutil.rmtree(path)
    success, output = run(["7z", "x", f"-o{path}", ext4])
    if len(output) > 0:
        log.debug(output)
    if success:
        log.success("Ext4 image extracted successfully")
    else:
        log.error("Error extracting ext4")
