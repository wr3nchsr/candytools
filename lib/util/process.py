import subprocess

import lib.log as log


def run(cmd, stdin=None, **kwargs):
    log.debug(f"Running {subprocess.list2cmdline(cmd)}")
    try:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            **kwargs,
        )
        stdout, stderr = p.communicate(stdin)
        exitcode = p.wait()
    except Exception as e:
        log.error(f"An exception occurred: {e}")
        return False, ""

    if (exitcode, stderr) != (0, ""):
        if exitcode != 0:
            log.error(
                f"An error occurred while running '{subprocess.list2cmdline(cmd)}'\n"
                + f"\texit code: {exitcode}\n"
                + f"\tstderr: {stderr[:-1]}"
            )
            return False, stdout
        elif len(stderr) > 0:
            log.debug("stderr")
    return True, stdout
