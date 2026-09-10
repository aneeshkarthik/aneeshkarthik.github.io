#!/usr/bin/env python3
"""
Scans photos/ and regenerates js/photos.js.

Run this every time you add, remove, or rename photos:

    ./update

Naming your files controls the captions and the order:

    photos/gym/01 - First deadlift PR.jpg   ->  caption "First deadlift PR", sorted first
    photos/gym/02.jpg                       ->  no caption, sorted second
    photos/gym/anything.jpg                 ->  no caption, sorted alphabetically

Nothing else needs configuring. Section metadata lives in sections.json.
"""

import json
import os
import re
import struct
import subprocess
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(ROOT, "photos")
OUT_FILE = os.path.join(ROOT, "js", "photos.js")

# Small copies for the grid and photolog tiles. The full photo is only fetched
# when a carousel opens, so first paint costs kilobytes instead of megabytes.
THUMBS_DIR = os.path.join(PHOTOS_DIR, "_thumbs")
THUMB_EDGE = 640
THUMB_QUALITY = 68

EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}

# "01 - Caption here.jpg" / "01. Caption here.jpg" / "01_Caption here.jpg"
CAPTION_RE = re.compile(r"^\s*\d+\s*[-–_.)]\s*(.+)$")
LEADING_NUM_RE = re.compile(r"^\s*(\d+)")


# ---------------------------------------------------------------------------
# Image dimensions, stdlib only (no Pillow required).
# We only need width/height so the page can reserve space and never jump
# while images load.
# ---------------------------------------------------------------------------

def _png_size(f):
    head = f.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def _gif_size(f):
    head = f.read(10)
    if len(head) < 10 or head[:6] not in (b"GIF87a", b"GIF89a"):
        return None
    return struct.unpack("<HH", head[6:10])


def _webp_size(f):
    head = f.read(30)
    if len(head) < 30 or head[:4] != b"RIFF" or head[8:12] != b"WEBP":
        return None
    chunk = head[12:16]
    if chunk == b"VP8 ":
        w, h = struct.unpack("<HH", head[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if chunk == b"VP8L":
        b = head[21:25]
        n = struct.unpack("<I", b)[0]
        return (n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1
    if chunk == b"VP8X":
        w = head[24] | (head[25] << 8) | (head[26] << 16)
        h = head[27] | (head[28] << 8) | (head[29] << 16)
        return w + 1, h + 1
    return None


def _jpeg_size(f):
    f.seek(0)
    if f.read(2) != b"\xff\xd8":
        return None
    while True:
        b = f.read(1)
        if not b:
            return None
        if b != b"\xff":
            continue
        # Skip fill bytes
        marker = f.read(1)
        while marker == b"\xff":
            marker = f.read(1)
        if not marker:
            return None
        m = marker[0]
        # Standalone markers with no payload
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            continue
        payload = f.read(2)
        if len(payload) < 2:
            return None
        length = struct.unpack(">H", payload)[0]
        # SOF markers that carry dimensions (excluding DHT/JPG/DAC)
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            data = f.read(5)
            if len(data) < 5:
                return None
            h, w = struct.unpack(">HH", data[1:5])
            return w, h
        f.seek(length - 2, os.SEEK_CUR)


def exif_orientation(path):
    """
    Return the JPEG EXIF orientation (1-8), or None.

    Phone cameras usually store the sensor's raw landscape pixels plus a flag
    saying "rotate this on display". Browsers honour the flag; a naive header
    read does not. Without this, every portrait phone photo gets indexed with
    its width and height swapped.
    """
    try:
        with open(path, "rb") as f:
            if f.read(2) != b"\xff\xd8":
                return None
            while True:
                b = f.read(1)
                if not b:
                    return None
                if b != b"\xff":
                    continue
                marker = f.read(1)
                while marker == b"\xff":
                    marker = f.read(1)
                if not marker:
                    return None
                m = marker[0]
                if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                    continue
                raw = f.read(2)
                if len(raw) < 2:
                    return None
                data = f.read(struct.unpack(">H", raw)[0] - 2)

                if m == 0xE1 and data[:6] == b"Exif\x00\x00":
                    tiff = data[6:]
                    if len(tiff) < 8:
                        return None
                    if tiff[:2] == b"II":
                        bo = "<"
                    elif tiff[:2] == b"MM":
                        bo = ">"
                    else:
                        return None
                    off = struct.unpack(bo + "I", tiff[4:8])[0]
                    if off + 2 > len(tiff):
                        return None
                    count = struct.unpack(bo + "H", tiff[off:off + 2])[0]
                    for i in range(count):
                        e = off + 2 + i * 12
                        if e + 12 > len(tiff):
                            break
                        if struct.unpack(bo + "H", tiff[e:e + 2])[0] == 0x0112:
                            return struct.unpack(bo + "H", tiff[e + 8:e + 10])[0]
                    return None
                if m == 0xDA:  # start of scan — no EXIF before the image data
                    return None
    except (OSError, struct.error, IndexError):
        return None


def image_size(path):
    """Return (width, height) or None if the format isn't readable."""
    try:
        with open(path, "rb") as f:
            for reader in (_png_size, _gif_size, _webp_size, _jpeg_size):
                f.seek(0)
                try:
                    size = reader(f)
                except (struct.error, IndexError, OSError):
                    size = None
                if size and size[0] > 0 and size[1] > 0:
                    return size
    except OSError:
        pass
    return None


# ---------------------------------------------------------------------------

def caption_for(filename):
    stem = os.path.splitext(filename)[0]
    # "cover.jpg" is a marker, not a caption. "cover - Text.jpg" keeps the text.
    if stem.lower() == "cover":
        return ""
    if stem.lower().startswith("cover "):
        return stem[6:].lstrip(" -–_.").strip()
    match = CAPTION_RE.match(stem)
    if match:
        return match.group(1).strip()
    # A bare number like "03" is a deliberate no-caption photo.
    if re.fullmatch(r"\s*\d+\s*", stem):
        return ""
    # Otherwise treat a normal filename as no caption; machine-generated names
    # would only be noise under the photo.
    if re.match(r"^(IMG|DSC|PXL|Screenshot|Photo|image)[\s_-]", stem, re.I):
        return ""
    if re.fullmatch(r"[A-Za-z0-9_-]{0,4}\d{3,}", stem):
        return ""
    # UUIDs, the usual result of AirDrop or an iCloud export.
    if re.fullmatch(r"[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}", stem):
        return ""
    # Epoch timestamps and other long digit runs.
    if re.fullmatch(r"\d{6,}", stem):
        return ""
    # Anything long with no spaces is a filename, not a sentence.
    if " " not in stem and len(stem) >= 16:
        return ""
    if stem.lower().replace(" ", "") in (
        "fullsizerender", "untitled", "image", "photo", "picture", "unknown",
        "img", "dsc", "pxl", "screenshot"
    ):
        return ""
    return stem.replace("_", " ").strip()


def sort_key(filename):
    stem = os.path.splitext(filename)[0].lower()
    # A file named cover.* always wins — it becomes the card's cover image.
    if stem == "cover" or stem.startswith("cover "):
        return (-1, 0, stem)
    match = LEADING_NUM_RE.match(filename)
    # Numbered files come next, in numeric order; everything else alphabetical.
    return (0, int(match.group(1)), filename.lower()) if match else (1, 0, filename.lower())


def make_thumb(src, folder, name):
    """
    Build (or reuse) a small copy of `src`. Returns its web path, or None if
    sips isn't available or the resize fails — callers fall back to the full
    photo, so a missing thumbnail is never fatal.
    """
    out_dir = os.path.join(THUMBS_DIR, folder)
    dst = os.path.join(out_dir, os.path.splitext(name)[0] + ".jpg")

    # Skip work if the thumbnail is already newer than the source.
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return "photos/_thumbs/{}/{}".format(
            quote(folder, safe=""), quote(os.path.basename(dst), safe=""))

    os.makedirs(out_dir, exist_ok=True)
    result = subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(THUMB_QUALITY),
         "-Z", str(THUMB_EDGE), src, "--out", dst],
        capture_output=True,
    )
    if result.returncode != 0 or not os.path.exists(dst):
        return None
    return "photos/_thumbs/{}/{}".format(
        quote(folder, safe=""), quote(os.path.basename(dst), safe=""))


def prune_thumbs(keep):
    """Delete thumbnails whose source photo no longer exists."""
    if not os.path.isdir(THUMBS_DIR):
        return 0
    removed = 0
    for folder in os.listdir(THUMBS_DIR):
        fdir = os.path.join(THUMBS_DIR, folder)
        if not os.path.isdir(fdir):
            continue
        for name in os.listdir(fdir):
            if os.path.join(folder, name) not in keep:
                try:
                    os.remove(os.path.join(fdir, name))
                    removed += 1
                except OSError:
                    pass
        if not os.listdir(fdir):
            try:
                os.rmdir(fdir)
            except OSError:
                pass
    return removed


def scan():
    if not os.path.isdir(PHOTOS_DIR):
        sys.exit("No photos/ directory found next to update.py.")

    has_sips = subprocess.run(["which", "sips"], capture_output=True).returncode == 0

    result = {}
    total = 0
    unreadable = []
    skipped = []
    thumbs_made = 0
    thumb_keep = set()

    for folder in sorted(os.listdir(PHOTOS_DIR)):
        folder_path = os.path.join(PHOTOS_DIR, folder)
        # "_"-prefixed folders are scratch space (e.g. _heic-originals, which
        # ./convert fills with your untouched originals) — never indexed, and
        # never warned about.
        if (not os.path.isdir(folder_path)
                or folder.startswith(".") or folder.startswith("_")):
            continue

        all_names = [
            name for name in os.listdir(folder_path)
            if not name.startswith(".")
            and os.path.isfile(os.path.join(folder_path, name))
        ]

        # Anything a browser can't display gets called out rather than
        # silently ignored — HEIC straight off an iPhone is the usual culprit.
        for name in all_names:
            ext = os.path.splitext(name)[1].lower()
            if ext not in EXTS and ext not in (".md", ".txt"):
                skipped.append(os.path.join(folder, name))

        files = [n for n in all_names if os.path.splitext(n)[1].lower() in EXTS]
        files.sort(key=sort_key)

        entries = []
        for name in files:
            full = os.path.join(folder_path, name)
            size = image_size(full)
            if size is None:
                unreadable.append(os.path.join(folder, name))
            elif exif_orientation(full) in (5, 6, 7, 8):
                # Rotated a quarter turn on display, so the stored width and
                # height are the wrong way round for layout purposes.
                size = (size[1], size[0])
            entry = {
                # Percent-encode so filenames containing #, ?, & or spaces
                # still resolve as URLs.
                "src": "photos/{}/{}".format(
                    quote(folder, safe=""), quote(name, safe="")
                ),
                "caption": caption_for(name),
            }
            if size:
                entry["w"], entry["h"] = size

            if has_sips:
                thumb = make_thumb(full, folder, name)
                if thumb:
                    entry["thumb"] = thumb
                    thumbs_made += 1
                    thumb_keep.add(os.path.join(
                        folder, os.path.splitext(name)[0] + ".jpg"))

            entries.append(entry)

        result[folder] = entries
        total += len(entries)
        print("  {:<20} {:>3} photo{}".format(folder, len(entries), "" if len(entries) == 1 else "s"))

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("// Generated by update.py — do not edit by hand.\n")
        f.write("// Add or rename photos in photos/, then run ./update\n")
        f.write("window.PHOTOS = ")
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    stale = prune_thumbs(thumb_keep)

    print("\n{} photos indexed -> js/photos.js".format(total))
    if thumbs_made:
        print("{} thumbnails ready in photos/_thumbs/{}".format(
            thumbs_made, " ({} stale removed)".format(stale) if stale else ""))
    elif total and not has_sips:
        print("`sips` not found, so no thumbnails were made — the grid will "
              "load full-size photos.")

    if skipped:
        heic = [n for n in skipped if os.path.splitext(n)[1].lower() in (".heic", ".heif")]
        print("\n" + "!" * 62)
        print("SKIPPED {} file(s) — browsers can't display these formats:"
              .format(len(skipped)))
        for name in skipped[:10]:
            print("  " + name)
        if len(skipped) > 10:
            print("  ... and {} more".format(len(skipped) - 10))
        if heic:
            print("\n{} of them are HEIC (the iPhone default). Convert them to "
                  "JPEG with:\n".format(len(heic)))
            print("    ./convert")
            print("\n...then run ./update again.")
        print("!" * 62)

    if unreadable:
        print("\nCouldn't read dimensions for {} file(s); they'll still show, "
              "just without reserved space:".format(len(unreadable)))
        for name in unreadable[:10]:
            print("  " + name)
    if total == 0:
        print("\nNothing found yet. Drop images into the folders under photos/ "
              "and run this again.")


if __name__ == "__main__":
    print("Scanning photos/ ...\n")
    scan()
