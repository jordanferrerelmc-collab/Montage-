"""« La défense sur FC 27 » — TikTok Specimen Gaming, montage constructif et entraînant, voix de l'utilisateur.

assets/plans.mp4 (scripts/track.py puis scripts/prep.py) : le match recadré en vertical, qui suit le joueur contrôlé.
Sous-titres centrés mot à mot, zooms rythmés, liste « à éviter / à faire » qui se construit en haut (jamais sur les
sous-titres, pas de barre de progression), une réaction de foule sur l'égalisation.
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
MAIN = 28.6
END = 2.3
DUR = round(MAIN + END, 2)
# parties : accroche, anecdote, constat, à éviter, à faire, question, appel à l'action
P_STORY, P_IA, P_DONT, P_DO, P_ASK, P_CTA = W[13], W[28], W[39], W[50], W[70], W[74]

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5):
    audio.append((name, t, vol, d))

# ------------------------------------------------------------------ vidéo plein écran
body.append(f'<div id="game"><video id="gv" class="clip" src="assets/plans.mp4" data-start="0" data-duration="{MAIN}" '
            'data-has-audio="true" data-volume="0.2" data-track-index="0"></video></div>')
body.append('<div id="vign"></div>')

events = []
def punch(t, z=1.14, hold=0.8):
    events.append((t, t + hold, z, 1.0, "power3.out"))
def through(t, zin=2.2):
    """Transition « zoom à travers » : on plonge dans l'image, puis elle se repose."""
    events.append((t - 0.26, t, 1.0, zin, "power3.in")); events.append((t, t + 0.45, zin * 0.9, 1.0, "power3.out"))
    js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px)'}}, {{filter: 'blur(14px)', duration: 0.24, ease: 'power2.in', immediateRender: false}}, {t - 0.26:.3f});")
    js.append(f"  tl.fromTo('#game', {{filter: 'blur(14px)'}}, {{filter: 'blur(0px)', duration: 0.34, ease: 'power2.out', immediateRender: false}}, {t:.3f});")
    sfx("whoosh-court", t - 0.2, 0.2, 0.6)

punch(0.0, 1.14, 0.6)
punch(W[12], 1.22)                                   # nerfé
for t in (P_STORY, P_IA, P_DONT, P_DO):
    through(t)
punch(W[16], 1.14, 0.6)                              # 2 à 0
punch(W[19], 1.14, 0.6)                              # 88e
punch(W[25], 1.18, 0.55); punch(W[26], 1.24, 0.5); punch(W[27], 1.34, 0.9)      # raté, contre, égalisation
punch(W[33], 1.16)                                   # (l'IA ne) tacle (presque plus)
punch(W[45], 1.14, 0.7)                              # arrête de sprinter
for i in (53, 57, 63):
    punch(W[i], 1.12, 0.6)                           # change de joueur, ferme l'axe, tacle seulement
punch(P_ASK, 1.18, 0.8)
sfx("impact-sec", W[12], 0.3, 0.35); sfx("clic", W[25], 0.3, 0.1); sfx("clic", W[26], 0.3, 0.1); sfx("impact-boom", W[27], 0.4, 0.9)

events.sort()
for n, (a, b, z0, z1, ease) in enumerate(events):
    if n + 1 < len(events):
        b = min(b, events[n + 1][0])                 # jamais deux zooms en même temps
    if b - a < 0.05:
        continue
    js.append(f"  tl.fromTo('#game', {{scale: {z0:.3f}}}, {{scale: {z1:.3f}, duration: {b - a:.3f}, ease: '{ease}', immediateRender: {'true' if n == 0 else 'false'}}}, {a:.3f});")
js.append(f"  tl.fromTo('#game', {{filter: 'blur(0px) brightness(1)'}}, {{filter: 'blur(14px) brightness(0.5)', duration: 0.4, ease: 'power2.out', immediateRender: false}}, {P_CTA - 0.1:.3f});")

# réaction de foule (son validé par l'utilisateur) : une seule, sur l'égalisation
REACT = f"{REPO}/effets/sfx/reactions/foule-stade-cris.wav"
has_react = os.path.exists(REACT)

# ------------------------------------------------------------------ signature (pas de barre de progression)
body.append('<div class="handle">SPECIMEN GAMING</div>')
js.append("  fx.blurIn(tl, '.handle', 0.05, {blur: 8, d: 0.3});")

# ------------------------------------------------------------------ titres en haut (pastille + ligne), centrés
LABELS = [
    (0.0, P_STORY, "FC 27 · DÉFENSE", "Ton défenseur est <b>nerfé</b>"),
    (P_STORY, W[21], "HIER", "<b>2 - 0</b> · 88e minute"),
    (W[21], P_IA, "ET LÀ…", "Raté · Contre · <b>Égalisation</b>"),
    (P_IA, P_DONT, "LE CONSTAT", "L'IA ne <b>tacle</b> plus pour toi"),
    (P_ASK, P_CTA, "ET TOI ?", "Tu défends <b>comme ça</b> ?"),
]
for n, (a, b, small, big) in enumerate(LABELS):
    a0 = a + (0.2 if a else 0.05)
    body.append(f'<div class="clip plabel" id="pl{n}" data-start="{a0:.2f}" data-duration="{b - a0:.2f}" data-track-index="2">'
                f'<div class="ps">{small}</div><div class="pb">{big}</div></div>')
    js.append(f"  fx.blurIn(tl, '#pl{n}', {a0 + 0.05:.2f}, {{blur: 14, y: -20, d: 0.3}});")
    js.append(f"  fx.blurOut(tl, '#pl{n}', {b - 0.3:.2f}, {{d: 0.25}});")
sfx("whoosh-long", 0.0, 0.28, 1.1)

# ------------------------------------------------------------------ liste « à éviter » puis « à faire » (se construit ligne par ligne)
NO = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" style="fill:var(--accent)"/><path d="M7.5 7.5 L16.5 16.5 M16.5 7.5 L7.5 16.5" style="stroke:var(--ink)" stroke-width="2.8" stroke-linecap="round"/></svg>'
OK = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" style="fill:var(--ink)"/><path d="M6.5 12.5 L10.5 16.5 L17.5 8" fill="none" style="stroke:var(--charcoal-deep)" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def checklist(cid, a, b, title, icon, rows):
    lines = "".join(f'<div class="row" id="{cid}r{k}">{icon}<span>{t}</span></div>' for k, (_, t) in enumerate(rows))
    body.append(f'<div class="clip check" id="{cid}" data-start="{a + 0.2:.2f}" data-duration="{b - a - 0.2:.2f}" data-track-index="2">'
                f'<div class="ps">{title}</div>{lines}</div>')
    js.append(f"  fx.blurIn(tl, '#{cid} .ps', {a + 0.25:.2f}, {{blur: 10, y: -14, d: 0.25}});")
    for k, (t, _) in enumerate(rows):
        t = max(t, a + 0.3)
        js.append(f"  fx.slideBlur(tl, '#{cid}r{k}', {t:.2f}, {{x: -60}});")
        sfx("pop", t, 0.24, 0.12)
    js.append(f"  fx.blurOut(tl, '#{cid}', {b - 0.3:.2f}, {{d: 0.25}});")

checklist("no", P_DONT, P_DO, "À ÉVITER", NO, [(W[40], "Spammer le tacle"), (W[45], "Sprinter sur l'attaquant")])
checklist("ok", P_DO, P_ASK, "À FAIRE", OK, [(W[50], "Reste en jockey"), (W[53], "Change de joueur tôt"),
                                               (W[57], "Ferme l'axe, force-le sur l'aile"), (W[63], "Tacle quand il perd la balle")])

# ------------------------------------------------------------------ appels à l'action
body.append(f'<div class="clip pill" id="cta" data-start="{P_CTA - 0.05:.2f}" data-duration="{W[79] - P_CTA:.2f}" data-track-index="3">'
            '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>Abonne-toi</div>')
js.append(f"  fx.blurIn(tl, '#cta', {P_CTA - 0.05:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
js.append(f"  fx.blurOut(tl, '#cta', {W[79] - 0.3:.2f}, {{d: 0.2}});")
body.append(f'<div class="clip pill" id="cta2" data-start="{W[79] - 0.05:.2f}" data-duration="{MAIN - W[79] + 0.05:.2f}" data-track-index="3">'
            'Commente <b>« DEF »</b></div>')
js.append(f"  fx.blurIn(tl, '#cta2', {W[79] - 0.05:.2f}, {{blur: 14, scale: 1.15, y: 0}});")
sfx("pop", P_CTA, 0.25, 0.12); sfx("ding", W[80], 0.22, 0.7)

# ------------------------------------------------------------------ sous-titres mot à mot, centrés, mots clés en rouge
fix = {2: "27,", 12: "nerfé,", 16: "2", 18: "0,", 19: "88e", 24: "tacle,", 25: "raté,", 26: "contre,", 27: "égalisation", 30: "27,",
       31: "l'IA", 33: "tacle", 42: "spammer", 44: "tacle,", 52: "jockey,", 63: "Tacle", 71: "défends", 73: "ça ?", 80: "« DEF »", 85: "setup"}
keys = {4, 8, 12, 16, 17, 18, 19, 25, 26, 27, 31, 35, 40, 42, 45, 47, 52, 55, 56, 58, 62, 63, 67, 69, 74, 78, 80, 85}
glue = {"sur", "fc", "ton", "ne", "te", "il", "a", "été", "je", "le", "à", "ta", "de", "en", "et", "la", "tu", "mon", "2", "quand",
        "comme", "alors"}
def txt(i):
    return fix.get(i, re.sub(r"[.,?!]$", "", words[i]["text"]))
groups, cur_g = [], []
for i in range(len(words)):
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
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.66) 0%, rgba(0, 0, 0, 0.4) 26%, rgba(0, 0, 0, 0) 40%, rgba(0, 0, 0, 0) 64%, rgba(0, 0, 0, 0.55) 80%, rgba(0, 0, 0, 0.35) 100%); }
      .handle { top: 200px; left: var(--cap-left); width: var(--cap-width); text-align: center; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6); }
      /* titres et listes : centrés, en haut, loin des sous-titres */
      .plabel, .check { position: absolute; left: var(--cap-left); width: var(--cap-width); top: 270px; text-align: center; }
      .ps { display: inline-block; padding: 8px 22px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 30px;
        letter-spacing: 0.16em; color: var(--ink); }
      .pb { margin-top: 14px; font-weight: 700; font-size: 66px; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink); white-space: nowrap;
        -webkit-text-stroke: 10px rgba(0, 0, 0, 0.85); paint-order: stroke fill; }
      .pb b { color: var(--accent-soft); }
      .check .row { margin: 16px auto 0; width: 800px; height: 92px; display: flex; align-items: center; justify-content: center; gap: 20px; border-radius: 22px;
        background: rgba(28, 29, 33, 0.86); border: 3px solid var(--accent); font-weight: 700; font-size: 46px; color: var(--ink); white-space: nowrap;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
      .check .row svg { width: 54px; height: 54px; flex: none; }
      /* sous-titres centrés, zone sûre TikTok, contour noir */
      #root .cap { display: block; top: 1380px; height: 130px; line-height: 130px; text-align: center; white-space: nowrap; font-size: 84px;
        -webkit-text-stroke: 12px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 6px 26px rgba(0, 0, 0, 0.8); }
      #root .cap .k { margin: 0; }
      .pill { position: absolute; left: 50%; top: 820px; transform: translateX(-50%); display: flex; align-items: center; gap: 20px;
        white-space: nowrap; padding: 28px 52px; border-radius: 999px; background: var(--accent); font-weight: 700; font-size: 64px;
        box-shadow: 0 0 50px rgba(218, 61, 57, 0.6); }
      .pill svg { width: 60px; height: 60px; }
      .pill b { margin-left: 4px; }
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
aud, tracks = ['<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="28.44" data-volume="1" data-track-index="6"></audio>'], {}
if has_react:        # non versionné (licence Mixkit) : copié à côté de la voix, ignoré par git (assets/*.wav)
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REACT, "-t", "3.2", "-af", "afade=t=in:d=0.15,afade=t=out:st=2.2:d=1.0", f"{A}/reaction.wav"], check=True)
    aud.append(f'<audio id="react" class="clip" src="assets/reaction.wav" data-start="{W[27] + 0.1:.2f}" data-duration="3.2" data-volume="0.32" data-track-index="12"></audio>')
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
print(f"défense FC 27 : {DUR} s, {len(groups)} sous-titres, {len(aud)} sons, réaction de foule : {'oui' if has_react else 'NON (npm run sfx:reactions)'}")
