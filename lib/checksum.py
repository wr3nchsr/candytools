import hashlib
import os

import lib.log as log


def _hashfile(f):
    h = hashlib.sha1()
    fd = open(f, "rb")
    while True:
        s = fd.read(4096)
        if not s:
            break
        h.update(s)
    fd.close()
    return h.hexdigest()


def gen_hashes(path):
    path = os.path.normpath(os.path.abspath(path))
    start = f"/{path.split(os.sep)[-1]}/"
    log.info(f"Computing checksums for: {start}")
    chk = {}
    fail = 0
    for subdir, _, files in os.walk(path):
        for f in files:
            fname = os.path.join(subdir, f)
            key = fname.replace("\\", "/")[fname.rfind(start):]
            try:
                chk[key] = _hashfile(fname)
                log.debug(f"{key}: {chk[key]}")
            except Exception:
                fail += 1
    log.success(f"Checksums computed for {len(chk)} files")
    log.failure(f"Failed to compute checksums for {fail} files")
    return chk


def save_hashes(hashes, output):
    fd = open(output, "w")
    for p in hashes:
        fd.write(f"{p},{hashes[p]}\n")
    fd.close()


def _load(fd):
    chk = {}
    for line in fd.readlines():
        line = line.split(",")
        chk[line[0]] = line[1].strip()
    fd.close()
    return chk


def _get_added_modified(old, new):
    add, mod = [], []
    for f in new:
        if f not in old:
            add.append(f)
        elif new[f] != old[f]:
            mod.append(f)
    return add, mod


def _get_deleted(old, new):
    out = []
    for f in old:
        if f not in new:
            out.append(f)
    return out


def gen_diff(old_fd, new_fd):
    log.info("Loading checksum files")
    old_chk = _load(old_fd)
    new_chk = _load(new_fd)

    log.info("Diffing in progress")
    added, modified = _get_added_modified(old_chk, new_chk)
    deleted = _get_deleted(old_chk, new_chk)

    log.success(
        f"Diffing results: {len(added)} added, "
        + f"{len(modified)} modified, {len(deleted)} deleted"
    )
    return _format_diff(added, modified, deleted)


def _format_diff(added, modified, deleted):
    out = ""
    sep = "=" * 60 + "\n"
    for a in added:
        out += f"[ADD] {a}\n"
    out += sep
    for m in modified:
        out += f"[MOD] {m}\n"
    out += sep
    for d in deleted:
        out += f"[DEL] {d}\n"
    return out
