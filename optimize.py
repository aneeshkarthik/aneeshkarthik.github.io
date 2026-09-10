#!/usr/bin/env python3
"""
Shrink oversized photos so the site loads fast.

    ./optimize            # show what would change, then ask before doing it
    ./optimize --dry-run  # just show, never touch anything

Resizes any image whose long edge is over MAX_EDGE down to MAX_EDGE and
re-encodes JPEGs at QUALITY. Uses `sips`, which ships with macOS — no
installs needed.

THIS EDITS FILES IN PLACE. The images in photos/ should be copies; keep your
originals in Photos/iCloud/your camera roll.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(ROOT, "photos")

MAX_EDGE = 1800      # px on the long edge — plenty for full-screen viewing
QUALITY = 70         # JPEG quality, 0-100
SIZE_FLOOR = 300_000  # don't bother with files already under ~300 KB

EXTS = {".jpg", ".jpeg", ".png"}


def human(n):
    return "{:.1f} MB".format(n / 1e6) if n >= 1e6 else "{:.0f} KB".format(n / 1e3)


def png_has_alpha(path):
    """
    True if a PNG carries transparency. Colour type lives at byte 25 of the
    IHDR chunk: 4 and 6 have an alpha channel, 3 (palette) may have a tRNS
    chunk. Flattening any of those onto JPEG would fill the clear pixels
    black, so those keep their PNG format.
    """
    try:
        with open(path, "rb") as f:
            head = f.read(26)
            if len(head) < 26 or head[:8] != b"\x89PNG\r\n\x1a\n":
                return True  # unreadable: assume the worst, leave it alone
            colour_type = head[25]
            if colour_type in (4, 6):
                return True
            if colour_type == 3:
                return b"tRNS" in f.read(4096)
            return False
    except OSError:
        return True


def dimensions(path):
    try:
        out = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
            capture_output=True, text=True, check=True,
        ).stdout
        w = h = 0
        for line in out.splitlines():
            if "pixelWidth:" in line:
                w = int(line.split(":")[1])
            elif "pixelHeight:" in line:
                h = int(line.split(":")[1])
        return w, h
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return 0, 0


def find_candidates():
    out = []
    for folder in sorted(os.listdir(PHOTOS_DIR)):
        fdir = os.path.join(PHOTOS_DIR, folder)
        if not os.path.isdir(fdir) or folder.startswith("."):
            continue
        for name in sorted(os.listdir(fdir)):
            if name.startswith(".") or os.path.splitext(name)[1].lower() not in EXTS:
                continue
            path = os.path.join(fdir, name)
            if not os.path.isfile(path):
                continue
            size = os.path.getsize(path)
            w, h = dimensions(path)
            if max(w, h) > MAX_EDGE or size > SIZE_FLOOR:
                out.append((path, size, w, h))
    return out


def main():
    dry = "--dry-run" in sys.argv

    if not os.path.isdir(PHOTOS_DIR):
        sys.exit("No photos/ directory found.")

    if subprocess.run(["which", "sips"], capture_output=True).returncode != 0:
        sys.exit("`sips` not found. This script only runs on macOS.")

    items = find_candidates()
    if not items:
        print("Nothing to optimize — every photo is already web-sized.")
        return

    total = sum(i[1] for i in items)
    print("{} photo(s) could be shrunk, {} total:\n".format(len(items), human(total)))
    for path, size, w, h in items[:20]:
        print("  {:<52} {:>9}  {}x{}".format(
            os.path.relpath(path, ROOT)[:52], human(size), w, h))
    if len(items) > 20:
        print("  ... and {} more".format(len(items) - 20))

    print("\nEach will be resized to max {}px on the long edge, JPEG quality {}."
          .format(MAX_EDGE, QUALITY))

    if dry:
        print("\n(dry run — nothing changed)")
        return

    if "--yes" not in sys.argv and "-y" not in sys.argv:
        print("\nThis edits the files in photos/ IN PLACE and cannot be undone.")
        print("Make sure your originals are safe elsewhere (Photos app, camera roll).")
        try:
            answer = input("Type 'yes' to continue (or anything else to abort): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nNo answer received — nothing changed.")
            print("If your terminal can't prompt, run:  ./optimize --yes")
            return
        if answer != "yes":
            print("\nAborted — nothing changed. You typed {!r}, which isn't 'yes'."
                  .format(answer))
            print("To skip this prompt next time, run:  ./optimize --yes")
            return

    saved = 0
    converted = 0

    for path, size, w, h in items:
        ext = os.path.splitext(path)[1].lower()

        # A 13 MB PNG screenshot is ~40x the size of the same image as JPEG.
        # Opaque PNGs get re-encoded; transparent ones stay as they are.
        if ext == ".png" and not png_has_alpha(path):
            dst = os.path.splitext(path)[0] + ".jpg"
            n = 2
            while os.path.exists(dst):
                dst = "{} ({}).jpg".format(os.path.splitext(path)[0], n)
                n += 1
            result = subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(QUALITY),
                 "-Z", str(MAX_EDGE), path, "--out", dst],
                capture_output=True,
            )
            if result.returncode == 0 and os.path.exists(dst):
                saved += size - os.path.getsize(dst)
                os.remove(path)
                converted += 1
                continue
            print("  ! convert failed: " + os.path.relpath(path, ROOT))
            continue

        cmd = ["sips"]
        if max(w, h) > MAX_EDGE:
            cmd += ["-Z", str(MAX_EDGE)]
        if ext in (".jpg", ".jpeg"):
            cmd += ["-s", "formatOptions", str(QUALITY)]
        if len(cmd) == 1:
            continue
        cmd.append(path)
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            saved += size - os.path.getsize(path)
        else:
            print("  ! failed: " + os.path.relpath(path, ROOT))

    print("\nDone. Saved {}{}.".format(
        human(max(saved, 0)),
        ", converted {} PNG(s) to JPEG".format(converted) if converted else ""))
    print("Now run ./update to refresh the photo index.")


if __name__ == "__main__":
    main()
