#!/usr/bin/env python3
"""Verrou de charte : refuse toute couleur absente de brand/<marque>/brand.json
et toute police autre que celle de la marque (var(--font)).

Analyse les compositions des projets vidéo (projets/*/montage/index.html), le modèle
templates/ et la charte elle-même. Codes de sortie : 0 = conforme, 1 = couleur hors charte.
Usage : python3 scripts/check-brand.py [--brand specimen-agency] [fichiers...]
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
brand = "specimen-agency"
if "--brand" in args:
    i = args.index("--brand"); brand = args[i + 1]; del args[i:i + 2]
spec = json.load(open(f"{ROOT}/brand/{brand}/brand.json"))

def norm_hex(h):
    h = h.lower().lstrip("#")
    if len(h) in (3, 4): h = "".join(c * 2 for c in h[:3])
    return "#" + h[:6]

allowed_hex = set()
for v in spec["colors"].values():
    for c in (v if isinstance(v, list) else [v]):
        allowed_hex.add(norm_hex(c))
allowed_rgb = {tuple(int(x) for x in t.split(",")) for t in spec["rgb_allowed"]}
for h in allowed_hex:
    allowed_rgb.add(tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)))

NAMED = re.compile(r"(?<![\w-])(red|green|blue|pink|purple|orange|yellow|cyan|magenta|lime|teal)(?![\w-])", re.I)
HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")

files = args or (glob.glob(f"{ROOT}/projets/*/montage/index.html")
                 + glob.glob(f"{ROOT}/templates/**/*.html", recursive=True)
                 + [f"{ROOT}/brand/{brand}/brand.css"])
bad = 0
for f in files:
    txt = open(f, encoding="utf-8").read()
    # ne contrôle que le style et le balisage graphique, pas le JS ni le texte des sous-titres
    zones = re.findall(r"<style>(.*?)</style>", txt, re.S) or [txt]
    zones += re.findall(r'(?:style|fill|stroke|stop-color|color)="([^"]*)"', txt)
    zone = "\n".join(zones)
    issues = set()
    for h in HEX.findall(zone):
        if len(h) in (4, 5, 7, 9) and norm_hex(h) not in allowed_hex:
            issues.add(h)
    for r in RGB.findall(zone):
        if tuple(int(x) for x in r) not in allowed_rgb:
            issues.add("rgb(" + ",".join(r) + ")")
    for css in re.findall(r"(?:color|background|fill|stroke|border)[^;{}]*:[^;{}]*", zone):
        for n in NAMED.findall(css):
            issues.add(n)
    # police verrouillée : seule var(--font) (ou la famille de la marque) est autorisée
    family = spec["fonts"]["family"]
    for ff in re.findall(r"font-family\s*:\s*([^;}\"]+(?:\"[^\"]*\"[^;}]*)?)", zone):
        val = ff.strip()
        if val not in ("var(--font)", "inherit") and not val.startswith(f'"{family}"'):
            issues.add("police " + val)
    if f.endswith("index.html") and family not in txt:
        issues.add("police de marque absente (brand.css non injecté ?)")
    rel = os.path.relpath(f, ROOT)
    if issues:
        bad += 1
        print(f"✗ {rel} : hors charte {sorted(issues)}")
    else:
        print(f"✓ {rel}")
if bad:
    print(f"\nCharte « {spec['name']} » non respectée. Utilisez les variables de brand/{brand}/brand.css.")
    sys.exit(1)
print(f"\n✅ Charte « {spec['name']} » respectée.")
