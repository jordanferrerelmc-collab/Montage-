"""Astuce Rush « Appuyez sur X » — TikTok Specimen Gaming, face caméra dynamique.

assets/cut.mp4 : source sans les blancs (2 s de silence retirés, 4 segments).
Coups de zoom sur les mots forts, sous-titres centrés mot à mot, émojis, bouton « X » animé.
"""
import html, json, os, re, shutil, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
words = json.load(open(f"{ROOT}/work/words_cut.json"))
W = [w["start"] for w in words]
VID_END = 12.17
MAIN = 12.25
END = 2.3
DUR = round(MAIN + END, 2)
JOINS = [7.90, 9.00, 11.25]          # raccords entre les segments (coupes des blancs)

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ vidéo plein écran + zooms
body.append(f'<div id="cam"><video id="v" class="clip" src="assets/cut.mp4" data-start="0" data-duration="{VID_END}" '
            'data-has-audio="true" data-volume="1" data-track-index="0"></video></div>')
body.append('<div id="vign"></div>')
# (instant, zoom d'arrivée) : coups de zoom secs sur les mots forts et sur les raccords, poussée lente entre deux
PUNCH = [(0.0, 1.0), (W[4], 1.18), (W[9], 1.0), (W[13], 1.22), (W[21], 1.08), (JOINS[0], 1.25), (W[29], 1.4),
         (JOINS[1], 1.12), (W[34], 1.32), (JOINS[2], 1.0), (W[36], 1.22)]
for k, (t, z) in enumerate(PUNCH):
    nxt = PUNCH[k + 1][0] if k + 1 < len(PUNCH) else VID_END
    js.append(f"  tl.fromTo('#cam', {{scale: {z * 1.06:.3f}}}, {{scale: {z:.3f}, duration: 0.22, ease: 'power3.out', immediateRender: {'true' if k == 0 else 'false'}}}, {t:.3f});")
    js.append(f"  tl.fromTo('#cam', {{scale: {z:.3f}}}, {{scale: {z * 1.03:.3f}, duration: {max(0.05, nxt - t - 0.22):.3f}, ease: 'none', immediateRender: false}}, {t + 0.22:.3f});")
    if k:
        sfx("whoosh-court", t - 0.06, 0.12, 0.4)

# ------------------------------------------------------------------ signature + barre de progression
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="bar"><i id="barfill"></i></div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")
js.append(f"  tl.fromTo('#barfill', {{scaleX: 0}}, {{scaleX: 1, duration: {MAIN:.2f}, ease: 'none', immediateRender: true}}, 0);")

# ------------------------------------------------------------------ émojis
def emoji(eid, char, t, end, x, y, size=220, rot=-8):
    body.append(f'<div class="clip emo" id="{eid}" data-start="{t:.2f}" data-duration="{end - t:.2f}" data-track-index="3" '
                f'style="left:{x}px; top:{y}px; font-size:{size}px"><div class="ering" id="{eid}r"></div><span id="{eid}c">{char}</span></div>')
    js.append(f"  tl.fromTo('#{eid}c', {{scale: 0, rotation: {rot * 3}}}, {{scale: 1, rotation: {rot}, duration: 0.42, ease: 'back.out(2.2)', immediateRender: true}}, {t:.3f});")
    js.append(f"  fx.shockwave(tl, '#{eid}r', {t + 0.04:.3f});")
    js.append(f"  fx.blurOut(tl, '#{eid}', {end - 0.2:.3f});")
    sfx("pop", t, 0.25, 0.12)

emoji("e1", "💡", W[9], W[12] - 0.05, 730, 400, 190, -8)             # une astuce
emoji("e2", "🏆", W[13], W[17] - 0.05, 110, 420, 200, 8)             # gagner tous vos matchs
emoji("e3", "📈", W[18], W[22] - 0.05, 730, 420, 190, -6)            # beaucoup de points
emoji("e4", "😤", W[34], JOINS[2] - 0.05, 110, 380, 210, 8)          # bordel

# bouton « X » de la manette (dessin original aux couleurs de la charte)
XBTN = ('<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" style="fill:var(--charcoal-deep); stroke:var(--accent)" stroke-width="6"/>'
        '<path d="M32 32 L68 68 M68 32 L32 68" style="stroke:var(--ink)" stroke-width="10" stroke-linecap="round"/></svg>')
xa, xb = W[27], JOINS[1] + 0.9
body.append(f'<div class="clip xbtn" id="xb" data-start="{xa:.2f}" data-duration="{xb - xa:.2f}" data-track-index="3">'
            f'<div class="ering" id="xbr"></div><div id="xbi">{XBTN}</div><div class="xlab" id="xbl">PASSE</div></div>')
js.append(f"  tl.fromTo('#xbi', {{scale: 0, rotation: -40}}, {{scale: 1, rotation: 0, duration: 0.4, ease: 'back.out(2.4)', immediateRender: true}}, {xa:.3f});")
js.append(f"  tl.fromTo('#xbi', {{scale: 1}}, {{scale: 0.82, duration: 0.08, yoyo: true, repeat: 1, ease: 'power2.out', immediateRender: false}}, {W[29]:.3f});")
js.append(f"  fx.shockwave(tl, '#xbr', {W[29]:.3f});")
js.append(f"  fx.blurIn(tl, '#xbl', {W[29] + 0.05:.3f}, {{blur: 8, d: 0.2}});")
js.append(f"  fx.blurOut(tl, '#xb', {xb - 0.2:.3f});")
sfx("clic", W[29], 0.45, 0.1); sfx("impact-sec", W[29] + 0.02, 0.3, 0.35)
sfx("impact-boom", W[34], 0.32, 0.9)

# ------------------------------------------------------------------ sous-titres mot à mot, centrés, mots clés en rouge
fix = {0: "Comment", 1: "", 2: "on dit,", 3: "les", 4: "gars ?", 5: "En", 6: "Rush,", 29: "X,", 30: "faites-moi", 31: "", 34: "bordel,", 36: "passe !"}
keys = {6, 9, 13, 14, 15, 16, 19, 21, 25, 26, 29, 33, 34, 36}
glue = {"comment", "on dit,", "les", "en", "j'ai", "une", "pour", "vos", "et", "de", "c'est", "un", "assez", "sur", "cette", "tous"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]$", "", words[i]["text"]))
groups, cur = [], []
for i in range(len(words)):
    if txt(i) == "":
        continue
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

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#cam', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(16px) brightness(0.5)', duration: 0.25, immediateRender: false}}, {VID_END - 0.25:.2f});")
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.2, immediateRender: false}}, {MAIN - 0.2:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.35)

EXTRA_CSS = """
      #cam { position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 24%; }
      #cam video { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }
      #vign { position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.25) 15%, rgba(0, 0, 0, 0) 24%, rgba(0, 0, 0, 0) 52%, rgba(0, 0, 0, 0.5) 75%, rgba(0, 0, 0, 0.35) 100%); }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6); }
      .bar { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 250px; height: 8px; border-radius: 99px; background: rgba(255, 255, 255, 0.25); overflow: hidden; }
      .bar i { display: block; height: 100%; background: var(--accent); transform-origin: 0 50%; }
      /* sous-titres centrés, sur la poitrine, zone sûre TikTok */
      .cap { display: block; top: 1180px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 86px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      .cap .k { margin: 0; }
      .emo { position: absolute; width: 240px; text-align: center; line-height: 1; z-index: 5; }
      .emo span { display: inline-block; filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.6)); }
      .ering { position: absolute; left: 50%; top: 50%; width: 360px; height: 360px; margin: -180px 0 0 -180px; border-radius: 50%;
        border: 6px solid var(--accent); opacity: 0; }
      .xbtn { position: absolute; left: 110px; width: 260px; top: 380px; height: 320px; text-align: center; z-index: 5; }
      .xbtn #xbi { display: inline-block; width: 210px; height: 210px; filter: drop-shadow(0 0 30px rgba(218, 61, 57, 0.7)); }
      .xbtn #xbi svg { width: 100%; height: 100%; }
      .xlab { font-weight: 700; font-size: 44px; letter-spacing: 0.2em; color: var(--ink); text-shadow: 0 4px 16px rgba(0, 0, 0, 0.8); }
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
aud, tracks = [], {}
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t); tr = 6; d = round(min(d, length(name)), 3)
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
print(f"astuce Rush : {DUR} s, {len(groups)} sous-titres, {len(aud)} sons")
