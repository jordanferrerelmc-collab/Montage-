"""Montage style « éditorial » (référence : references/reel-style) — génère montage/index.html.

Sous-titres mot à mot sans contour, grands titres derrière la tête (sujet détouré),
cartes flottantes, transitions en halo lumineux. Charte lue dans brand/<BRAND>/.
"""
import html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = os.environ.get("BRAND", "specimen-agency")
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
words = json.load(open(f"{ROOT}/work/words_cut.json"))
W = {i: w["start"] for i, w in enumerate(words)}
E = {i: w["end"] for i, w in enumerate(words)}

SPEECH_END = 26.05
DUR = 28.8
SOFTEN = True  # la source contient des sous-titres incrustés effacés : léger flou de la zone

# --------------------------------------------------------------------------- sous-titres
fix = {4: "200", 19: "« bonjour,", 23: "de… »", 41: "1.", 43: "/ après", 44: "2.", 58: "3.", 79: "envoie"}
keys = {4, 5, 9, 26, 40, 42, 43, 49, 55, 63, 66, 78, 83}
glue = {"le", "la", "les", "de", "du", "un", "une", "à", "a", "ce", "je", "tu", "il", "y", "n'y", "en", "et", "ou",
        "si", "par", "que", "qui", "pas", "c'est", "n'est", "font", "tes", "tous", "soit", "ça"}

def txt(i):
    t = fix.get(i, words[i]["text"])
    return t if i in fix else re.sub(r"[.,]$", "", t)

groups, cur = [], []
for i in range(len(words)):
    cur.append(i)
    joined = " ".join(txt(k) for k in cur)
    if txt(i).lower() in glue and len(cur) < 3 and len(joined) < 14 and i + 1 < len(words):
        continue
    groups.append(cur); cur = []
if cur: groups.append(cur)

caps_html, js = [], []
for gi, g in enumerate(groups):
    start = max(0.0, W[g[0]] - 0.04)
    end = (W[groups[gi + 1][0]] - 0.04) if gi + 1 < len(groups) else SPEECH_END
    label = " ".join(txt(i) for i in g)
    key = " key" if any(i in keys for i in g) else ""
    caps_html.append(f'<div class="cap clip{key}" id="c{gi}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                     f'data-track-index="4">{html.escape(label)}</div>')
    js.append(f'  tl.fromTo("#c{gi}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: 0.12, ease: "power2.out"}}, {start:.3f});')

# --------------------------------------------------------------------------- cadrage + halos
sections = [0.0, 3.86, 8.27, 10.61, 13.50, 14.95, 18.66, 22.27, 24.17]
framing = [1.00, 1.08, 1.00, 1.10, 1.02, 1.08, 1.00, 1.10, 1.02]
micro = [1.98, 3.24, 4.40, 4.80, 9.52, 16.30, 20.30]
sfx = []
for k, t in enumerate(sections):
    z = framing[k]
    nxt = sections[k + 1] if k + 1 < len(sections) else SPEECH_END
    if k:
        js.append(f'  tl.fromTo("#bloom", {{opacity: 0}}, {{opacity: 0.8, duration: 0.16, ease: "sine.in", immediateRender: false}}, {t - 0.16:.3f});')
        js.append(f'  tl.to("#bloom", {{opacity: 0, duration: 0.34, ease: "sine.out"}}, {t:.3f});')
        sfx.append((t - 0.2, "whoosh", 0.4, 0.18))
    js.append(f'  tl.fromTo("#cam", {{scale: {z:.3f}}}, {{scale: {z * 1.035:.3f}, duration: {nxt - t:.3f}, ease: "none", immediateRender: {"true" if k == 0 else "false"}}}, {t:.3f});')
for n, t in enumerate(micro):
    js.append(f'  tl.to("#punch", {{scale: {1.035 if n % 2 == 0 else 1.0}, duration: 0.08, ease: "power1.out"}}, {t:.3f});')

# --------------------------------------------------------------------------- titres derrière la tête
behind, bi = [], 0
def title(start, end, small, big, size=None, top=240):
    global bi
    size = size or min(215, int(1380 / max(4, len(big))))
    behind.append(f'<div class="behind clip" id="t{bi}" style="--title-top:{top}px" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="2">'
                  f'<span class="small">{html.escape(small)}</span><span class="huge" style="font-size:{size}px">{html.escape(big)}</span></div>')
    js.append(f'  tl.from("#t{bi} .small", {{opacity: 0, y: 20, duration: 0.25, ease: "power2.out"}}, {start:.3f});')
    js.append(f'  tl.from("#t{bi} .huge", {{opacity: 0, scale: 1.12, duration: 0.35, ease: "power3.out"}}, {start + 0.08:.3f});')
    js.append(f'  tl.fromTo("#t{bi} .huge", {{color: "var(--accent)"}}, {{color: "var(--ink)", duration: 0.5, ease: "none", immediateRender: false}}, {start + 0.6:.3f});')
    js.append(f'  tl.to("#t{bi}", {{opacity: 0, duration: 0.2}}, {end - 0.2:.3f});')
    bi += 1

title(0.0, W[6] - 0.05, "tes vidéos font", "200 vues", top=120)
title(W[24] - 0.05, sections[3], "non, c'est", "faux")
title(W[36] - 0.05, sections[4], "je commence par le", "résultat")
title(W[73] - 0.05, sections[8], "il n'y a pas de", "secret")

# --------------------------------------------------------------------------- cartes flottantes
cards = []
def deck(id_, start, end, inner):
    cards.append(f'<div class="deck clip" id="{id_}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">{inner}</div>')
    js.append(f'  tl.to("#{id_}", {{opacity: 0, scale: 0.94, duration: 0.2}}, {end - 0.2:.3f});')

def card(cid, x, y, w, h, rot, inner, light=False):
    return (f'<div class="card{" light" if light else ""}" id="{cid}" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px; '
            f'transform: rotate({rot}deg)">{inner}</div>')

def pop(sel, t, dx=0, dy=120, rot=0):
    js.append(f'  tl.from("{sel}", {{opacity: 0, x: {dx}, y: {dy}, rotation: "+={rot}", scale: 0.85, duration: 0.45, ease: "back.out(1.6)"}}, {t:.3f});')
    sfx.append((t, "pop", 0.12, 0.15))

RING = ('<svg viewBox="0 0 100 100" class="ring"><circle cx="50" cy="50" r="40" fill="none" style="stroke:var(--dark)" stroke-width="10"/>'
        '<circle id="ringarc" cx="50" cy="50" r="40" fill="none" style="stroke:var(--accent)" stroke-width="10" stroke-linecap="round" '
        'pathLength="1" stroke-dasharray="1" stroke-dashoffset="0.86" transform="rotate(-90 50 50)"/></svg>')
deck("d-views", W[6] - 0.05, sections[1],
     card("k-views", 640, 10, 360, 420, 6, f'<span class="label">vues</span>{RING}<span class="value" style="text-align:center">200</span>'))
pop("#k-views", W[6] - 0.05, dx=200, dy=0, rot=8)

deck("d-hello", sections[1] + 0.1, sections[2],
     card("k-timer", 90, 0, 360, 380, -7, '<span class="label">ton reel</span><span class="value">3 s</span><span class="text">pour accrocher</span>')
     + card("k-hello", 470, 40, 520, 330, 5, '<span class="label">à éviter</span><span class="text">« Bonjour, je vais parler de… »</span>', light=True))
pop("#k-timer", sections[1] + 0.1, dx=-160, rot=-6)
pop("#k-hello", W[19] - 0.05, dx=160, rot=6)

GRAPH_FLAT = '<svg viewBox="0 0 100 50"><polyline points="0,40 50,38 100,41" fill="none" style="stroke:var(--taupe)" stroke-width="5"/></svg>'
GRAPH_UP = '<svg viewBox="0 0 100 50"><polyline points="0,46 40,32 70,20 100,4" fill="none" style="stroke:var(--accent)" stroke-width="6" stroke-linecap="round"/></svg>'
deck("d-ba", sections[4], sections[5],
     card("k-before", 110, 20, 400, 360, -6, f'<span class="label" style="color:var(--taupe)">avant</span>{GRAPH_FLAT}')
     + card("k-after", 560, 0, 410, 380, 5, f'<span class="label">après</span>{GRAPH_UP}'))
pop("#k-before", W[42] - 0.05, dx=-180, rot=-6)
pop("#k-after", W[43] - 0.05, dx=180, rot=6)

bars = "".join(f'<i class="{"gap" if k in (2, 3, 6, 7) else ""}" style="height:{h}px"></i>'
               for k, h in enumerate([50, 110, 10, 10, 80, 140, 10, 10, 100, 60, 120]))
deck("d-cut", sections[5], sections[6],
     card("k-cut", 190, 10, 700, 380, -3, f'<span class="label">2 · zéro blanc</span><div class="bars" id="bars">{bars}</div>'))
pop("#k-cut", sections[5] + 0.05, dy=160, rot=-4)
js.append(f'  tl.to("#bars .gap", {{scaleX: 0, duration: 0.35, ease: "power3.in"}}, {W[49]:.3f});')

deck("d-eng", sections[6], sections[7],
     card("k-num", 90, 30, 300, 340, -8, '<span class="label">étape</span><span class="value" style="font-size:180px">3</span>')
     + card("k-com", 400, 0, 330, 360, 4, '<span class="label">commentaires</span><span class="value">+128</span>', light=True)
     + card("k-share", 720, 50, 290, 340, 9, '<span class="label">partages</span><span class="value">+54</span>'))
pop("#k-num", sections[6] + 0.05, dx=-150, rot=-8)
pop("#k-com", W[63] - 0.05, dy=180, rot=4)
pop("#k-share", W[66] - 0.05, dx=150, rot=8)


PLANE = '<svg viewBox="0 0 64 64"><path d="M6 30L58 8 44 58 32 36z" style="fill:var(--black)"/></svg>'
cards.append(f'<div class="pill clip" id="cta" data-start="{sections[8] + 0.05:.3f}" data-duration="{SPEECH_END - sections[8] - 0.05:.3f}" data-track-index="3">{PLANE}envoie à un pote</div>')
js.append(f'  tl.from("#cta", {{opacity: 0, y: 60, duration: 0.4, ease: "back.out(1.6)"}}, {sections[8] + 0.05:.3f});')
sfx.append((sections[8] + 0.05, "pop", 0.12, 0.15))

# --------------------------------------------------------------------------- écran de fin
tag = brand.get("tagline")
endcard = (f'<div class="clip" id="endcard" data-start="{SPEECH_END}" data-duration="{DUR - SPEECH_END:.2f}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/>'
           + (f'<div id="tagline">{"<br/>".join(p.strip() + "." for p in tag.rstrip(".").split("."))}</div>' if tag else "")
           + "</div>")
js.append(f'  tl.fromTo("#bloom", {{opacity: 0}}, {{opacity: 0.9, duration: 0.2, immediateRender: false}}, {SPEECH_END - 0.2:.3f});')
js.append(f'  tl.to("#bloom", {{opacity: 0, duration: 0.5}}, {SPEECH_END:.3f});')
js.append(f'  tl.from("#logo", {{opacity: 0, scale: 0.9, duration: 0.7, ease: "power3.out"}}, {SPEECH_END + 0.05:.3f});')
if tag:
    js.append(f'  tl.from("#tagline", {{opacity: 0, y: 30, duration: 0.6, ease: "power3.out"}}, {SPEECH_END + 0.5:.3f});')
sfx.append((SPEECH_END - 0.2, "whoosh", 0.4, 0.22))

sfx_html = [f'<audio id="sfx{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{d}" '
            f'data-volume="{v}" data-track-index="{6 if name == "whoosh" else 7}"></audio>' for n, (t, name, d, v) in enumerate(sfx)]

# --------------------------------------------------------------------------- assemblage
tpl = open(f"{REPO}/templates/reel-editorial/template.html").read()
brand_css = open(f"{BRAND_DIR}/brand.css").read()
os.makedirs(f"{ROOT}/montage/assets/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{ROOT}/montage/assets/brand/logo.png")
shutil.rmtree(f"{ROOT}/montage/assets/brand/fonts", ignore_errors=True)
shutil.copytree(f"{BRAND_DIR}/fonts", f"{ROOT}/montage/assets/brand/fonts")
subject_dur = 26.0
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in brand_css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", f"{DUR}").replace("{{SUBJECT_DUR}}", f"{subject_dur}")
          .replace("{{SOFTEN}}", "block" if SOFTEN else "none")
          .replace("{{BEHIND}}", "\n        ".join(behind))
          .replace("{{CARDS}}", "\n      ".join(cards))
          .replace("{{CAPTIONS}}", "\n      ".join(caps_html))
          .replace("{{ENDCARD}}", endcard)
          .replace("{{SFX}}", "\n    ".join(sfx_html))
          .replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"index.html (éditorial, {BRAND}) : {len(groups)} sous-titres, {len(behind)} titres, {len(cards)} cartes, {len(sfx_html)} sons")
