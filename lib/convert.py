import os

import lib.log as log
from lib.util.process import run


def _sparse_to_ext4(simg2img, simg, img):
    success, output = run([simg2img, simg, img])
    if len(output) > 0:
        log.debug(output)
    return success


def _sdat_to_ext4(dat, transfer, output):
    dat_fd = open(dat, "rb")
    transfer_fd = open(transfer, "r")
    block_size = 4096
    commands = _transfer_list_to_commands(transfer_fd)
    if commands == -1:
        return commands

    with open(output, "wb") as output_img:
        all_block_sets = [i for command in commands for i in command[1]]
        max_file_size = max(pair[1] for pair in all_block_sets) * block_size

        for command in commands:
            if command[0] == "new":
                for block in command[1]:
                    begin = block[0]
                    end = block[1]
                    block_count = end - begin
                    output_img.seek(begin * block_size)
                    log.debug(
                        f"Copying {block_count} blocks to position {begin}"
                        )
                    while block_count > 0:
                        output_img.write(dat_fd.read(block_size))
                        block_count -= 1
            else:
                log.debug(f"Skipping command {command[0]}")

        if output_img.tell() < max_file_size:
            output_img.truncate(max_file_size)

    return 0


def _transfer_list_to_commands(fd):
    version = int(fd.readline())
    fd.readline()

    if version >= 2:
        fd.readline()
        fd.readline()

    commands = []
    for line in fd:
        line = line.split(" ")
        cmd = line[0]

        if cmd in ["erase", "new", "zero"]:
            rng = _range_set(line[1])
            if rng == -1:
                return -1
            commands.append([cmd, rng])
        else:
            if not cmd[0].isdigit():
                log.error(f'Command "{cmd}" is not valid')
                return -1

    return commands


def _range_set(src):
    src_set = src.split(",")
    num_set = [int(item) for item in src_set]

    if len(num_set) != num_set[0] + 1:
        log.error("Error on parsing following data to range_set:")
        log.error(f"{src[:-1]}")
        return -1
    return tuple(
        [(num_set[i], num_set[i + 1]) for i in range(1, len(num_set), 2)]
        )


def _detect(path):
    entries = os.listdir(path)

    if "system.img" in entries:
        img = os.path.join(path, "system.img")
        if b"\x3a\xff\x26\xed" == open(img, "rb").read(4):
            return "sparse"

    if "system.transfer.list" in entries and "system.new.dat" in entries:
        return "sdat"

    return "unknown"


def convert(config, path, output):
    img_type = _detect(path)
    log.info(f"Detected image type: {img_type}")

    if img_type == "sparse":
        log.info("Converting sparse image to ext4")
        simg = os.path.join(path, "system.img")
        if _sparse_to_ext4(config["simg2img"], simg, output):
            log.success("Sparse image converted to ext4")
        else:
            log.error("Failed to convert sparse image")

    elif img_type == "sdat":
        log.info("Converting sdat image to ext4")
        dat = os.path.join(path, "system.new.dat")
        transfer = os.path.join(path, "system.transfer.list")
        if _sdat_to_ext4(dat, transfer, output) == 0:
            log.success("Sdat image converted to ext4")
        else:
            log.error("Failed to convert sdat image")

    else:
        log.critical("Image type not implemented")
