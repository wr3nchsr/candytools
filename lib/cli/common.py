import os
import argparse
import configparser

import lib.log as log

base_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)

config = configparser.ConfigParser()
config.read(os.path.join(base_path, "default.conf"))

log.set_level(config.getint("log", "level"))

log.debug(f"Candy base path: {base_path}")
log.debug("Loading config variables")
for k in ["unpack", "convert", "decompile"]:
    for i in config[k]:
        config[k][i] = os.path.realpath(os.path.join(base_path, config[k][i]))
        log.debug(f"config[{k}][{i}]: {config[k][i]}")

parser = argparse.ArgumentParser(description="Candy CLI Tools", prog="candy")
commands_parser = parser.add_subparsers(dest="command")
