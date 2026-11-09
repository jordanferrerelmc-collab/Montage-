"""« Utiliser le 4-3-1-2 » — montage dynamique gaming premium (Specimen Gaming), gameplay plein écran.

Vidéo de jeu ralentie à 0,85 (préparée dans assets/game.mp4, 3414 × 1920) et recadrée en vertical
par un panoramique qui suit l'action ; voix de l'utilisateur ; schéma tactique, émojis, sous-titres mot à mot.
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
SPEED, GAME_W = 0.85, 3414
GAME_END = 14.13
MAIN = 15.95
END = 2.3
DUR = round(MAIN + END, 2)

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ gameplay plein écran + panoramique qui suit l'action
# centre de l'action (fraction de la largeur) à chaque seconde de la source
CX = [0.42, 0.48, 0.45, 0.42, 0.42, 0.40, 0.45, 0.52, 0.48, 0.42, 0.36, 0.28, 0.24]
def xpos(c):
    return max(-(GAME_W - 1080), min(0, -(c * GAME_W - 540)))
body.append('<div id="game"><div id="pan"><video id="gv" class="clip" src="assets/game.mp4" data-start="0" '
            f'data-duration="{GAME_END}" data-has-audio="true" data-volume="0.22" data-track-index="0"></video>'
            f'<img id="last" class="clip" src="assets/last.jpg" alt="" data-start="{GAME_END - 0.05:.2f}" data-duration="{MAIN - GAME_END + 0.05:.2f}" data-track-index="1"/></div></div>')
body.append('<div id="vign"></div>')
prev = xpos(CX[0])
for s in range(len(CX) - 1):
    a, b = s / SPEED, min((s + 1) / SPEED, GAME_END)
    nxt = xpos(CX[s + 1])
    js.append(f"  tl.fromTo('#pan', {{x: {prev:.0f}}}, {{x: {nxt:.0f}, duration: {b - a:.3f}, ease: 'sine.inOut', immediateRender: {'true' if s == 0 else 'false'}}}, {a:.3f});")
    prev = nxt
# zoom : poussée lente, coups de zoom sur « erreur », « Boom », « But »
js.append("  tl.fromTo('#game', {scale: 1.0}, {scale: 1.06, duration: 3.3, ease: 'none', immediateRender: true}, 0);")
js.append(f"  tl.fromTo('#game', {{scale: 1.14}}, {{scale: 1.0, duration: 0.9, ease: 'power3.out', immediateRender: false}}, {W[13]:.3f});")
js.append(f"  tl.fromTo('#game', {{scale: 1.0}}, {{scale: 1.04, duration: {13.1 - W[13] - 0.9:.3f}, ease: 'none', immediateRender: false}}, {W[13] + 0.9:.3f});")
js.append("  tl.fromTo('#game', {scale: 1.16}, {scale: 1.08, duration: 1.0, ease: 'power3.out', immediateRender: false}, 13.11);")
# fin du jeu : image floutée sous l'appel à l'action
js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(14px) brightness(0.55)', duration: 0.35, ease: 'power2.out', immediateRender: false}}, {W[42] - 0.1:.3f});")

# ------------------------------------------------------------------ signature + barre de progression
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="tracker"><span class="lbl">TACTIQUE</span>' + "".join(f'<div class="slot" id="slot{i}"></div>' for i in range(3)) + "</div>")
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")
js.append("  fx.blurIn(tl, '.tracker', 0.15, {blur: 8, d: 0.3});")

# ------------------------------------------------------------------ accroche
body.append(f'<div class="clip hook" id="hook" data-start="0" data-duration="{W[11] - 0.05:.2f}" data-track-index="2">'
            '<div class="kicker" id="hk">FC · TACTIQUE</div><div class="htitle" id="ht1">Tu joues en</div>'
            '<div class="htitle big" id="ht2">4-3-1-2</div></div>')
js.append("  fx.blurIn(tl, '#hk', 0.1, {blur: 10});")
js.append("  fx.blurIn(tl, '#ht1', 0.15);")
js.append(f"  fx.blurIn(tl, '#ht2', {W[3]:.2f}, {{blur: 24, scale: 1.2, y: 0}});")
js.append(f"  fx.blurOut(tl, '#hook', {W[11] - 0.35:.2f});")
sfx("whoosh-long", 0.0, 0.3, 1.1); sfx("impact-sec", W[3], 0.35, 0.35)

# ------------------------------------------------------------------ émojis (pop + onde de choc)
def emoji(eid, char, t, end, x, y, size=220, rot=-8):
    body.append(f'<div class="clip emo" id="{eid}" data-start="{t:.2f}" data-duration="{end - t:.2f}" data-track-index="3" '
                f'style="left:{x}px; top:{y}px; font-size:{size}px"><div class="ering" id="{eid}r"></div><span id="{eid}c">{char}</span></div>')
    js.append(f"  tl.fromTo('#{eid}c', {{scale: 0, rotation: {rot * 3}}}, {{scale: 1, rotation: {rot}, duration: 0.45, ease: 'back.out(2.2)', immediateRender: true}}, {t:.3f});")
    js.append(f"  fx.shockwave(tl, '#{eid}r', {t + 0.05:.3f});")
    js.append(f"  fx.blurOut(tl, '#{eid}', {end - 0.25:.3f});")
    sfx("pop", t, 0.3, 0.3)

emoji("e1", "❌", W[12], W[14] - 0.1, 560, 380, 260, -10)           # Grosse erreur !
emoji("e2", "🎯", W[14], W[16] + 0.6, 640, 380, 180, 8)             # Le secret
emoji("e3", "💥", W[40], W[41], 380, 520, 300, -6)                  # Boom !
emoji("e4", "⚽", W[41], W[42] - 0.05, 400, 520, 300, 10)            # But !
sfx("impact-boom", W[40], 0.4, 0.9)
js.append(f"  fx.trackerFill(tl, '#slot0', {W[14]:.2f});")
js.append(f"  fx.trackerFill(tl, '#slot1', {W[27]:.2f});")
js.append(f"  fx.trackerFill(tl, '#slot2', {W[40]:.2f});")

# ------------------------------------------------------------------ schéma tactique : latéraux écartés, puis combinaisons dans l'axe
# 4-3-1-2 vu de haut, attaque vers le haut (x, y en % de la carte)
P = {"G": (50, 92), "DG": (14, 72), "DCG": (38, 77), "DCD": (62, 77), "DD": (86, 72),
     "MG": (24, 55), "MC": (50, 59), "MD": (76, 55), "MOC": (50, 38), "BG": (36, 16), "BD": (64, 16)}
def dot(k, cls=""):
    x, y = P[k]
    return f'<b class="pl {cls}" id="p{k}" style="left:{x}%; top:{y}%"></b>'
pitch = ('<div class="pitch"><i class="mid"></i><i class="circ"></i><i class="box top"></i><i class="box bot"></i>'
         '<svg class="arrows" viewBox="0 0 100 100" preserveAspectRatio="none">'
         '<path id="aL" d="M14 70 Q6 50 8 30" pathLength="1"/><path id="aR" d="M86 70 Q94 50 92 30" pathLength="1"/>'
         '<path id="c1" d="M50 38 L36 16" pathLength="1"/><path id="c2" d="M36 16 L64 16" pathLength="1"/><path id="c3" d="M64 16 L50 38" pathLength="1"/>'
         '</svg>' + "".join(dot(k, "acc" if k in ("BG", "BD", "MOC") else "") for k in P) + "</div>")
CARD_A, CARD_B = W[14] - 0.05, W[40] - 0.15
body.append(f'<div class="clip tcard" id="tc" data-start="{CARD_A:.2f}" data-duration="{CARD_B - CARD_A:.2f}" data-track-index="2">'
            f'<div class="tlab" id="tl1">1 · ÉCARTE</div><div class="tlab" id="tl2">2 · REVIENS DANS L\'AXE</div>{pitch}</div>')
js.append(f"  fx.slideBlur(tl, '#tc', {CARD_A:.2f}, {{x: -80}});")
sfx("whoosh-court", CARD_A, 0.22, 0.6)
js.append(f"  fx.blurIn(tl, '#tl1', {CARD_A + 0.2:.2f}, {{blur: 8}});")
js.append(f"  tl.fromTo('.pitch .pl', {{scale: 0}}, {{scale: 1, duration: 0.3, ease: 'back.out(3)', stagger: 0.03, immediateRender: true}}, {CARD_A + 0.25:.2f});")
lat = W[22]                                                      # « latéraux »
js.append(f"  tl.fromTo('#pDG', {{x: 0, y: 0}}, {{x: -34, y: -213, duration: 0.9, ease: 'power2.inOut', immediateRender: false}}, {lat:.2f});")
js.append(f"  tl.fromTo('#pDD', {{x: 0, y: 0}}, {{x: 34, y: -213, duration: 0.9, ease: 'power2.inOut', immediateRender: false}}, {lat:.2f});")
js.append(f"  tl.fromTo('#aL, #aR', {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.7, ease: 'power2.out', immediateRender: true}}, {lat - 0.1:.2f});")
js.append(f"  tl.fromTo('#pDG, #pDD', {{backgroundColor: 'var(--ink)'}}, {{backgroundColor: 'var(--accent)', duration: 0.2, immediateRender: false}}, {lat:.2f});")
sfx("clic", lat, 0.3, 0.1)
axe = W[27]                                                      # « Ensuite, tu reviens dans l'axe »
js.append(f"  fx.blurOut(tl, '#tl1', {axe - 0.2:.2f});")
js.append(f"  fx.blurIn(tl, '#tl2', {axe:.2f}, {{blur: 8}});")
js.append(f"  tl.to('#aL, #aR', {{opacity: 0, duration: 0.25}}, {axe:.2f});")
combo = W[32]                                                    # « combinaisons »
for n, k in enumerate(("c1", "c2", "c3")):
    js.append(f"  tl.fromTo('#{k}', {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.35, ease: 'power2.out', immediateRender: true}}, {combo + n * 0.4:.2f});")
    sfx("clic", combo + n * 0.4, 0.28, 0.1)
js.append(f"  tl.fromTo('#pMOC', {{scale: 1}}, {{scale: 1.5, duration: 0.25, yoyo: true, repeat: 1, immediateRender: false}}, {W[36]:.2f});")
js.append(f"  fx.blurOut(tl, '#tc', {CARD_B - 0.3:.2f});")

# ------------------------------------------------------------------ appel à l'action
body.append(f'<div class="clip pill" id="cta" data-start="{W[42] - 0.05:.2f}" data-duration="{MAIN - W[42] + 0.05:.2f}" data-track-index="3">'
            '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>Abonne-toi</div>')
js.append(f"  fx.blurIn(tl, '#cta', {W[42] - 0.05:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("ding", W[42], 0.22, 0.7)

# ------------------------------------------------------------------ sous-titres mot à mot (mots clés en rouge)
fix = {17: "d'écarter", 33: "rapides", 40: "BOOM !", 41: "BUT !"}
keys = {3, 11, 13, 15, 22, 26, 31, 32, 36, 39, 40, 41, 42}
glue = {"tu", "en", "et", "tes", "dans", "le", "la", "c'est", "avec", "pour", "des", "ton", "entre"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]$", "", words[i]["text"]))
groups, cur = [], []
for i in range(len(words)):
    cur.append(i)
    if txt(i).lower() in glue and len(cur) < 3 and i + 1 < len(words):
        continue
    groups.append(cur); cur = []
if cur: groups.append(cur)
skip = set(range(0, 4))                                         # l'accroche affiche déjà « Tu joues en 4-3-1-2 »
k = 0
for gi, g in enumerate(groups):
    if all(i in skip for i in g):
        continue
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[gi + 1][0]] - 0.04) if gi + 1 < len(groups) else MAIN
    label = " ".join(f"<span class='k'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    body.append(f'<div class="cap clip" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="4">{label}</div>')
    js.append(f"  fx.blurIn(tl, '#c{k}', {a:.2f}, {{blur: 10, y: 14, d: 0.18}});")
    k += 1

# ------------------------------------------------------------------ voix + écran de fin
audio.append(("../voix", 0.0, 1.0, 15.8))
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {MAIN - 0.3:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.5)

aud, tracks = [], {}
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t); tr = 6
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    src = "assets/voix.wav" if name == "../voix" else f"assets/sfx/{name}.wav"
    aud.append(f'<audio id="a{n}" class="clip" src="{src}" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

EXTRA_CSS = """
      /* zones sûres TikTok (charte gaming) : rien sous les onglets du haut, ni dans la colonne d'icônes, ni dans la description */
      .handle { top: 200px; } .tracker { top: 245px; }
      .cap { top: var(--cap-top); left: var(--cap-left); width: var(--cap-width); }
      #game { position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 45%; }
      #pan { position: absolute; left: 0; top: 0; width: 3414px; height: 1920px; }
      #pan video, #pan img { position: absolute; left: 0; top: 0; width: 3414px; height: 1920px; }
      #vign { position: absolute; inset: 0; pointer-events: none; z-index: 0;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.35) 30%, rgba(0, 0, 0, 0) 45%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.7) 100%); }
      .hook { position: absolute; left: 70px; top: 360px; width: 840px; }
      .htitle { font-weight: 700; font-size: 96px; letter-spacing: -0.03em; line-height: 0.95; text-shadow: 0 4px 0 rgba(0, 0, 0, 0.55), 0 6px 30px rgba(0, 0, 0, 0.85); }
      .htitle.big { font-size: 230px; color: var(--accent-soft); letter-spacing: -0.05em; }
      .emo { position: absolute; line-height: 1; z-index: 5; }
      .emo span { display: inline-block; filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.6)); }
      .ering { position: absolute; left: 50%; top: 50%; width: 360px; height: 360px; margin: -180px 0 0 -180px; border-radius: 50%;
        border: 6px solid var(--accent); opacity: 0; }
      .tcard { position: absolute; left: 50px; top: 330px; width: 470px; padding: 24px; border-radius: 30px; border: 3px solid var(--accent);
        background: rgba(28, 29, 33, 0.82); box-shadow: 0 0 40px rgba(218, 61, 57, 0.4), 0 30px 70px rgba(0, 0, 0, 0.6); }
      .tlab { position: absolute; left: 24px; top: 22px; font-weight: 700; font-size: 32px; letter-spacing: 0.06em; color: var(--accent-soft); }
      .pitch { position: relative; margin-top: 56px; width: 422px; height: 560px; border-radius: 18px; border: 2px solid var(--silver);
        background: rgba(0, 0, 0, 0.25); overflow: hidden; }
      .pitch i { position: absolute; border: 2px solid var(--silver); opacity: 0.45; }
      .pitch .mid { left: 0; right: 0; top: 50%; height: 0; border-width: 2px 0 0 0; }
      .pitch .circ { left: 50%; top: 50%; width: 120px; height: 120px; margin: -60px; border-radius: 50%; }
      .pitch .box { left: 25%; width: 50%; height: 15%; }
      .pitch .box.top { top: -2px; } .pitch .box.bot { bottom: -2px; }
      .pitch .pl { position: absolute; width: 34px; height: 34px; margin: -17px 0 0 -17px; border-radius: 50%; background: var(--ink);
        box-shadow: 0 0 0 4px var(--charcoal-deep); }
      .pitch .pl.acc { background: var(--accent); }
      .arrows { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
      .arrows path { fill: none; stroke: var(--accent-soft); stroke-width: 1.6; stroke-dasharray: 1; stroke-dashoffset: 1;
        stroke-linecap: round; vector-effect: non-scaling-stroke; }
      .arrows path { stroke-width: 6px; }
      .pill { position: absolute; left: 50%; top: 820px; transform: translateX(-50%); display: flex; align-items: center; gap: 20px;
        white-space: nowrap; padding: 30px 56px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 70px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill svg { width: 70px; height: 70px; }
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
tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()) + EXTRA_CSS)
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"4-3-1-2 jeu : {DUR} s, {len(body)} blocs, {len(aud)} sons")
