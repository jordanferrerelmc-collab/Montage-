"""« 75 000 crédits pour de l'or… j'ai eu du Bronze » — TikTok Specimen Gaming, voix de l'utilisateur (src/voix.mp3).

assets/plans.mp4 et assets/voix.wav : scripts/prep.py (18 plans de 0,5 à 1,9 s, calés sur la voix).
Accroche « 75 000 CRÉDITS = ??? » avec la carte floutée, étapes pack / 20 joueurs / pays / club / note, révélation
« Bronze » (Lucy Bronze 85, le jeu de mots), la suite du pack nom par nom, question « Rentable ou arnaque ? », CTA.
"""
import html, json, os, re, shutil, subprocess, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
raw = json.load(open(f"{ROOT}/src/transcript.json"))
# corrections de la transcription (vérifiées sur l'image) ; None = mot fusionné avec le précédent
FIX = {2: "75 000", 3: None, 6: "de l'or", 10: "bronze", 11: "Pack", 12: "Origines", 13: "déchaînées", 17: "Angleterre", 18: "Chelsea",
       19: "85", 20: "BRONZE !", 21: "Derrière", 23: "Alexander-Arnold", 24: None, 25: "Isco", 26: "Tchouaméni", 27: None,
       30: "arnaque ?", 31: "Dis-le", 33: "commentaire", 35: "abonne-toi !"}
words = []
for i, w in enumerate(raw):
    t = FIX.get(i, re.sub(r"[.,?!]+$", "", w["text"]))
    if t is None:
        continue
    words.append({"text": t, "start": w["start"], "src": i})
W = [w["start"] for w in words]
S = {w["src"]: k for k, w in enumerate(words)}          # index d'origine → index corrigé
PLANS = json.load(open(f"{ROOT}/scripts/plans.json"))
CUTS, t = [], 0.0
for p in PLANS:
    CUTS.append(round(t, 3)); t += p[1]
MAIN = round(t, 2)                                      # 19.60
END = 2.3
DUR = round(MAIN + END, 2)
T_TEASE, T_PACK, T_OPEN, T_ENG, T_CHE, T_85, T_REV, T_LIST = CUTS[2], CUTS[3], CUTS[5], CUTS[6], CUTS[7], CUTS[8], CUTS[9], CUTS[10]
T_ASK, T_CTA = CUTS[14], CUTS[16]

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ vidéo plein écran
body.append(f'<div id="game"><video id="gv" class="clip" src="assets/plans.mp4" data-start="0" data-duration="{MAIN}" '
            'data-has-audio="true" data-volume="0.4" data-track-index="0"></video></div>')
body.append('<div id="vign"></div>')

events = []
def punch(t, z=1.12, hold=0.6):
    events.append((t, t + hold, z, 1.0, "power3.out"))
punch(0.0, 1.16, 0.7)
for k, c in enumerate(CUTS[1:], 1):
    if c in (T_REV,):
        continue
    punch(c, 1.10 if k % 2 else 1.14, 0.5)
events.append((T_85, T_REV, 1.0, 1.18, "power1.in"))            # la note monte : poussée lente
events.append((T_REV, T_REV + 0.7, 1.4, 1.0, "expo.out"))       # révélation
events.sort()
clean = []
for e in events:                                                # une seule animation par instant
    if clean and abs(clean[-1][0] - e[0]) < 0.02:
        clean[-1] = e if e[2] > clean[-1][2] else clean[-1]
    else:
        clean.append(e)
for n, (a, b, z0, z1, ease) in enumerate(clean):
    if n + 1 < len(clean):
        b = min(b, clean[n + 1][0])
    if b - a < 0.05:
        continue
    js.append(f"  tl.fromTo('#game', {{scale: {z0:.3f}}}, {{scale: {z1:.3f}, duration: {b - a:.3f}, ease: '{ease}', immediateRender: {'true' if n == 0 else 'false'}}}, {a:.3f});")
# accroche : la carte est montrée floutée (on ne dévoile pas tout de suite)
js.append(f"  tl.fromTo('#gv', {{filter: 'blur(0px)'}}, {{filter: 'blur(28px) brightness(0.8)', duration: 0.12, immediateRender: false}}, {T_TEASE:.3f});")
js.append(f"  tl.to('#gv', {{filter: 'blur(0px) brightness(1)', duration: 0.12}}, {T_PACK - 0.06:.3f});")
js.append(f"  tl.fromTo('#game', {{filter: 'blur(18px) brightness(1.5)'}}, {{filter: 'blur(0px) brightness(1)', duration: 0.5, ease: 'power2.out', immediateRender: false}}, {T_REV:.3f});")
js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(14px) brightness(0.5)', duration: 0.3, ease: 'power2.in', immediateRender: false}}, {MAIN - 0.3:.3f});")
body.append(f'<div class="clip" id="wave" data-start="{T_REV:.2f}" data-duration="1.2" data-track-index="1"><div class="ring" id="ring"></div></div>')
js.append(f"  tl.fromTo('#ring', {{opacity: 0.95, scale: 0.2}}, {{opacity: 0, scale: 1.6, duration: 0.9, ease: 'power2.out', immediateRender: false}}, {T_REV:.3f});")

# ------------------------------------------------------------------ signature
body.append('<div class="handle">SPECIMEN GAMING</div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")

# ------------------------------------------------------------------ titres en haut
def label(lid, a, b, small, big, first=False):
    body.append(f'<div class="clip plabel" id="{lid}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="2">'
                f'<div class="ps">{small}</div><div class="pb">{big}</div></div>')
    js.append(f"  fx.blurIn(tl, '#{lid}', {a:.2f}, {{blur: 12, y: -16, d: {0.18 if first else 0.28}}});")
    js.append(f"  fx.blurOut(tl, '#{lid}', {b - 0.25:.2f}, {{d: 0.2}});")
label("hook", 0.0, T_PACK, "FC 27 · PACK OPENING", "75 000 CRÉDITS = <b>???</b>", True)
label("answer", T_REV + 0.08, T_LIST, "75 000 CRÉDITS =", "<b>BRONZE</b> 85")
for n, k in enumerate((10, 11, 12, 13)):                 # la suite du pack, un nom par plan
    name = ["Griezmann", "Alexander-Arnold", "Isco", "Tchouaméni"][n]
    body.append(f'<div class="clip plabel" id="nx{n}" data-start="{CUTS[k] + 0.03:.2f}" data-duration="{CUTS[k + 1] - CUTS[k] - 0.03:.2f}" data-track-index="2">'
                f'<div class="ps">DERRIÈRE</div><div class="pb">{name}</div></div>')
    js.append(f"  fx.blurIn(tl, '#nx{n} .pb', {CUTS[k] + 0.03:.2f}, {{blur: 10, y: -10, d: 0.15}});")
    sfx("pop", CUTS[k] + 0.03, 0.22, 0.12)
label("ask", T_ASK + 0.05, MAIN, "ET TOI ?", "Rentable <b>ou</b> arnaque ?")

# ------------------------------------------------------------------ étapes (au-dessus des sous-titres)
STEPS = [(T_PACK, CUTS[4], "LE PACK", "Origines déchaînées"), (CUTS[4], T_OPEN, "CONTENU", "20 joueurs Or"),
         (T_ENG, T_CHE, "LE PAYS", "Angleterre"), (T_CHE, T_85, "LE CLUB", "Chelsea"), (T_85, T_REV, "LA NOTE", "85")]
for n, (a, b, small, big) in enumerate(STEPS):
    body.append(f'<div class="clip step" id="st{n}" data-start="{a + 0.05:.2f}" data-duration="{b - a - 0.05:.2f}" data-track-index="3">'
                f'<span class="sn">{small}</span><span class="sv">{big}</span></div>')
    js.append(f"  fx.slideBlur(tl, '#st{n}', {a + 0.08:.2f}, {{x: -60}});")
    js.append(f"  fx.blurOut(tl, '#st{n}', {b - 0.2:.2f}, {{d: 0.16}});")
    sfx("pop", a + 0.08, 0.22, 0.12)

# ------------------------------------------------------------------ appels à l'action
T_SUB = W[S[34]]
body.append(f'<div class="clip pill" id="cta" data-start="{T_CTA:.2f}" data-duration="{T_SUB - T_CTA:.2f}" data-track-index="3">Commente <b>« RENTABLE »</b> ou <b>« ARNAQUE »</b></div>')
js.append(f"  fx.blurIn(tl, '#cta', {T_CTA:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
js.append(f"  fx.blurOut(tl, '#cta', {T_SUB - 0.2:.2f}, {{d: 0.18}});")
body.append(f'<div class="clip pill" id="cta2" data-start="{T_SUB:.2f}" data-duration="{MAIN - T_SUB:.2f}" data-track-index="3">'
            '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>Abonne-toi</div>')
js.append(f"  fx.blurIn(tl, '#cta2', {T_SUB:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("pop", T_CTA, 0.24, 0.12); sfx("ding", T_SUB + 0.1, 0.22, 0.7)

# ------------------------------------------------------------------ sous-titres mot à mot, mots clés en rouge
keys = {S[x] for x in (2, 4, 6, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 25, 26, 28, 30, 31, 35)}
glue = {"j'ai", "pour", "eu", "du", "et", "ou", "en", "dis-le"}
groups, cur_g = [], []
for i, w in enumerate(words):
    cur_g.append(i)
    joined = " ".join(words[k]["text"] for k in cur_g)
    if w["text"].lower() in glue and len(cur_g) < 3 and len(joined) < 14 and i + 1 < len(words):
        continue
    groups.append(cur_g); cur_g = []
if cur_g: groups.append(cur_g)
for k, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else MAIN
    lab = " ".join(f"<span class='k'>{html.escape(words[i]['text'])}</span>" if i in keys else html.escape(words[i]["text"]) for i in g)
    big = " big" if S[20] in g else ""
    body.append(f'<div class="cap clip{big}" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="4">{lab}</div>')
    js.append(f"  tl.fromTo('#c{k}', {{opacity: 0, scale: 1.25, filter: 'blur(8px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.16, ease: 'back.out(2)', immediateRender: true}}, {a:.3f});")

# ------------------------------------------------------------------ sons
sfx("whoosh-long", 0.0, 0.25, 1.0)
sfx("impact-sec", T_TEASE, 0.28, 0.35)                    # « j'ai eu du bronze » (carte floutée)
for c in (T_PACK, T_OPEN, T_LIST, T_ASK):
    sfx("whoosh-court", c - 0.18, 0.18, 0.5)
sfx("riser", T_85 - 0.2, 0.2, T_REV - T_85 + 0.2)
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
      #wave .ring { opacity: 0; top: 860px; }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6); }
      .plabel { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 270px; text-align: center; }
      .ps { display: inline-block; padding: 8px 22px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 30px;
        letter-spacing: 0.16em; color: var(--ink); }
      .pb { margin-top: 14px; font-weight: 700; font-size: 80px; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink); white-space: nowrap;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.85); paint-order: stroke fill; }
      .pb b { color: var(--accent-soft); }
      #answer .pb { font-size: 120px; }
      .step { position: absolute; left: 50%; top: 1210px; transform: translateX(-50%); display: flex; align-items: center; gap: 18px; white-space: nowrap;
        padding: 14px 34px; border-radius: 22px; background: rgba(28, 29, 33, 0.86); border: 3px solid var(--accent);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
      .step .sn { font-weight: 700; font-size: 28px; letter-spacing: 0.14em; color: var(--silver); }
      .step .sv { font-weight: 700; font-size: 52px; color: var(--ink); }
      #root .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      #root .cap.big { font-size: 104px; }
      #root .cap .k { margin: 0; }
      .pill { position: absolute; left: 50%; top: 1240px; transform: translateX(-50%); display: flex; align-items: center; gap: 16px;
        white-space: nowrap; padding: 16px 40px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 44px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill svg { width: 46px; height: 46px; }
"""

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
used = sorted({a[0] for a in audio})
shutil.rmtree(f"{A}/sfx", ignore_errors=True); os.makedirs(f"{A}/sfx")
for name in used:
    shutil.copy(f"{REPO}/effets/sfx/{name}.wav", f"{A}/sfx/{name}.wav")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")

def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
vd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{A}/voix.wav"],
                          capture_output=True, text=True).stdout)
aud, tracks = [f'<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="{min(vd, MAIN):.2f}" data-volume="1" data-track-index="6"></audio>'], {}
# réaction de foule validée par l'utilisateur, une seule, sur la révélation (non versionnée, licence Mixkit)
REACT = f"{REPO}/effets/sfx/reactions/foule-acclame-court.wav"
has_react = os.path.exists(REACT)
if has_react:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REACT, "-t", "2.6", "-af", "afade=t=in:d=0.05,afade=t=out:st=1.6:d=1.0",
                    f"{A}/reaction.wav"], check=True)
    aud.append(f'<audio id="react" class="clip" src="assets/reaction.wav" data-start="{T_REV + 0.05:.2f}" data-duration="2.6" data-volume="0.35" data-track-index="12"></audio>')
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
print(f"pack opening 2 : {DUR} s, {len(PLANS)} plans, {len(groups)} sous-titres, {len(aud)} sons, foule : {'oui' if has_react else 'NON'}")
print(" | ".join(" ".join(words[i]["text"] for i in g) for g in groups))
