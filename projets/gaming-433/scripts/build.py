"""« La 4-3-3 qui ne perd plus » — TikTok Specimen Gaming, voix et script de l'utilisateur.

assets/plans.mp4 (scripts/track.py puis scripts/prep.py) : 8 plans verticaux (zones utiles des menus
agrandies sur l'écran flouté). Sous-titres centrés mot à mot, transitions « zoom à travers », coups de zoom sur les
chiffres, titres en haut sous la signature (jamais sur les sous-titres, pas de barre de progression).
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
PLANS = json.load(open(f"{ROOT}/scripts/plans.json"))
STARTS = [0.0]
for p in PLANS:
    STARTS.append(round(STARTS[-1] + p[-1], 2))          # débuts des plans + fin
MAIN = STARTS[-1]                                        # 39.0
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
events = []
def punch(t, z=1.14, hold=0.9):
    events.append((t, t + hold, z, 1.0, "power3.out"))
def through(t, zin=2.4):
    """Transition « zoom à travers » : on plonge dans l'image, la suivante arrive déjà zoomée et se pose."""
    events.append((t - 0.26, t, 1.0, zin, "power3.in")); events.append((t, t + 0.45, zin * 0.9, 1.0, "power3.out"))
    js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px)'}}, {{filter: 'blur(14px)', duration: 0.24, ease: 'power2.in', immediateRender: false}}, {t - 0.26:.3f});")
    js.append(f"  tl.fromTo('#game', {{filter: 'blur(14px)'}}, {{filter: 'blur(0px)', duration: 0.34, ease: 'power2.out', immediateRender: false}}, {t:.3f});")
    sfx("whoosh-court", t - 0.2, 0.2, 0.6)

punch(0.0, 1.14, 0.6)
SOFT = {1}                                               # même écran : simple coup de zoom
for k in range(1, len(PLANS)):
    if k in SOFT:
        punch(STARTS[k], 1.2, 0.7); sfx("clic", STARTS[k], 0.3, 0.1)
    else:
        through(STARTS[k])
punch(W[2], 1.2)            # 4-3-3
punch(W[13], 1.18, 0.6)     # but sur but
punch(W[25], 1.14, 0.6)     # équilibrée
punch(W[29], 1.26)          # 40
punch(W[34], 1.22)          # ne passe
punch(W[40], 1.2)           # copie-le
sfx("impact-sec", W[2], 0.32, 0.35); sfx("impact-boom", W[29], 0.36, 0.9); sfx("ding", W[40], 0.22, 0.7)

events.sort()
for n, (a, b, z0, z1, ease) in enumerate(events):
    if n + 1 < len(events):
        b = min(b, events[n + 1][0])                     # jamais deux zooms en même temps
    if b - a < 0.05:
        continue
    js.append(f"  tl.fromTo('#game', {{scale: {z0:.3f}}}, {{scale: {z1:.3f}, duration: {b - a:.3f}, ease: '{ease}', immediateRender: {'true' if n == 0 else 'false'}}}, {a:.3f});")


# ------------------------------------------------------------------ signature (pas de barre de progression)
body.append('<div class="handle">SPECIMEN GAMING</div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")

# ------------------------------------------------------------------ titres en haut (pastille + ligne), centrés
LABELS = [
    (0.0, STARTS[1], "FC 27 · TACTIQUE", "<span class='xl'>LA <b>4-3-3</b></span><br/>QUI NE PERD PLUS"),
    (STARTS[1], STARTS[2], "AVANT", "But sur but…"),
    (STARTS[2], STARTS[3], "ALORS", "J'ai <b>tout changé</b>"),
    (STARTS[3], STARTS[4], "EN POINTE", "<b>Fausse 9</b>"),
    (STARTS[4], STARTS[5], "LE JEU", "<span class='sm'>Passes <b>courtes</b> · <b>Équilibrée</b></span>"),
    (STARTS[5], STARTS[6], "RÉGLAGE", "<span class='xl'>LIGNE : <b>40</b></span>"),
    (STARTS[6], STARTS[7], "RÉSULTAT", "Plus personne <b>ne passe</b>"),
    (STARTS[7], MAIN, "LE CODE", "CODE 👇 <b>COPIE-LE</b>"),
]
for n, (a, b, small, big) in enumerate(LABELS):
    a0 = a + (0.2 if a else 0.05)
    body.append(f'<div class="clip plabel" id="pl{n}" data-start="{a0:.2f}" data-duration="{b - a0:.2f}" data-track-index="2">'
                f'<div class="ps">{small}</div><div class="pb">{big}</div></div>')
    js.append(f"  fx.blurIn(tl, '#pl{n}', {a0 + 0.05:.2f}, {{blur: 14, y: -20, d: 0.3}});")
    js.append(f"  fx.blurOut(tl, '#pl{n}', {b - 0.3:.2f}, {{d: 0.25}});")
sfx("whoosh-long", 0.0, 0.28, 1.1)

# ------------------------------------------------------------------ le code en grand + appel à l'action (au-dessus des sous-titres)
CODE = "zAMddZP99@BS"
ca = STARTS[7] + 0.5
body.append(f'<div class="clip bigcode" id="code" data-start="{ca:.2f}" data-duration="{MAIN - ca:.2f}" data-track-index="3">{html.escape(CODE)}</div>')
js.append(f"  fx.blurIn(tl, '#code', {ca:.2f}, {{blur: 16, scale: 1.2, y: 0, d: 0.35}});")
sfx("pop", ca, 0.25, 0.12)
cb = W[41] - 0.05
body.append(f'<div class="clip pill" id="cta" data-start="{cb:.2f}" data-duration="{MAIN - cb:.2f}" data-track-index="3">'
            '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>Abonne-toi</div>')
js.append(f"  fx.blurIn(tl, '#cta', {cb:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("pop", cb, 0.25, 0.12)

# ------------------------------------------------------------------ sous-titres mot à mot, centrés, mots clés en rouge
fix = {2: "4-3-3", 7: "perdre", 19: "9", 22: "Passes", 23: "courtes,", 29: "40", 30: "Résultat ?", 40: "Copie-le"}
keys = {2, 5, 7, 11, 13, 16, 17, 18, 19, 23, 25, 26, 28, 29, 32, 34, 36, 40, 41}
glue = {"cette", "m'a", "fait", "de", "je", "sur", "alors", "j'ai", "tout", "en", "plus", "ne", "le", "est", "à", "pour", "la", "fausse"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]$", "", words[i]["text"]))
groups, cur_g = [], []
for i in range(len(words)):
    if txt(i) == "":
        continue
    cur_g.append(i)
    joined = " ".join(txt(k) for k in cur_g)
    if txt(i).lower() in glue and len(cur_g) < 3 and len(joined) < 14 and i + 1 < len(words):
        continue
    groups.append(cur_g); cur_g = []
if cur_g: groups.append(cur_g)
for k, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else MAIN
    label = " ".join(f"<span class='k'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    body.append(f'<div class="cap clip" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="4">{label}</div>')
    js.append(f"  tl.fromTo('#c{k}', {{opacity: 0, scale: 1.25, filter: 'blur(8px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.16, ease: 'back.out(2)', immediateRender: true}}, {a:.3f});")

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.25, immediateRender: false}}, {MAIN - 0.25:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.35)

EXTRA_CSS = """
      #game { position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 47%; }
      #game video { position: absolute; inset: 0; width: 1080px; height: 1920px; }
      #vign { position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.62) 0%, rgba(0, 0, 0, 0.3) 22%, rgba(0, 0, 0, 0) 34%, rgba(0, 0, 0, 0) 64%, rgba(0, 0, 0, 0.55) 80%, rgba(0, 0, 0, 0.35) 100%); }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6); }
      /* titres : centrés, en haut, loin des sous-titres */
      .plabel { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 258px; text-align: center; }
      .ps { display: inline-block; padding: 8px 22px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 30px;
        letter-spacing: 0.16em; color: var(--ink); }
      .pb { margin-top: 14px; font-weight: 700; font-size: 74px; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink); white-space: nowrap;
        -webkit-text-stroke: 10px rgba(0, 0, 0, 0.85); paint-order: stroke fill; }
      .pb b { color: var(--accent-soft); }
      .pb .xl { font-size: 126px; letter-spacing: -0.04em; line-height: 1; -webkit-text-stroke: 14px rgba(0, 0, 0, 0.85); paint-order: stroke fill; }
      .pb .sm { font-size: 58px; }
      .pb { font-size: 68px; }
      .bigcode { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 1090px; text-align: center; font-weight: 700; font-size: 112px;
        letter-spacing: 0.01em; color: var(--ink); -webkit-text-stroke: 14px var(--accent); paint-order: stroke fill; text-shadow: 0 10px 40px rgba(0, 0, 0, 0.8); }
      /* sous-titres centrés, zone sûre TikTok, contour noir */
      #root .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      #root .cap .k { margin: 0; }
      .pill { position: absolute; left: 50%; top: 540px; transform: translateX(-50%); display: flex; align-items: center; gap: 20px;
        white-space: nowrap; padding: 28px 48px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 60px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill svg { width: 60px; height: 60px; }
"""

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx", ignore=shutil.ignore_patterns("reactions"))
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")

def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
aud, tracks = ['<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="17.55" data-volume="1" data-track-index="6"></audio>'], {}
REACT = f"{REPO}/effets/sfx/reactions/foule-acclame-court.wav"
if os.path.exists(REACT):                # non versionné (licence Mixkit) ; assets/*.wav est ignoré par git
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REACT, "-t", "2.6", "-af", "afade=t=in:d=0.1,afade=t=out:st=1.8:d=0.8", f"{A}/reaction.wav"], check=True)
    aud.append(f'<audio id="react" class="clip" src="assets/reaction.wav" data-start="{W[34]:.2f}" data-duration="2.6" data-volume="0.3" data-track-index="12"></audio>')
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
print(f"4-3-3 : {DUR} s, {len(groups)} sous-titres, {len(aud)} sons")
