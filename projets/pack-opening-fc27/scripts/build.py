"""« Pack opening FC 27 : 0 crédit » — TikTok Specimen Gaming, voix de l'utilisateur (src/voix.mp3).

assets/plans.mp4 et assets/voix.wav : scripts/prep.py (13 plans de 0,6 à 1,85 s, 1 s de silence avant la révélation).
Accroche « PACK GRATUIT = ??? » dès la 1re image, étapes drapeau / poste / club, silence + poussée lente sur le logo du
club, puis explosion (impact + foule) sur la carte : « PACK GRATUIT = VEERMAN 85 ».
"""
import html, json, os, re, shutil, subprocess, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
GAP, VCUT = 1.0, 10.90
words = json.load(open(f"{ROOT}/src/transcript.json"))
for w in words:                                   # recale sur la voix avec silence
    if w["start"] >= VCUT:
        w["start"] += GAP; w["end"] += GAP
words[28]["end"] = VCUT                           # « club… » s'arrête avant le silence
W = [w["start"] for w in words]
PLANS = json.load(open(f"{ROOT}/scripts/plans.json"))
CUTS, t = [], 0.0
for p in PLANS:
    CUTS.append(round(t, 3)); t += p[1]
MAIN = round(t, 2)                                # 16.90
END = 2.3
DUR = round(MAIN + END, 2)
T_SIL, T_REV = CUTS[9], CUTS[10]                  # silence (10.90), révélation (11.90)
T_CTA = W[32]

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ vidéo plein écran
body.append(f'<div id="game"><video id="gv" class="clip" src="assets/plans.mp4" data-start="0" data-duration="{MAIN}" '
            'data-has-audio="true" data-volume="0.4" data-track-index="0"></video></div>')
body.append('<div id="vign"></div><div id="dim"></div>')

events = []
def punch(t, z=1.12, hold=0.7):
    events.append((t, t + hold, z, 1.0, "power3.out"))
punch(0.0, 1.16, 0.7)
for k, c in enumerate(CUTS[1:9], 1):              # micro-zoom à chaque coupe (rythme toutes les ~1,5 s)
    punch(c, 1.10 if k % 2 else 1.14, 0.55)
punch(W[26], 1.22, 0.5)                           # « NON »
events.append((T_SIL, T_REV, 1.0, 1.32, "power1.in"))          # silence : poussée lente sur le logo du club
events.append((T_REV, T_REV + 0.7, 1.45, 1.0, "expo.out"))     # explosion
punch(CUTS[11], 1.10, 0.6); punch(CUTS[12], 1.12, 0.6)
events.sort()
for n, (a, b, z0, z1, ease) in enumerate(events):
    if n + 1 < len(events):
        b = min(b, events[n + 1][0])
    if b - a < 0.05:
        continue
    js.append(f"  tl.fromTo('#game', {{scale: {z0:.3f}}}, {{scale: {z1:.3f}, duration: {b - a:.3f}, ease: '{ease}', immediateRender: {'true' if n == 0 else 'false'}}}, {a:.3f});")
# silence : l'image s'assombrit sur les bords ; explosion : défocalisation qui se résout
js.append(f"  tl.fromTo('#dim', {{opacity: 0}}, {{opacity: 1, duration: 0.8, ease: 'power2.in', immediateRender: false}}, {T_SIL:.3f});")
js.append(f"  tl.to('#dim', {{opacity: 0, duration: 0.15, ease: 'power2.out'}}, {T_REV:.3f});")
js.append(f"  tl.fromTo('#game', {{filter: 'blur(18px) brightness(1.6)'}}, {{filter: 'blur(0px) brightness(1)', duration: 0.5, ease: 'power2.out', immediateRender: false}}, {T_REV:.3f});")
js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(14px) brightness(0.5)', duration: 0.3, ease: 'power2.in', immediateRender: false}}, {MAIN - 0.3:.3f});")
body.append(f'<div class="clip" id="wave" data-start="{T_REV:.2f}" data-duration="1.2" data-track-index="1"><div class="ring" id="ring"></div></div>')
js.append(f"  tl.fromTo('#ring', {{opacity: 0.95, scale: 0.2}}, {{opacity: 0, scale: 1.6, duration: 0.9, ease: 'power2.out', immediateRender: false}}, {T_REV:.3f});")

# ------------------------------------------------------------------ signature
body.append('<div class="handle">SPECIMEN GAMING</div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")

# ------------------------------------------------------------------ accroche « PACK GRATUIT = ??? » puis la réponse
body.append(f'<div class="clip plabel" id="hook" data-start="0" data-duration="{CUTS[2] - 0.05:.2f}" data-track-index="2">'
            '<div class="ps">FC 27 · PACK OPENING</div><div class="pb">PACK GRATUIT = <b>???</b></div></div>')
js.append("  fx.blurIn(tl, '#hook', 0.0, {blur: 12, y: -16, d: 0.18});")
js.append(f"  fx.blurOut(tl, '#hook', {CUTS[2] - 0.3:.2f}, {{d: 0.25}});")
body.append(f'<div class="clip plabel" id="answer" data-start="{W[29] + 0.1:.2f}" data-duration="{CUTS[11] - W[29] - 0.1:.2f}" data-track-index="2">'
            '<div class="ps">PACK GRATUIT =</div><div class="pb"><b>VEERMAN 85</b></div></div>')
js.append(f"  fx.blurIn(tl, '#answer', {W[29] + 0.1:.2f}, {{blur: 16, scale: 1.2, y: 0, d: 0.3}});")
js.append(f"  fx.blurOut(tl, '#answer', {CUTS[11] - 0.3:.2f}, {{d: 0.2}});")

# ------------------------------------------------------------------ étapes du walkout (au-dessus des sous-titres)
STEPS = [(CUTS[5], CUTS[7], "LE DRAPEAU", "Pays-Bas"), (CUTS[7], CUTS[8], "LE POSTE", "MC"), (CUTS[8], T_SIL, "LE CLUB", "Dortmund")]
for n, (a, b, small, big) in enumerate(STEPS):
    body.append(f'<div class="clip step" id="st{n}" data-start="{a + 0.05:.2f}" data-duration="{b - a - 0.05:.2f}" data-track-index="3">'
                f'<span class="sn">{small}</span><span class="sv">{big}</span></div>')
    js.append(f"  fx.slideBlur(tl, '#st{n}', {a + 0.08:.2f}, {{x: -60}});")
    js.append(f"  fx.blurOut(tl, '#st{n}', {b - 0.22:.2f}, {{d: 0.18}});")
    sfx("pop", a + 0.08, 0.22, 0.12)

# ------------------------------------------------------------------ appel à l'action
body.append(f'<div class="clip pill" id="cta" data-start="{T_CTA - 0.05:.2f}" data-duration="{MAIN - T_CTA + 0.05:.2f}" data-track-index="3">'
            '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>Abonne-toi</div>')
js.append(f"  fx.blurIn(tl, '#cta', {T_CTA - 0.05:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("ding", T_CTA, 0.22, 0.7)

# ------------------------------------------------------------------ sous-titres mot à mot, mots clés en rouge
fix = {4: "0", 5: "crédit", 11: "dedans", 16: "soirée", 19: "plus", 20: "J'ouvre", 22: "drapeau…", 23: "attends…", 25: "poste…",
       26: "NON", 28: "club…", 29: "C'EST", 30: "PAS", 31: "POSSIBLE !", 32: "Abonne-toi", 39: "tien", 41: "j'ouvre"}
keys = {4, 5, 11, 12, 19, 20, 22, 23, 25, 26, 28, 29, 30, 31, 32, 34, 39}
glue = {"ce", "m'a", "le", "de", "la", "j'y", "qu'il", "y", "a", "c'est", "que", "pas"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]+$", "", words[i]["text"]))
groups, cur_g = [], []
for i in range(len(words)):
    cur_g.append(i)
    joined = " ".join(txt(k) for k in cur_g)
    if i not in (28, 30, 31) and txt(i).lower() in glue and len(cur_g) < 3 and len(joined) < 14 and i + 1 < len(words):
        continue
    groups.append(cur_g); cur_g = []
if cur_g: groups.append(cur_g)
for k, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else MAIN
    if 28 in g: b = T_SIL                         # rien pendant le silence
    label = " ".join(f"<span class='k'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    big = " big" if 29 in g or 31 in g else ""
    body.append(f'<div class="cap clip{big}" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="4">{label}</div>')
    js.append(f"  tl.fromTo('#c{k}', {{opacity: 0, scale: 1.25, filter: 'blur(8px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.16, ease: 'back.out(2)', immediateRender: true}}, {a:.3f});")

# ------------------------------------------------------------------ sons
sfx("whoosh-long", 0.0, 0.25, 1.0)
for c in (CUTS[2], CUTS[5], CUTS[8]):
    sfx("whoosh-court", c - 0.18, 0.18, 0.5)
sfx("riser", CUTS[8] - 0.1, 0.22, T_SIL - CUTS[8] + 0.1)        # monte sur « le club… » puis coupure nette
sfx("impact-boom", T_REV, 0.5, 1.2)

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.25, immediateRender: false}}, {MAIN - 0.25:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.35)

EXTRA_CSS = """
      #game { position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 45%; }
      #game video { position: absolute; inset: 0; width: 1080px; height: 1920px; }
      #vign { position: absolute; inset: 0; pointer-events: none;
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.3) 24%, rgba(0, 0, 0, 0) 38%, rgba(0, 0, 0, 0) 60%, rgba(0, 0, 0, 0.55) 78%, rgba(0, 0, 0, 0.35) 100%); }
      #dim { position: absolute; inset: 0; pointer-events: none; opacity: 0;
        background: radial-gradient(ellipse 60% 45% at 50% 45%, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.85) 100%); }
      #wave .ring { opacity: 0; top: 860px; }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6); }
      .plabel { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 270px; text-align: center; }
      .ps { display: inline-block; padding: 8px 22px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 30px;
        letter-spacing: 0.16em; color: var(--ink); }
      .pb { margin-top: 14px; font-weight: 700; font-size: 84px; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink); white-space: nowrap;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.85); paint-order: stroke fill; }
      .pb b { color: var(--accent-soft); }
      #answer .pb { font-size: 110px; }
      .step { position: absolute; left: 50%; top: 1210px; transform: translateX(-50%); display: flex; align-items: center; gap: 18px; white-space: nowrap;
        padding: 14px 34px; border-radius: 22px; background: rgba(28, 29, 33, 0.86); border: 3px solid var(--accent);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
      .step .sn { font-weight: 700; font-size: 28px; letter-spacing: 0.14em; color: var(--silver); }
      .step .sv { font-weight: 700; font-size: 52px; color: var(--ink); }
      #root .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      #root .cap.big { font-size: 100px; }
      #root .cap .k { margin: 0; }
      .pill { position: absolute; left: 50%; top: 1268px; transform: translateX(-50%); display: flex; align-items: center; gap: 20px;
        white-space: nowrap; padding: 14px 40px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 48px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill svg { width: 46px; height: 46px; }
"""

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx", ignore=shutil.ignore_patterns("reactions", "openverse"))
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")

def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
aud, tracks = [f'<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="16.80" data-volume="1" data-track-index="6"></audio>'], {}
# réaction de foule validée par l'utilisateur, une seule, sur la révélation (non versionnée, licence Mixkit)
REACT = f"{REPO}/effets/sfx/reactions/foule-victoire-enorme.wav"
has_react = os.path.exists(REACT)
if has_react:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REACT, "-t", "4.6", "-af", "afade=t=in:d=0.05,afade=t=out:st=3.4:d=1.2",
                    f"{A}/reaction.wav"], check=True)
    aud.append(f'<audio id="react" class="clip" src="assets/reaction.wav" data-start="{T_REV + 0.05:.2f}" data-duration="4.6" data-volume="0.4" data-track-index="12"></audio>')
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
print(f"pack opening FC 27 : {DUR} s, coupes {CUTS}, {len(groups)} sous-titres, {len(aud)} sons, foule : {'oui' if has_react else 'NON'}")
print(" | ".join(" ".join(txt(i) for i in g) for g in groups))
