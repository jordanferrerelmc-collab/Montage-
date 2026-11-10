"""« 4-3-1-2 : tu galères à marquer ? » — TikTok Specimen Gaming, gameplay plein écran + voix de l'utilisateur.

assets/plans.mp4 (scripts/track.py puis scripts/prep.py) : 9 plans verticaux qui suivent le joueur contrôlé.
Sous-titres centrés mot à mot, transitions « zoom à travers » entre les parties, coups de zoom sur les mots forts,
titres de partie sous la barre de progression (jamais sur les sous-titres).
"""
import html, json, os, re, shutil, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
words = json.load(open(f"{ROOT}/src/transcript.json"))
W = [w["start"] for w in words]
HOOK_CUTS = [1.25, 2.63, 4.40]                 # coupes rapides de l'accroche
PARTS = [5.83, 10.24, 18.44, 27.36]            # débuts des 4 parties (voir scripts/plans.json)
FREEZE = 34.27                                 # image figée pour l'appel à l'action
MAIN = 38.0
END = 2.3
DUR = round(MAIN + END, 2)

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ vidéo plein écran
body.append(f'<div id="game"><video id="gv" class="clip" src="assets/plans.mp4" data-start="0" data-duration="{MAIN}" '
            'data-has-audio="true" data-volume="0.2" data-track-index="0"></video></div>')
body.append('<div id="vign"></div>')

# zoom : fenêtres qui ne se chevauchent pas, chaque tween a un départ explicite (rendu déterministe)
events = []                                    # (début, fin, de, à, ease)
def punch(t, z=1.14, hold=0.9):
    """Coup de zoom sec à t, qui se relâche."""
    events.append((t, t + hold, z, 1.0, "power3.out"))
def through(t, zin=2.4):
    """Transition « zoom à travers » : on plonge dans l'image, la suivante arrive déjà zoomée et se pose."""
    events.append((t - 0.26, t, 1.0, zin, "power3.in")); events.append((t, t + 0.45, zin * 0.9, 1.0, "power3.out"))
    js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px)'}}, {{filter: 'blur(14px)', duration: 0.24, ease: 'power2.in', immediateRender: false}}, {t - 0.26:.3f});")
    js.append(f"  tl.fromTo('#game', {{filter: 'blur(14px)'}}, {{filter: 'blur(0px)', duration: 0.34, ease: 'power2.out', immediateRender: false}}, {t:.3f});")
    sfx("whoosh-court", t - 0.2, 0.22, 0.6)

punch(0.0, 1.14, 0.6)
for t in HOOK_CUTS:
    punch(t, 1.18, 0.8); sfx("whoosh-court", t - 0.06, 0.14, 0.4)
for t in PARTS:
    through(t)
punch(W[27], 1.18)          # l'espace
punch(W[35], 1.2)           # L1 + triangle
punch(W[42], 1.16)          # profondeur
punch(W[56], 1.2)           # très mal
punch(W[66], 1.2)           # patience
punch(W[82], 1.16)          # décalage
punch(W[89], 1.2)           # R1 + X
punch(W[100], 1.35, 1.6)    # BOOM
sfx("impact-sec", W[56], 0.26, 0.35); sfx("impact-boom", W[100], 0.45, 0.9); sfx("ding", W[104], 0.2, 0.7)

events.sort()
for n, (a, b, z0, z1, ease) in enumerate(events):
    if n + 1 < len(events):
        b = min(b, events[n + 1][0])           # jamais deux zooms en même temps
    if b - a < 0.05:
        continue
    js.append(f"  tl.fromTo('#game', {{scale: {z0:.3f}}}, {{scale: {z1:.3f}, duration: {b - a:.3f}, ease: '{ease}', immediateRender: {'true' if n == 0 else 'false'}}}, {a:.3f});")

# image figée floutée sous l'appel à l'action
js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(14px) brightness(0.5)', duration: 0.4, ease: 'power2.out', immediateRender: false}}, {W[105] - 0.15:.3f});")

# ------------------------------------------------------------------ signature + barre de progression
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="bar"><i id="barfill"></i></div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")
js.append(f"  tl.fromTo('#barfill', {{scaleX: 0}}, {{scaleX: 1, duration: {MAIN:.2f}, ease: 'none', immediateRender: true}}, 0);")

# ------------------------------------------------------------------ accroche + titres de partie (en haut, sous la barre)
body.append(f'<div class="clip hook" id="hook" data-start="0" data-duration="{PARTS[0] - 0.1:.2f}" data-track-index="2">'
            '<div class="hk" id="hk">FC 27 · TACTIQUE</div><div class="hbig" id="hbig">4-3-1-2</div></div>')
js.append("  fx.blurIn(tl, '#hk', 0.1, {blur: 10});")
js.append(f"  fx.blurIn(tl, '#hbig', {W[3]:.2f}, {{blur: 24, scale: 1.25, y: 0}});")
js.append(f"  fx.blurOut(tl, '#hook', {PARTS[0] - 0.4:.2f});")
sfx("whoosh-long", 0.0, 0.28, 1.1); sfx("impact-sec", W[3], 0.3, 0.35)

TRI = '<svg viewBox="0 0 24 24"><path d="M12 4 L21 20 H3 Z" fill="none" style="stroke:var(--ink)" stroke-width="2.6" stroke-linejoin="round"/></svg>'
CROSS = '<svg viewBox="0 0 24 24"><path d="M5 5 L19 19 M19 5 L5 19" style="stroke:var(--ink)" stroke-width="2.8" stroke-linecap="round"/></svg>'
key = lambda t: f'<span class="key">{t}</span>'
LABELS = [
    (PARTS[0], PARTS[1], "ASTUCE 1", "Appel dirigé du piston"),
    (PARTS[1], PARTS[2], "ASTUCE 2", f'{key("L1")}<i>+</i>{key(TRI)}'),
    (PARTS[2], PARTS[3], "LE SECRET", "La patience"),
    (PARTS[3], W[105] - 0.1, "LA FINITION", f'{key("R1")}<i>+</i>{key(CROSS)}'),
]
for n, (a, b, small, big) in enumerate(LABELS):
    body.append(f'<div class="clip plabel" id="pl{n}" data-start="{a + 0.2:.2f}" data-duration="{b - a - 0.2:.2f}" data-track-index="2">'
                f'<div class="ps">{small}</div><div class="pb">{big}</div></div>')
    js.append(f"  fx.blurIn(tl, '#pl{n}', {a + 0.25:.2f}, {{blur: 14, y: -20, d: 0.35}});")
    js.append(f"  fx.blurOut(tl, '#pl{n}', {b - 0.35:.2f});")

# ------------------------------------------------------------------ appel à l'action
body.append(f'<div class="clip pill" id="cta" data-start="{W[105] - 0.05:.2f}" data-duration="{MAIN - W[105] + 0.05:.2f}" data-track-index="3">'
            '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--ink)"/></svg>Enregistre + abonne-toi</div>')
js.append(f"  fx.blurIn(tl, '#cta', {W[105] - 0.05:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("pop", W[105], 0.25, 0.12)

# ------------------------------------------------------------------ sous-titres mot à mot, centrés, mots clés en rouge
fix = {8: "marquer ?", 16: "dernière !", 35: "L1 + triangle", 53: "là,", 90: "+", 91: "X au", 100: "BOOM !", 104: "fond !", 113: "27"}
keys = {3, 8, 16, 20, 21, 24, 27, 32, 33, 35, 42, 48, 56, 57, 61, 63, 66, 78, 82, 89, 90, 98, 100, 104, 105, 109, 112, 113}
glue = {"tu", "en", "mais", "à", "alors", "ces", "la", "un", "de", "mon", "et", "qui", "se", "le", "dès", "que", "je", "dans", "ça", "du",
        "c'est", "les", "pour", "une", "au", "est", "cette", "fc", "très", "+", "r1", "x au"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]$", "", words[i]["text"]))
groups, cur_g = [], []
for i in range(len(words)):
    cur_g.append(i)
    joined = " ".join(txt(k) for k in cur_g)
    if txt(i).lower() in glue and len(cur_g) < 3 and len(joined) < 15 and i + 1 < len(words):
        continue
    groups.append(cur_g); cur_g = []
if cur_g: groups.append(cur_g)
for k, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else MAIN
    label = " ".join(f"<span class='k'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    body.append(f'<div class="cap clip" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="4">{label}</div>')
    js.append(f"  tl.fromTo('#c{k}', {{opacity: 0, scale: 1.25, filter: 'blur(8px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.16, ease: 'back.out(2)', immediateRender: true}}, {a:.3f});")

# ------------------------------------------------------------------ voix + écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.25, immediateRender: false}}, {MAIN - 0.25:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.35)

EXTRA_CSS = """
      #game { position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 46%; }
      #game video { position: absolute; inset: 0; width: 1080px; height: 1920px; }
      #vign { position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.62) 0%, rgba(0, 0, 0, 0.3) 22%, rgba(0, 0, 0, 0) 36%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.55) 80%, rgba(0, 0, 0, 0.35) 100%); }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6); }
      .bar { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 250px; height: 8px; border-radius: 99px; background: rgba(255, 255, 255, 0.25); overflow: hidden; }
      .bar i { display: block; height: 100%; background: var(--accent); transform-origin: 0 50%; }
      /* accroche et titres de partie : centrés, en haut, loin des sous-titres */
      .hook, .plabel { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 300px; text-align: center; }
      .hk, .ps { font-weight: 700; font-size: 36px; letter-spacing: 0.16em; color: var(--ink); text-shadow: 0 3px 14px rgba(0, 0, 0, 0.8); }
      .hbig { font-weight: 700; font-size: 220px; line-height: 1; letter-spacing: -0.05em; color: var(--ink);
        -webkit-text-stroke: 14px var(--accent); paint-order: stroke fill; text-shadow: 0 10px 40px rgba(0, 0, 0, 0.7); }
      .ps { display: inline-block; padding: 8px 22px; border-radius: 999px; background: var(--accent); font-size: 30px; }
      .pb { margin-top: 14px; font-weight: 700; font-size: 68px; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink);
        -webkit-text-stroke: 10px rgba(0, 0, 0, 0.85); paint-order: stroke fill; display: flex; align-items: center; justify-content: center; gap: 18px; }
      .pb i { font-style: normal; }
      .key { display: inline-flex; align-items: center; justify-content: center; min-width: 120px; height: 104px; padding: 0 22px; border-radius: 24px;
        background: var(--charcoal-deep); border: 4px solid var(--accent); font-size: 60px; -webkit-text-stroke: 0; box-shadow: 0 0 30px rgba(218, 61, 57, 0.55); }
      .key svg { width: 62px; height: 62px; }
      /* sous-titres centrés, zone sûre TikTok, contour noir */
      #root .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      #root .cap .k { margin: 0; }
      .pill { position: absolute; left: 50%; top: 820px; transform: translateX(-50%); display: flex; align-items: center; gap: 20px;
        white-space: nowrap; padding: 28px 48px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 60px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill svg { width: 60px; height: 60px; }
"""

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")

def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
aud, tracks = [f'<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="37.95" data-volume="1" data-track-index="6"></audio>'], {}
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t); tr = 7; d = round(min(d, length(name)), 3)
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()) + EXTRA_CSS)
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"explication 4-3-1-2 : {DUR} s, {len(groups)} sous-titres, {len(aud)} sons")
