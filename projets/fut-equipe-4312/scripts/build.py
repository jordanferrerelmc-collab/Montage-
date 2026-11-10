"""« Équipe originale ? Encore le 4-3-1-2 » — TikTok gaming (Specimen Gaming), plein écran dynamique.

assets/plans.mp4 (scripts/prep.sh) : 6 plans verticaux tirés de la capture, calés sur la voix de l'utilisateur.
Sous-titres centrés, émojis, coups de zoom sur les coupes, gros zoom sur le « 4-3-1-2 » du panneau adverse.
"""
import html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
words = json.load(open(f"{ROOT}/src/transcript.json"))
W = [w["start"] for w in words]
CUTS = [0.0, 2.05, 4.40, 5.40, 7.10, 8.50]      # débuts des plans (voir prep.sh)
VID_END = 10.52
MAIN = 10.75
END = 2.3
DUR = round(MAIN + END, 2)
ZOOM_ORIGIN = "446px 971px"                       # position du texte « 4-3-1-2 » dans le plan 4

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ vidéo plein écran
body.append(f'<div id="game"><video id="gv" class="clip" src="assets/plans.mp4" data-start="0" data-duration="{VID_END}" '
            'data-has-audio="true" data-volume="0.25" data-track-index="0"></video></div>')
body.append('<div id="vign"></div>')

# coupes : coup de zoom + léger flou de mouvement (pas de flash), whoosh discret
for k, t in enumerate(CUTS):
    nxt = CUTS[k + 1] if k + 1 < len(CUTS) else VID_END
    if k == 3:
        continue                                   # plan du panneau : zoom dédié plus bas
    js.append(f"  tl.set('#game', {{transformOrigin: '50% 45%'}}, {t:.3f});")
    js.append(f"  tl.fromTo('#game', {{scale: 1.12}}, {{scale: 1.0, duration: 0.35, ease: 'power3.out', immediateRender: {'true' if k == 0 else 'false'}}}, {t:.3f});")
    js.append(f"  tl.fromTo('#game', {{scale: 1.0}}, {{scale: 1.05, duration: {nxt - t - 0.35:.3f}, ease: 'none', immediateRender: false}}, {t + 0.35:.3f});")
    if k:
        js.append(f"  tl.fromTo('#game', {{filter: 'blur(10px)'}}, {{filter: 'blur(0px)', duration: 0.18, ease: 'power2.out', immediateRender: false}}, {t:.3f});")
        sfx("whoosh-court", t - 0.08, 0.18, 0.5)

# zoom sur le « 4-3-1-2 » : approche lente puis coup de zoom sur le mot
a, b = CUTS[3], CUTS[4]
js.append(f"  tl.set('#game', {{transformOrigin: '{ZOOM_ORIGIN}'}}, {a:.3f});")
js.append(f"  tl.fromTo('#game', {{scale: 1.0}}, {{scale: 1.45, duration: {W[17] - a:.3f}, ease: 'power1.inOut', immediateRender: false}}, {a:.3f});")
js.append(f"  tl.fromTo('#game', {{filter: 'blur(10px)'}}, {{filter: 'blur(0px)', duration: 0.18, ease: 'power2.out', immediateRender: false}}, {a:.3f});")
js.append(f"  tl.fromTo('#game', {{scale: 2.6}}, {{scale: 2.2, duration: 0.5, ease: 'power3.out', immediateRender: false}}, {W[17]:.3f});")
js.append(f"  tl.fromTo('#game', {{scale: 2.2}}, {{scale: 2.3, duration: {b - W[17] - 0.5:.3f}, ease: 'none', immediateRender: false}}, {W[17] + 0.5:.3f});")
sfx("whoosh-court", a - 0.08, 0.18, 0.5)
sfx("impact-boom", W[17], 0.4, 0.9)
body.append(f'<div class="clip zring" id="zr" data-start="{W[17]:.2f}" data-duration="0.8" data-track-index="2"></div>')
js.append(f"  fx.shockwave(tl, '#zr', {W[17]:.3f});")

# ------------------------------------------------------------------ signature + barre de progression (sous les onglets TikTok)
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append(f'<div class="bar"><i id="barfill"></i></div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")
js.append(f"  tl.fromTo('#barfill', {{scaleX: 0}}, {{scaleX: 1, duration: {MAIN:.2f}, ease: 'none', immediateRender: true}}, 0);")

# ------------------------------------------------------------------ émojis
def emoji(eid, char, t, end, y, size=230, rot=-8):
    body.append(f'<div class="clip emo" id="{eid}" data-start="{t:.2f}" data-duration="{end - t:.2f}" data-track-index="3" '
                f'style="top:{y}px; font-size:{size}px"><div class="ering" id="{eid}r"></div><span id="{eid}c">{char}</span></div>')
    js.append(f"  tl.fromTo('#{eid}c', {{scale: 0, rotation: {rot * 3}}}, {{scale: 1, rotation: {rot}, duration: 0.42, ease: 'back.out(2.2)', immediateRender: true}}, {t:.3f});")
    js.append(f"  fx.shockwave(tl, '#{eid}r', {t + 0.04:.3f});")
    js.append(f"  fx.blurOut(tl, '#{eid}', {end - 0.22:.3f});")
    sfx("pop", t, 0.28, 0.12)

emoji("e1", "🤨", W[1], CUTS[1] - 0.05, 330, 240, -8)        # c'est quoi ça ?
emoji("e2", "👀", W[5], CUTS[2] - 0.05, 1100, 220, 6)         # une équipe originale
emoji("e3", "😤", W[11], CUTS[3] - 0.05, 1120, 240, -6)       # ah bah non !
emoji("e4", "🤦", W[17] + 0.15, CUTS[4] - 0.05, 300, 230, 8)  # encore ce foutu 4-3-1-2
emoji("e5", "🔁", W[19], CUTS[5] - 0.05, 300, 200, -6)        # les mêmes joueurs
emoji("e6", "🤡", W[29], MAIN, 330, 260, 8)                   # sur le même compte ou quoi ?

# ------------------------------------------------------------------ sous-titres mot à mot, centrés, mots clés en rouge
fix = {3: "ça ?", 10: "Champions ?", 13: "non !", 21: "joueurs !", 31: "quoi ?"}
keys = {6, 8, 10, 13, 16, 17, 20, 21, 28, 29}
glue = {"c'est", "une", "en", "de", "ah", "ce", "avec", "les", "mais", "vous", "sur", "le", "ou"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]$", "", words[i]["text"]))
groups, cur = [], []
for i in range(len(words)):
    cur.append(i)
    if txt(i).lower() in glue and len(cur) < 3 and i + 1 < len(words):
        continue
    groups.append(cur); cur = []
if cur: groups.append(cur)
for k, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else MAIN
    label = " ".join(f"<span class='k'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    body.append(f'<div class="cap clip" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="4">{label}</div>')
    js.append(f"  tl.fromTo('#c{k}', {{opacity: 0, scale: 1.25, filter: 'blur(8px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.16, ease: 'back.out(2)', immediateRender: true}}, {a:.3f});")

# ------------------------------------------------------------------ voix + écran de fin
audio.append(("voix", 0.0, 1.0, 10.53))
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(16px) brightness(0.5)', duration: 0.25, immediateRender: false}}, {VID_END - 0.25:.2f});")
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.25, immediateRender: false}}, {MAIN - 0.25:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.35)

import wave
def length(name):
    with wave.open(f"{ROOT}/montage/assets/{'voix' if name == 'voix' else 'sfx/' + name}.wav") as w:
        return w.getnframes() / w.getframerate()

EXTRA_CSS = """
      #game { position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 45%; }
      #game video { position: absolute; inset: 0; width: 1080px; height: 1920px; }
      #vign { position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.55) 0%, rgba(0, 0, 0, 0) 18%, rgba(0, 0, 0, 0) 60%, rgba(0, 0, 0, 0.55) 82%, rgba(0, 0, 0, 0.3) 100%); }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; }
      .bar { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 250px; height: 8px; border-radius: 99px; background: rgba(255, 255, 255, 0.18); overflow: hidden; }
      .bar i { display: block; height: 100%; background: var(--accent); transform-origin: 0 50%; }
      /* sous-titres centrés, zone sûre TikTok */
      .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px; text-shadow: 0 4px 0 rgba(0, 0, 0, 0.6), 0 6px 26px rgba(0, 0, 0, 0.9); }
      .cap .k { margin: 0; }
      .emo { position: absolute; left: var(--cap-left); width: var(--cap-width); text-align: center; line-height: 1; z-index: 5; }
      .emo span { display: inline-block; filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.6)); }
      .ering { position: absolute; left: 50%; top: 50%; width: 360px; height: 360px; margin: -180px 0 0 -180px; border-radius: 50%;
        border: 6px solid var(--accent); opacity: 0; }
      .zring { position: absolute; left: 50%; top: 940px; width: 700px; height: 700px; margin: -350px 0 0 -350px; border-radius: 50%;
        border: 8px solid var(--accent); box-shadow: 0 0 40px rgba(218, 61, 57, 0.6); opacity: 0; }
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

aud, tracks = [], {}
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t); tr = 6; d = round(min(d, length(name)), 3)
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    src = "assets/voix.wav" if name == "voix" else f"assets/sfx/{name}.wav"
    aud.append(f'<audio id="a{n}" class="clip" src="{src}" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()) + EXTRA_CSS)
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"équipe 4-3-1-2 : {DUR} s, {len(groups)} sous-titres, {len(aud)} sons")
