"""Copy individual icon files out of the skill, ready for slides, docs or a website.

Examples:
  python export.py react ts nodejs -o ./icons                    dark 512px PNGs
  python export.py react,ts --theme light --format svg -o ./icons
  python export.py docker --size 256 -o ./icons                  any size (needs Pillow
                                                                 unless 128 or 512)
  python export.py react,vue --theme all --format both -o ./icons
      -> ./icons/dark/react.png, ./icons/dark/react.svg, ./icons/light/... and so on
"""
import argparse
import io
import sys
from pathlib import Path

from _common import PNG_SIZES, THEMES, read_png, read_svg, resolve_or_exit, split_names


def export_png(icon_id, theme, size, dest):
    if size in PNG_SIZES:
        dest.write_bytes(read_png(icon_id, theme, size))
        return
    try:
        from PIL import Image
    except ImportError:
        nearest = min(PNG_SIZES, key=lambda s: abs(s - size))
        print(f"warning: Pillow not installed, exporting {nearest}px instead of {size}px", file=sys.stderr)
        dest.write_bytes(read_png(icon_id, theme, nearest))
        return
    Image.open(io.BytesIO(read_png(icon_id, theme, 512))).resize((size, size), Image.LANCZOS).save(dest)


def main():
    p = argparse.ArgumentParser(description="Export icon files.")
    p.add_argument("icons", nargs="+", help="icon names (comma or space separated)")
    p.add_argument("--theme", choices=[*THEMES, "all"], default="dark")
    p.add_argument("--format", choices=["png", "svg", "both"], default="png")
    p.add_argument("--size", type=int, default=512, help="PNG size in px (default 512)")
    p.add_argument("-o", "--out", default="icons", help="output folder (default ./icons)")
    args = p.parse_args()

    if args.size < 8:
        sys.exit("error: --size must be >= 8")
    if args.size > 512 and args.format != "svg":
        print("warning: PNG tiles are 512px, so larger sizes will look soft; use --format svg for big output",
              file=sys.stderr)

    icons = resolve_or_exit(split_names(args.icons))
    themes = THEMES if args.theme == "all" else (args.theme,)
    written = []

    for theme in themes:
        folder = Path(args.out) / theme if len(themes) > 1 else Path(args.out)
        folder.mkdir(parents=True, exist_ok=True)
        for icon in icons:
            if args.format in ("png", "both"):
                dest = folder / f"{icon['id']}.png"
                export_png(icon["id"], theme, args.size, dest)
                written.append(dest)
            if args.format in ("svg", "both"):
                dest = folder / f"{icon['id']}.svg"
                dest.write_text(read_svg(icon["id"], theme), encoding="utf-8")
                written.append(dest)

    for path in written:
        print(f"  {path}")
    print(f"Exported {len(written)} file{'' if len(written) == 1 else 's'}")


if __name__ == "__main__":
    main()
