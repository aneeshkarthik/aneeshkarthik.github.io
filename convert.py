#!/usr/bin/env python3
"""
Convert HEIC/HEIF photos (the iPhone default) to JPEG so browsers can show them.

    ./convert             # convert everything under photos/
    ./convert --dry-run   # list what would be converted, change nothing

Originals are NOT deleted. Each photo.heic becomes photo.jpg next to it, and
the .heic is moved into photos/_heic-originals/ so ./update stops warning about
it. Delete that folder once you're happy with the results.

Uses `sips`, which ships with macOS — nothing to install.
"""

import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(ROOT, "photos")
BACKUP_DIR = os.path.join(PHOTOS_DIR, "_heic-originals")

SRC_EXTS = {".heic", ".heif"}
MAX_EDGE = 1800   # matches optimize.py, so converted files are already web-sized
QUALITY = 72


def find_sources():
    found = []
    for folder in sorted(os.listdir(PHOTOS_DIR)):
        fdir = os.path.join(PHOTOS_DIR, folder)
        if not os.path.isdir(fdir) or folder.startswith(".") or folder == "_heic-originals":
            continue
        for name in sorted(os.listdir(fdir)):
            if name.startswith("."):
                continue
            if os.path.splitext(name)[1].lower() in SRC_EXTS:
                found.append((folder, name))
    return found


def main():
    dry = "--dry-run" in sys.argv

    if not os.path.isdir(PHOTOS_DIR):
        sys.exit("No photos/ directory found.")
    if subprocess.run(["which", "sips"], capture_output=True).returncode != 0:
        sys.exit("`sips` not found. This script only runs on macOS.")

    items = find_sources()
    if not items:
        print("No HEIC/HEIF files found. Nothing to do.")
        return

    print("Found {} HEIC/HEIF file(s):\n".format(len(items)))
    for folder, name in items[:20]:
        print("  {}/{}".format(folder, name))
    if len(items) > 20:
        print("  ... and {} more".format(len(items) - 20))

    if dry:
        print("\n(dry run — nothing changed)")
        return

    print("\nEach becomes a .jpg at max {}px, quality {}.".format(MAX_EDGE, QUALITY))
    print("Originals move to photos/_heic-originals/ — nothing is deleted.")

    converted = failed = 0

    for folder, name in items:
        src = os.path.join(PHOTOS_DIR, folder, name)
        stem = os.path.splitext(name)[0]
        dst = os.path.join(PHOTOS_DIR, folder, stem + ".jpg")

        # Don't clobber an existing JPEG with the same name.
        n = 2
        while os.path.exists(dst):
            dst = os.path.join(PHOTOS_DIR, folder, "{} ({}).jpg".format(stem, n))
            n += 1

        result = subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(QUALITY),
             "-Z", str(MAX_EDGE), src, "--out", dst],
            capture_output=True,
        )

        if result.returncode == 0 and os.path.exists(dst):
            backup_folder = os.path.join(BACKUP_DIR, folder)
            os.makedirs(backup_folder, exist_ok=True)
            shutil.move(src, os.path.join(backup_folder, name))
            converted += 1
            print("  ok   {}/{}".format(folder, stem + ".jpg"))
        else:
            failed += 1
            print("  FAIL {}/{}".format(folder, name))

    print("\nConverted {}{}.".format(
        converted, ", {} failed".format(failed) if failed else ""))
    print("Originals are in photos/_heic-originals/ — delete it when you're happy.")
    print("Now run ./update")


if __name__ == "__main__":
    main()
