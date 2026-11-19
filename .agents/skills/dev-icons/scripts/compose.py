"""Join several icons into one strip or grid, like a skillicons tech-stack banner.

Examples:
  python compose.py react,ts,nodejs,postgres -o stack.svg
  python compose.py react ts nodejs --theme light --size 64 --gap 12 -o stack.svg
  python compose.py html,css,js,react,nextjs,vue,svelte --perline 4 -o grid.png
  (.png output needs Pillow; .svg output needs nothing)
"""
import argparse
import io
import math
import sys
from pathlib import Path

from _common import THEMES, read_png, require_pillow, resolve_or_exit, split_names, svg_inner


def layout(count, perline, size, gap):
    cols = min(count, perline)
    rows = math.ceil(count / cols)
    width = cols * size + (cols - 1) * gap
    height = rows * size + (rows - 1) * gap
    positions = [((i % cols) * (size + gap), (i // cols) * (size + gap)) for i in range(count)]
    return width, height, positions


def compose_svg(icons, theme, size, gap, perline):
    width, height, positions = layout(len(icons), perline, size, gap)
    label = ", ".join(i["name"] for i in icons)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{label}">'
    ]
    for icon, (x, y) in zip(icons, positions):
        parts.append(
            f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 256 256">'
            f"{svg_inner(icon['id'], theme)}</svg>"
        )
    parts.append("</svg>")
    return "".join(parts)


def compose_png(icons, theme, size, gap, perline, out):
    require_pillow("PNG output")
    from PIL import Image

    width, height, positions = layout(len(icons), perline, size, gap)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for icon, (x, y) in zip(icons, positions):
        tile = Image.open(io.BytesIO(read_png(icon["id"], theme, 512))).convert("RGBA")
        tile = tile.resize((size, size), Image.LANCZOS)
        canvas.alpha_composite(tile, (x, y))
    canvas.save(out)
    return width, height


def main():
    p = argparse.ArgumentParser(description="Compose icons into a strip or grid.")
    p.add_argument("icons", nargs="+", help="icon names (comma or space separated)")
    p.add_argument("--theme", choices=THEMES, default="dark")
    p.add_argument("--size", type=int, default=48, help="size of each icon in px (default 48)")
    p.add_argument("--gap", type=int, default=None, help="space between icons in px (default size/6)")
    p.add_argument("--perline", type=int, default=15, help="icons per row before wrapping (default 15)")
    p.add_argument("-o", "--out", default="stack.svg", help="output file, .svg or .png (default stack.svg)")
    args = p.parse_args()

    if args.size < 8 or args.perline < 1:
        sys.exit("error: --size must be >= 8 and --perline >= 1")
    if args.size > 512:
        print("warning: PNG tiles are 512px, so PNG output above that will look soft; SVG stays sharp", file=sys.stderr)
    gap = args.gap if args.gap is not None else round(args.size / 6)

    icons = resolve_or_exit(split_names(args.icons))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if out.suffix.lower() == ".png":
        width, height = compose_png(icons, args.theme, args.size, gap, args.perline, out)
    elif out.suffix.lower() == ".svg":
        svg = compose_svg(icons, args.theme, args.size, gap, args.perline)
        out.write_text(svg, encoding="utf-8")
        width, height, _ = layout(len(icons), args.perline, args.size, gap)
    else:
        sys.exit("error: --out must end in .svg or .png")

    print(f"Wrote {out} ({width}x{height}px, {len(icons)} icons, {args.theme} theme)")


if __name__ == "__main__":
    main()
