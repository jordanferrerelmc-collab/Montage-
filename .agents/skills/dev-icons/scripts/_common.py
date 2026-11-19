"""Shared helpers: load the manifest, resolve icon names, read tiles from tiles.bin."""
import difflib
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
THEMES = ("dark", "light", "brand")
PNG_SIZES = (128, 512)


def load_manifest():
    with open(SKILL_DIR / "manifest.json", encoding="utf-8") as f:
        return json.load(f)


def normalize(name):
    """'Next.js' -> 'nextjs', 'Tailwind CSS' -> 'tailwindcss' (keeps + and # for c++/c#)."""
    return re.sub(r"[^a-z0-9+#]", "", name.lower())


def build_index(manifest):
    """Map every id, display name and alias to its icon. Ids win over aliases."""
    index = {}
    for icon in manifest:
        index[normalize(icon["id"])] = icon
    for icon in manifest:
        for key in [icon["name"], *icon["aliases"]]:
            index.setdefault(normalize(key), icon)
    return index


def split_names(args):
    """Accept 'react,ts nodejs' style input: commas and spaces both separate names."""
    return [n for a in args for n in a.split(",") if n.strip()]


def suggest(name, index):
    close = difflib.get_close_matches(normalize(name), index.keys(), n=3, cutoff=0.6)
    return sorted({index[c]["id"] for c in close})


def resolve_or_exit(names):
    """Turn user-typed names into manifest entries, or exit with suggestions."""
    index = build_index(load_manifest())
    found, errors = [], []
    for name in names:
        icon = index.get(normalize(name))
        if icon:
            found.append(icon)
            continue
        hint = suggest(name, index)
        errors.append(f'unknown icon "{name}"' + (f" (did you mean: {', '.join(hint)}?)" if hint else ""))
    if errors:
        for e in errors:
            print("error: " + e, file=sys.stderr)
        print("Run find.py --list to see every available icon.", file=sys.stderr)
        sys.exit(1)
    if not found:
        print("error: no icons given", file=sys.stderr)
        sys.exit(1)
    return found


@lru_cache(maxsize=None)
def _tile_index():
    """tiles.json maps each tile path to [offset, length] inside tiles.bin.

    All tiles are packed into that one plain file because skill uploads allow
    at most 200 files and no archives inside the upload.
    """
    with open(SKILL_DIR / "tiles.json", encoding="utf-8") as f:
        return json.load(f)


def _read_tile(name):
    offset, length = _tile_index()[name]
    with open(SKILL_DIR / "tiles.bin", "rb") as f:
        f.seek(offset)
        return f.read(length)


def read_svg(icon_id, theme):
    """The full SVG tile as text."""
    return _read_tile(f"icons/{theme}/{icon_id}.svg").decode("utf-8")


def read_png(icon_id, theme, size):
    """A pre-rendered PNG tile as bytes (size must be one of PNG_SIZES)."""
    return _read_tile(f"png/{theme}/{size}/{icon_id}.png")


def svg_inner(icon_id, theme):
    """The tile's contents without its outer <svg> tag, for nesting inside another SVG."""
    text = read_svg(icon_id, theme)
    return text[text.index(">") + 1 : text.rindex("</svg>")]


def require_pillow(reason):
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print(f"error: {reason} needs Pillow (pip install pillow). Use SVG output instead.", file=sys.stderr)
        sys.exit(1)
