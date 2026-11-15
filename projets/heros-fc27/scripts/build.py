"""« Les Héros sont là » — TikTok Specimen Gaming sans gameplay : voix de l'utilisateur + cartes (src/cartes.jpg découpée
dans montage/assets/cartes/). Début rapide (titre dès la 1re image, blancs de la voix resserrés par scripts/prep.py).
Icônes Silva / Rossi, grille des Héros, puis Nasri (DRI 89), Hyypiä (PHY 99), Sturridge (PAC 91), Carrick (80 partout),
Diogo Jota (hommage, traité sobrement : pas d'impact ni de foule), question finale et CTA.
"""
import html, json, os, re, shutil, subprocess, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
CUTS = json.load(open(f"{ROOT}/work/timemap.json"))
def remap(t):
    s = 0.0
    for a, b in CUTS:
        if t >= b: s += b - a
        elif t > a: return a - s
    return t - s
raw = json.load(open(f"{ROOT}/src/transcript.json"))
FIX = {0: "EA", 5: "Héros", 10: "réclamait !", 12: "Icônes", 14: "88", 18: "Rossi", 20: "Héros ?", 22: "lourd", 23: "Nasri", 26: "dribble",
       27: "Hyypiä", 30: "physique", 32: "mur !", 33: "Sturridge", 36: "vitesse", 37: "Carrick", 39: "partout", 44: "Héros",
       45: "L'hommage", 48: "frissonner", 49: "Tu packes", 50: None, 51: None, 54: "premier ?", 55: "Dis-le", 59: "abonne-toi", 64: "carte"}
words = []
for i, w in enumerate(raw):
    txt = FIX.get(i, re.sub(r"[.,?!]+$", "", w["text"]))
    if txt is None: continue
    words.append({"text": txt, "start": remap(w["start"]), "src": i})
S = {w["src"]: k for k, w in enumerate(words)}
def T(i):                                       # temps (nouvelle timeline) du mot d'origine i
    return words[S[i]]["start"]
vd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{ROOT}/montage/assets/voix.wav"],
                          capture_output=True, text=True).stdout)
MAIN = round(vd + 0.35, 2)
END = 2.3
DUR = round(MAIN + END, 2)
SEC = {"hook": (0.0, T(11)), "icons": (T(11), T(19)), "grid": (T(19), T(23)), "nasri": (T(23), T(27)), "hyypia": (T(27), T(33)),
       "sturridge": (T(33), T(37)), "carrick": (T(37), T(40)), "jota": (T(40), T(49)), "cta": (T(49), MAIN)}

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))
def clip(cid, a, b, inner, cls="", track=1):
    body.append(f'<div class="clip {cls}" id="{cid}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="{track}">{inner}</div>')

js.append(f"  fx.breathe(tl, '#halo', 0, {MAIN}, {{}});")

# ------------------------------------------------------------------ titres en haut
def label(lid, a, b, small, big, fast=False):
    clip(lid, a, b, f'<div class="ps">{small}</div><div class="pb">{big}</div>', "plabel", 3)
    if fast:   # 1re image : déjà lisible (début rapide)
        js.append(f"  tl.fromTo('#{lid}', {{scale: 1.08, opacity: 1}}, {{scale: 1, duration: 0.35, ease: 'back.out(2)', immediateRender: true}}, 0);")
    else:
        js.append(f"  fx.blurIn(tl, '#{lid}', {a + 0.02:.2f}, {{blur: 12, y: -16, d: 0.25}});")
    js.append(f"  fx.blurOut(tl, '#{lid}', {b - 0.22:.2f}, {{d: 0.18}});")

FLAME = ('<svg class="flame" viewBox="0 0 24 24"><path d="M12 2c1 3.2-.6 5-2 6.6C8.6 10.2 7 12 7 14.6 7 18 9.3 21 12.6 21 16.2 21 18 18.2 18 15.2'
         'c0-2.6-1.4-4.2-2.3-5.4-.3 1.6-1 2.6-2 3.1.4-3.2-.2-7.6-1.7-10.9z" style="fill:var(--accent)"/><path d="M12.4 21c-1.8 0-3-1.5-3-3.2 0-1.6 1-2.6 1.9-3.6'
         '.4 1.2 1.2 1.8 2 2 .1-.9.6-1.7 1.3-2.2.4.9.9 1.8.9 3 0 2.3-1.4 4-3.1 4z" style="fill:var(--ink)"/></svg>')
a, b = SEC["hook"]
label("hook", a, b, "FC 27 · ULTIMATE TEAM", f"LES HÉROS SONT LÀ {FLAME}", fast=True)
label("l_icons", *SEC["icons"], "2 ICÔNES", "<b>88</b> de note")
label("l_grid", *SEC["grid"], "CÔTÉ HÉROS ?", "Du <b>lourd</b>")
label("l_cta", *SEC["cta"], "ET TOI ?", "Tu packes <b>lequel</b> ?")

# ------------------------------------------------------------------ grille complète (accroche, héros, appel à l'action)
for gid, (a, b), z in (("g0", SEC["hook"], (1.3, 1.0)), ("g1", SEC["grid"], (1.0, 1.12)), ("g2", SEC["cta"], (1.08, 1.0))):
    clip(gid, a, b, '<img src="assets/cartes/grille.jpg" alt=""/>', "grid", 1)
    if gid == "g0":
        js.append(f"  tl.fromTo('#g0 img', {{scale: {z[0]}}}, {{scale: {z[1]}, duration: {b - a:.2f}, ease: 'power2.out', immediateRender: true}}, 0);")
    else:
        js.append(f"  fx.blurIn(tl, '#{gid}', {a:.2f}, {{blur: 18, y: 0, scale: 1.1, d: 0.35}});")
        js.append(f"  tl.fromTo('#{gid} img', {{scale: {z[0]}}}, {{scale: {z[1]}, duration: {b - a:.2f}, ease: 'none', immediateRender: false}}, {a:.2f});")
    if gid != "g2":
        js.append(f"  fx.blurOut(tl, '#{gid}', {b - 0.22:.2f}, {{d: 0.2}});")
    sfx("whoosh-long" if gid == "g0" else "whoosh-court", max(0, a - 0.12), 0.24 if gid == "g0" else 0.2, 0.9)

# ------------------------------------------------------------------ les deux Icônes
a, b = SEC["icons"]
clip("icons", a, b, '<img id="i_silva" class="card2" src="assets/cartes/silva.jpg" alt="David Silva"/>'
                    '<img id="i_rossi" class="card2" src="assets/cartes/rossi.jpg" alt="Rossi"/>', "", 1)
js.append(f"  fx.slideBlur(tl, '#i_silva', {a + 0.02:.2f}, {{x: -120}});")
js.append(f"  fx.slideBlur(tl, '#i_rossi', {a + 0.12:.2f}, {{x: 120}});")
for me, other, t in (("#i_silva", "#i_rossi", T(15)), ("#i_rossi", "#i_silva", T(18))):
    js.append(f"  tl.to('{me}', {{scale: 1.1, filter: 'brightness(1.1)', duration: 0.3, ease: 'back.out(2)'}}, {t:.2f});")
    js.append(f"  tl.to('{other}', {{scale: 0.92, filter: 'brightness(0.45)', duration: 0.3, ease: 'power2.out'}}, {t:.2f});")
    sfx("clic", t, 0.25, 0.1)
js.append(f"  fx.blurOut(tl, '#icons', {b - 0.22:.2f}, {{d: 0.2}});")
sfx("whoosh-court", a - 0.12, 0.2, 0.6)

# ------------------------------------------------------------------ un Héros par plan : carte + encadré de stat
HEROES = [("nasri", "Nasri", "LM", "DRIBBLE", 89, 24, None), ("hyypia", "Hyypiä", "CB", "PHYSIQUE", 99, 28, (31, "UN MUR")),
          ("sturridge", "Sturridge", "ST", "VITESSE", 91, 34, None), ("carrick", "Carrick", "CM", "PARTOUT", 80, 38, None),
          ("jota", "Diogo Jota", "ST", None, None, None, (45, "L'HOMMAGE"))]
for key, name, pos, stat, val, wi, extra in HEROES:
    a, b = SEC[key]
    clip(f"h_{key}", a, b, f'<div class="ring" id="r_{key}"></div><img class="card1" id="k_{key}" src="assets/cartes/{key}.jpg" alt="{html.escape(name)}"/>', "hero", 1)
    label(f"l_{key}", a, b, f"HÉROS · {pos}", name)
    js.append(f"  fx.mysteryReveal(tl, null, '#k_{key}', null, {a + 0.02:.2f});")
    js.append(f"  tl.fromTo('#k_{key}', {{y: 0}}, {{y: -18, duration: {b - a:.2f}, ease: 'none', immediateRender: false}}, {a:.2f});")
    js.append(f"  fx.blurOut(tl, '#h_{key}', {b - 0.22:.2f}, {{d: 0.2}});")
    if key != "jota":
        sfx("whoosh-court", a - 0.12, 0.2, 0.6)
    if stat:
        t = T(wi)
        start = val - 25
        clip(f"s_{key}", t - 0.05, b, f'<span class="sl">{stat}</span><span class="sv" id="v_{key}">{start}</span>', "statbox", 2)
        js.append(f"  fx.slideBlur(tl, '#s_{key}', {t - 0.05:.2f}, {{x: -60}});")
        js.append(f"  fx.countUp(tl, '#v_{key}', {start}, {val}, {t:.2f}, 0.5);")
        js.append(f"  fx.blurOut(tl, '#s_{key}', {b - 0.22:.2f}, {{d: 0.18}});")
        js.append(f"  tl.fromTo('#k_{key}', {{scale: 1}}, {{scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, ease: 'power2.out', immediateRender: false}}, {t + 0.45:.2f});")
        if key == "hyypia":
            js.append(f"  fx.shockwave(tl, '#r_{key}', {t + 0.45:.2f}, {{to: 1.0}});")
            sfx("impact-boom", t + 0.45, 0.4, 0.9)
        else:
            sfx("ding", t + 0.45, 0.2, 0.6)
    if extra:
        t = T(extra[0])
        clip(f"x_{key}", t - 0.05, b, f'<span class="sl">{extra[1]}</span>', "statbox note2", 2)
        if key == "jota":    # hommage : entrée lente, sans bruitage
            js.append(f"  fx.blurIn(tl, '#x_{key}', {t - 0.05:.2f}, {{blur: 16, y: 10, d: 0.6}});")
        else:
            js.append(f"  fx.slideBlur(tl, '#x_{key}', {t - 0.05:.2f}, {{x: 60}});")
            js.append(f"  tl.set('#s_{key}', {{opacity: 0}}, {t - 0.05:.2f});")
        js.append(f"  fx.blurOut(tl, '#x_{key}', {b - 0.22:.2f}, {{d: 0.18}});")
# Jota : halo atténué, lente poussée
a, b = SEC["jota"]
js.append(f"  tl.to('#halo', {{opacity: 0.18, duration: 0.8, ease: 'power2.out'}}, {a:.2f});")
js.append(f"  tl.to('#halo', {{opacity: 0.45, duration: 0.5, ease: 'power2.out'}}, {b:.2f});")

# ------------------------------------------------------------------ appels à l'action
a, b = SEC["cta"]
T_COM, T_SUB = T(55), T(59)
clip("cta", T_COM - 0.05, T_SUB - 0.1, "Commente <b>ton choix</b>", "pill", 4)
js.append(f"  fx.blurIn(tl, '#cta', {T_COM - 0.05:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
js.append(f"  fx.blurOut(tl, '#cta', {T_SUB - 0.28:.2f}, {{d: 0.16}});")
clip("cta2", T_SUB - 0.1, MAIN, '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>Abonne-toi', "pill", 4)
js.append(f"  fx.blurIn(tl, '#cta2', {T_SUB - 0.1:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("pop", T_COM, 0.24, 0.12); sfx("ding", T_SUB, 0.2, 0.7)

# ------------------------------------------------------------------ signature
body.append('<div class="handle">SPECIMEN GAMING</div>')

# ------------------------------------------------------------------ sous-titres mot à mot, mots clés en rouge
keys = {S[x] for x in (5, 10, 12, 14, 15, 16, 18, 20, 22, 23, 24, 26, 27, 28, 30, 32, 33, 34, 36, 37, 38, 39, 41, 42, 45, 48, 49, 52, 57, 59)}
glue = {"de", "les", "que", "tout", "le", "à", "et", "du", "un", "en", "qui", "fait", "pour", "ne", "dis-le", "tu packes"}
groups, cur_g = [], []
for i, w in enumerate(words):
    cur_g.append(i)
    joined = " ".join(words[k]["text"] for k in cur_g)
    if w["text"].lower() in glue and len(cur_g) < 3 and len(joined) < 14 and i + 1 < len(words):
        continue
    groups.append(cur_g); cur_g = []
if cur_g: groups.append(cur_g)
for k, g in enumerate(groups):
    a = max(0.0, words[g[0]]["start"] - 0.04)
    b = (words[groups[k + 1][0]]["start"] - 0.04) if k + 1 < len(groups) else MAIN
    lab = " ".join(f"<span class='k'>{html.escape(words[i]['text'])}</span>" if i in keys else html.escape(words[i]["text"]) for i in g)
    body.append(f'<div class="cap clip" id="c{k}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="5">{lab}</div>')
    js.append(f"  tl.fromTo('#c{k}', {{opacity: 0, scale: 1.25, filter: 'blur(8px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.16, ease: 'back.out(2)', immediateRender: true}}, {a:.3f});")

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="6">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.25, immediateRender: false}}, {MAIN - 0.25:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.3, 0.35)

EXTRA_CSS = """
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; }
      .plabel { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 270px; text-align: center; }
      .ps { display: inline-block; padding: 8px 22px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 30px;
        letter-spacing: 0.16em; color: var(--ink); }
      .pb { margin-top: 14px; font-weight: 700; font-size: 84px; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink); white-space: nowrap;
        display: flex; align-items: center; justify-content: center; gap: 14px; }
      .pb b { color: var(--accent-soft); }
      .pb .flame { width: 76px; height: 76px; flex: none; }
      #hook .pb { font-size: 74px; gap: 10px; }
      .grid { position: absolute; left: 40px; top: 520px; width: 1000px; height: 618px; overflow: hidden; border-radius: 30px;
        border: 3px solid var(--accent); box-shadow: 0 0 60px rgba(218, 61, 57, 0.45), 0 30px 80px rgba(0, 0, 0, 0.6); }
      .grid img { width: 100%; height: 100%; object-fit: cover; transform-origin: 62% 55%; }
      #icons { position: absolute; inset: 0; }
      .card2 { position: absolute; top: 520px; width: 420px; height: 540px; border-radius: 26px; object-fit: cover;
        box-shadow: 0 0 40px rgba(218, 61, 57, 0.4), 0 30px 70px rgba(0, 0, 0, 0.6); }
      #i_silva { left: 100px; } #i_rossi { left: 560px; }
      .hero { position: absolute; inset: 0; }
      .card1 { position: absolute; left: 280px; top: 470px; width: 520px; height: 684px; border-radius: 30px; object-fit: cover;
        border: 4px solid var(--accent); box-shadow: 0 0 70px rgba(218, 61, 57, 0.55), 0 30px 80px rgba(0, 0, 0, 0.65); }
      .hero .ring { top: 812px; }
      .statbox { position: absolute; left: 50%; top: 1190px; transform: translateX(-50%); display: flex; align-items: center; gap: 22px; white-space: nowrap;
        padding: 10px 34px; border-radius: 22px; background: rgba(28, 29, 33, 0.9); border: 3px solid var(--accent);
        box-shadow: inset 0 0 30px rgba(218, 61, 57, 0.2), 0 10px 30px rgba(0, 0, 0, 0.5); }
      .statbox .sl { font-weight: 700; font-size: 34px; letter-spacing: 0.14em; color: var(--silver); }
      .statbox .sv { font-weight: 700; font-size: 84px; line-height: 1; color: var(--ink); }
      .note2 { padding: 22px 40px; }
      .note2 .sl { font-size: 48px; color: var(--ink); letter-spacing: 0.1em; }
      #root .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      #root .cap .k { margin: 0; }
      .pill { position: absolute; left: 50%; top: 1210px; transform: translateX(-50%); display: flex; align-items: center; gap: 16px;
        white-space: nowrap; padding: 18px 44px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 50px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill b { margin-left: 4px; }
      .pill svg { width: 50px; height: 50px; }
"""

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.copy(f"{ROOT}/src/cartes.jpg", f"{A}/cartes/grille.jpg")
used = sorted({x[0] for x in audio})
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
aud, tracks = [f'<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="{vd:.2f}" data-volume="1" data-track-index="7"></audio>'], {}
# une seule réaction de foule (son validé), sur « Un mur ! »
REACT = f"{REPO}/effets/sfx/reactions/foule-acclame-court.wav"
has_react = os.path.exists(REACT)
if has_react:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REACT, "-t", "2.4", "-af", "afade=t=in:d=0.05,afade=t=out:st=1.4:d=1.0",
                    f"{A}/reaction.wav"], check=True)
    aud.append(f'<audio id="react" class="clip" src="assets/reaction.wav" data-start="{T(32):.2f}" data-duration="2.4" data-volume="0.3" data-track-index="13"></audio>')
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t); tr = 8; d = round(min(d, length(name)), 3)
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
print(f"Héros FC 27 : {DUR} s ; sections " + ", ".join(f"{k} {a:.2f}-{b:.2f}" for k, (a, b) in SEC.items()))
print(" | ".join(" ".join(words[i]["text"] for i in g) for g in groups))
