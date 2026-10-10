#!/usr/bin/env python3
# Recolors the stock TWRP theme XML files to an AMOLED black/gray palette.
# Dark colors become neutral near-black grays, bright colors (text, accents) stay.
# Usage: python3 amoled_theme.py <theme_dir> [<theme_dir> ...]
import collections
import os
import re
import sys

# Matches #RRGGBB and #RRGGBBAA
HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?(?![0-9A-Fa-f])")

# Colors whose brightest channel is below this limit are treated as "dark"
DARK_LIMIT = 0.45
# How dark the resulting gray is (0.0 = pure black, 1.0 = unchanged brightness)
DARK_FACTOR = 0.30

changes = collections.Counter()


def convert(match):
    rgb = match.group(1)
    alpha = match.group(2) or ""
    r = int(rgb[0:2], 16)
    g = int(rgb[2:4], 16)
    b = int(rgb[4:6], 16)
    if max(r, g, b) / 255.0 >= DARK_LIMIT:
        return match.group(0)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    gray = int(round(luminance * DARK_FACTOR))
    new_value = "#%02X%02X%02X%s" % (gray, gray, gray, alpha)
    if new_value.upper() != match.group(0).upper():
        changes[(match.group(0), new_value)] += 1
    return new_value


def process_file(path):
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
        text = f.read()
    new_text = HEX_RE.sub(convert, text)
    if new_text != text:
        with open(path, "w", encoding="utf-8", errors="surrogateescape") as f:
            f.write(new_text)
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 amoled_theme.py <theme_dir> [<theme_dir> ...]")
        return 1

    files_changed = 0
    files_seen = 0
    for theme_dir in sys.argv[1:]:
        if not os.path.isdir(theme_dir):
            print("WARNING: directory not found: %s" % theme_dir)
            continue
        for dirpath, dirnames, filenames in os.walk(theme_dir):
            # Language files contain no colors, skip them
            dirnames[:] = [d for d in dirnames if "languages" not in d]
            for name in filenames:
                if name.endswith(".xml"):
                    files_seen += 1
                    if process_file(os.path.join(dirpath, name)):
                        files_changed += 1

    print("AMOLED theme: %d XML files scanned, %d changed" % (files_seen, files_changed))
    print("Top color replacements (old -> new : count):")
    for (old, new), count in changes.most_common(25):
        print("  %s -> %s : %d" % (old, new, count))
    if files_seen == 0:
        print("WARNING: no XML files found, theme was NOT changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
