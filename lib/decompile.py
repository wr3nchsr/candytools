import os
import shutil
import lief
from tqdm import tqdm

import lib.log as log
from lib.util.process import run


def _crawl_path(path):
    apk, jar, odex = {}, {}, {}
    for subdir, _, files in os.walk(path):
        for f in files:
            fname = os.path.join(subdir, f)
            if fname.endswith(".apk"):
                apk[f[: f.rfind(".apk")]] = fname
            elif fname.endswith(".jar"):
                jar[f[: f.rfind(".jar")]] = fname
            elif fname.endswith(".odex"):
                odex[f[: f.rfind(".odex")]] = fname
            elif fname.endswith(".oat"):
                odex[f[: f.rfind(".oat")].replace("boot-", "")] = fname
    return apk, jar, odex


def _deodex(odex, output):
    log.debug(f"Deodexing {odex}")
    odex = lief.parse(odex)
    for i in range(len(odex.dex_files)):
        c = os.path.join(output, f"classes{i if i > 0 else ''}.dex")
        odex.dex_files[i].save(c)
    log.debug(f"Found {len(odex.dex_files)} dex files")
    return len(odex.dex_files)


def _decompile(jadx, file, output):
    path = os.path.join(output, "decompiled")
    success, output = run([jadx, "-d", path, file])
    if len(output) > 0:
        log.debug(output)
    return success


def _process_apps(jadx, apps, odex, output):
    for app in tqdm(apps, leave=False):
        log.debug(f"Decompiling {app}")
        path = os.path.join(output, app)
        os.mkdir(path)

        shutil.copy(apps[app], path)
        _decompile(jadx, apps[app], path)

        if app in odex:
            classes_len = _deodex(odex[app], path)
            for c in range(classes_len):
                f = os.path.join(path, f"classes{c if c > 0 else ''}.dex")
                _decompile(jadx, f, path)


def decompile(config, path, output):
    apps_path = os.path.join(output, "apps")
    if os.path.exists(apps_path):
        shutil.rmtree(apps_path)
    os.mkdir(apps_path)

    log.info("Collecing all APK, JAR, ODEX, OAT files")
    apk, jar, odex = _crawl_path(path)
    log.success(f"Found {len(apk)} APK, {len(jar)} JAR, {len(odex)} ODEX and OAT files")

    log.info(f"Decompiling {len(apk)} APKs")
    apk_path = os.path.join(apps_path, "apks")
    os.mkdir(apk_path)
    _process_apps(config["jadx"], apk, odex, apk_path)

    log.info(f"Decompiling {len(jar)} JARs")
    jar_path = os.path.join(apps_path, "jars")
    os.mkdir(jar_path)
    _process_apps(config["jadx"], jar, odex, jar_path)
