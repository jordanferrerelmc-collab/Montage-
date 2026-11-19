"""Make a self-contained animated HTML page of icons, for screen-recording into videos
or embedding in a site. Open the file in a browser; click anywhere to replay.

Styles:
  pop    icons pop in one after another (default)
  slide  icons slide up and fade in one after another
  float  icons pop in, then bob gently forever
  wave   icons ripple up and down in a continuous wave

Examples:
  python animate.py react,ts,nodejs,postgres -o stack.html
  python animate.py react ts nodejs --style wave --size 140 --title "My stack" -o intro.html
  python animate.py docker,kubernetes --theme light --bg transparent -o k8s.html
"""
import argparse
import html
import sys
from pathlib import Path

from _common import THEMES, read_svg, resolve_or_exit, split_names

DEFAULT_BG = {"dark": "#0D1117", "light": "#FFFFFF", "brand": "#111318"}
TEXT_COLOR = {"dark": "#E6EDF3", "light": "#1F2328", "brand": "#E6EDF3"}

KEYFRAMES = {
    "pop": """
@keyframes enter { 0% { opacity: 0; transform: scale(0.3); }
                   70% { opacity: 1; transform: scale(1.08); }
                   100% { opacity: 1; transform: scale(1); } }
.icon { animation: enter var(--dur) cubic-bezier(.2,.8,.3,1.2) both; animation-delay: calc(var(--i) * var(--stagger)); }""",
    "slide": """
@keyframes enter { from { opacity: 0; transform: translateY(40%); } to { opacity: 1; transform: none; } }
.icon { animation: enter var(--dur) cubic-bezier(.2,.8,.2,1) both; animation-delay: calc(var(--i) * var(--stagger)); }""",
    "float": """
@keyframes enter { 0% { opacity: 0; transform: scale(0.3); } 70% { opacity: 1; transform: scale(1.08); }
                   100% { opacity: 1; transform: scale(1); } }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8%); } }
.icon { animation: enter var(--dur) cubic-bezier(.2,.8,.3,1.2) both; animation-delay: calc(var(--i) * var(--stagger)); }
.icon > svg { animation: bob 3s ease-in-out infinite; animation-delay: calc(var(--i) * -0.4s); }""",
    "wave": """
@keyframes wave { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-25%); } }
.icon { animation: wave calc(var(--dur) * 3) ease-in-out infinite; animation-delay: calc(var(--i) * var(--stagger)); }""",
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_text}</title>
<style>
:root {{ --size: {size}px; --gap: {gap}px; --dur: {duration}s; --stagger: {stagger}s; }}
html, body {{ margin: 0; height: 100%; }}
body {{ background: {bg}; color: {text}; display: flex; flex-direction: column; align-items: center;
        justify-content: center; gap: calc(var(--size) * 0.4);
        font-family: system-ui, -apple-system, "Segoe UI", sans-serif; cursor: pointer; }}
h1 {{ margin: 0; font-size: calc(var(--size) * 0.36); font-weight: 650; letter-spacing: -0.01em; }}
.row {{ display: flex; flex-wrap: wrap; justify-content: center; gap: var(--gap); max-width: {max_width}px; padding: 0 16px; }}
.icon, .icon > svg {{ width: var(--size); height: var(--size); display: block; }}
{keyframes}
</style>
</head>
<body>
{heading}<div class="row">
{icons}
</div>
<script>
// Click anywhere to replay the animation (handy when screen-recording).
document.body.addEventListener('click', () => {{
  for (const el of document.querySelectorAll('.icon, .icon > svg')) {{
    el.style.animation = 'none'; void el.offsetWidth; el.style.animation = '';
  }}
}});
</script>
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser(description="Make an animated HTML page of icons.")
    p.add_argument("icons", nargs="+", help="icon names (comma or space separated)")
    p.add_argument("--theme", choices=THEMES, default="dark")
    p.add_argument("--style", choices=sorted(KEYFRAMES), default="pop")
    p.add_argument("--size", type=int, default=120, help="icon size in px (default 120)")
    p.add_argument("--perline", type=int, default=8, help="icons per row before wrapping (default 8)")
    p.add_argument("--duration", type=float, default=0.6, help="seconds per icon animation (default 0.6)")
    p.add_argument("--stagger", type=float, default=0.12, help="seconds between icons (default 0.12)")
    p.add_argument("--bg", help='page background, e.g. "#000000" or "transparent" (default depends on theme)')
    p.add_argument("--title", help="optional heading shown above the icons")
    p.add_argument("-o", "--out", default="stack.html", help="output file (default stack.html)")
    args = p.parse_args()

    if args.size < 8 or args.perline < 1:
        sys.exit("error: --size must be >= 8 and --perline >= 1")

    icons = resolve_or_exit(split_names(args.icons))
    gap = round(args.size / 5)
    tiles = "\n".join(
        f'<div class="icon" style="--i:{i}" title="{html.escape(icon["name"])}">'
        f'{read_svg(icon["id"], args.theme)}</div>'
        for i, icon in enumerate(icons)
    )
    title = args.title or ", ".join(icon["name"] for icon in icons)

    page = PAGE.format(
        title_text=html.escape(title),
        size=args.size,
        gap=gap,
        duration=args.duration,
        stagger=args.stagger,
        bg=args.bg or DEFAULT_BG[args.theme],
        text=TEXT_COLOR[args.theme],
        max_width=args.perline * args.size + (args.perline - 1) * gap + 32,
        keyframes=KEYFRAMES[args.style],
        heading=f"<h1>{html.escape(args.title)}</h1>\n" if args.title else "",
        icons=tiles,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out} ({len(icons)} icons, {args.style} style, {args.theme} theme). Open it in a browser.")


if __name__ == "__main__":
    main()
