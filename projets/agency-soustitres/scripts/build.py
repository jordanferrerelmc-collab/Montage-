"""« Sous-titres = vues » — motion design Specimen Agency (voix off ElevenLabs de l'utilisateur, sans visage).

Téléphone stylisé en légère perspective sur fond noir et halos or, bulles « liquid glass » (templates/reel-glass/glass.css),
zooms : coups de zoom sur les mots forts et transitions zoom entre les 5 parties du plan. Illustrations 100 % originales
(aucun logo ni interface d'application réelle), aucune statistique inventée (jauges sans chiffres).
"""
import html, json, os, re, shutil, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-agency"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
words = json.load(open(f"{ROOT}/work/transcript.json"))
W = [w["start"] for w in words]
P = [0.0, W[6] - 0.05, W[13] - 0.05, W[27] - 0.05, W[40] - 0.05]       # débuts des 5 parties
SPEECH_END = 18.76
MAIN = 19.0
END = 2.7
DUR = round(MAIN + END, 2)

body, js, sfx = [], [], []
def at(t): return f"{t:.3f}"
def fromto(sel, a, b, t, d, ease="power3.out", first=True):
    js.append(f'  tl.fromTo("{sel}", {a}, {{...{b}, duration: {d}, ease: "{ease}", immediateRender: {"true" if first else "false"}}}, {at(t)});')
def spring(sel, t, d=0.55, y=30):
    fromto(sel, f"{{opacity: 0, scaleX: 0.5, scaleY: 0.35, y: {y}}}", "{opacity: 1, scaleX: 1, scaleY: 1, y: 0}", t, d, "elastic.out(1, 0.62)")
def fade_out(sel, t, d=0.2):
    fromto(sel, "{opacity: 1}", "{opacity: 0}", t, d, "power2.in", False)

# ------------------------------------------------------------------ icônes (charte : or / ivoire / noir)
ICON = {
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.4-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.6-8 11-8 11z" style="fill:var(--ink)"/></svg>',
    "heartg": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.4-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.6-8 11-8 11z" style="fill:var(--accent)"/></svg>',
    "bubble": '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z" style="fill:var(--ink)"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 1-5 4-9 10-10z" style="fill:var(--ink)"/></svg>',
    "eye": '<svg viewBox="0 0 24 24"><path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" fill="none" style="stroke:var(--accent)" stroke-width="2.2"/><circle cx="12" cy="12" r="3" style="fill:var(--accent)"/></svg>',
    "text": '<svg viewBox="0 0 24 24"><path d="M5 6h14M12 6v13" fill="none" style="stroke:var(--accent)" stroke-width="2.8" stroke-linecap="round"/></svg>',
    "sync": '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3M18 3v4h-4M6 21v-4h4" fill="none" style="stroke:var(--accent)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "spark": '<svg viewBox="0 0 24 24"><path d="M12 2l2.2 6.6L21 11l-6.8 2.4L12 20l-2.2-6.6L3 11l6.8-2.4z" style="fill:var(--accent)"/></svg>',
    "up": '<svg viewBox="0 0 24 24"><path d="M4 17l6-6 4 4 6-7M14 8h6v6" fill="none" style="stroke:var(--accent)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" style="stroke:var(--ink)" stroke-width="2.4"/><path d="M15.5 15.5 21 21" style="stroke:var(--ink)" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "play": '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" style="fill:var(--black)"/></svg>',
}

def scene(cls=""):
    """« Vidéo » à l'écran : personnage stylisé face caméra (illustration originale), fond ivoire / or."""
    return (f'<div class="scene {cls}"><svg viewBox="0 0 100 160" preserveAspectRatio="xMidYMid slice">'
            '<rect width="100" height="160" style="fill:var(--gold-deep)"/><circle cx="78" cy="30" r="40" style="fill:var(--gold)" opacity="0.6"/>'
            '<circle cx="50" cy="62" r="17" style="fill:var(--ivory)"/><path d="M18 160c0-30 14-52 32-52s32 22 32 52z" style="fill:var(--black)"/>'
            '<path d="M38 108c4 8 20 8 24 0" fill="none" style="stroke:var(--gold-light)" stroke-width="2"/></svg></div>')

def side_icons(cls=""):
    return (f'<div class="side {cls}">' + "".join(f'<span>{ICON[k]}</span>' for k in ("heart", "bubble", "share")) + "</div>")

# ------------------------------------------------------------------ décor : fond noir, halos or qui dérivent, grille fine
body.append('<div id="bg"><i class="blob b1"></i><i class="blob b2"></i><i class="blob b3"></i><i class="grid"></i></div>')
fromto(".b1", "{x: -60, y: 0}", "{x: 80, y: 120}", 0, MAIN, "sine.inOut")
fromto(".b2", "{x: 40, y: 60}", "{x: -90, y: -80}", 0, MAIN, "sine.inOut")
fromto(".b3", "{x: 0, y: -40}", "{x: 60, y: 60}", 0, MAIN, "sine.inOut")

# tout le contenu animé passe dans #stage (coups de zoom + transitions zoom)
stage = []

# ---- Partie 1 : téléphone sans sous-titres, gros plan rapide, 3 mots « Sous-titres = vues »
stage.append(f'<div class="clip part" id="p1" data-start="0" data-duration="{P[1] + 0.3:.2f}" data-track-index="1">'
             f'<div class="phone" id="ph1"><div class="screen">{scene("ken")}{side_icons()}<div class="prog"><i id="pg1"></i></div></div></div>'
             '<div class="words"><span class="glass w" id="w1">Sous-titres</span><span class="glass w eq" id="w2">=</span><span class="glass w gold" id="w3">vues</span></div></div>')
fromto("#ph1", "{opacity: 0, scale: 0.7, rotateX: 18, y: 120}", "{opacity: 1, scale: 1, rotateX: 6, y: 0}", 0.0, 0.7, "power3.out")
fromto("#pg1", "{scaleX: 0}", "{scaleX: 1}", 0.0, P[1] + 0.3, "none")
fromto("#p1 .ken", "{scale: 1.0}", "{scale: 1.12}", 0.0, P[1] + 0.3, "none")
for k, t in enumerate((W[1], W[3], W[5])):            # « mots » … « booster » … « vues »
    spring(f"#w{k + 1}", t - 0.05, 0.5, 40)
    sfx.append(("ui", t - 0.05, 0.22, 0.5))
fade_out("#p1", P[1] - 0.15)

# ---- Partie 2 : mosaïque 2×2, sans sous-titres (à gauche) / avec (à droite), jauges qui montent (sans chiffres inventés)
def mini(n, on):
    cap = '<div class="minicap glass">Texte <b>court</b></div><i class="ov o1">' + ICON["spark"] + '</i>' if on else ""
    return (f'<div class="mini {"on" if on else "off"}" id="m{n}"><div class="screen">{scene()}{cap}</div>'
            f'<div class="meter"><span class="mi">{ICON["eye"]}</span><span class="bar"><i id="bar{n}"></i></span></div></div>')
stage.append(f'<div class="clip part" id="p2" data-start="{P[1] - 0.1:.2f}" data-duration="{P[2] - P[1] + 0.4:.2f}" data-track-index="1">'
             '<div class="colhead l glass" id="h2l">Sans sous-titres</div><div class="colhead r glass gold" id="h2r">Avec sous-titres</div>'
             f'<div class="mosaic">{mini(1, False)}{mini(2, True)}{mini(3, False)}{mini(4, True)}</div></div>')
for n, d in ((1, 0.0), (2, 0.08), (3, 0.16), (4, 0.24)):
    fromto(f"#m{n}", "{opacity: 0, scale: 0.6, y: 60}", "{opacity: 1, scale: 1, y: 0}", P[1] + d, 0.5, "back.out(1.7)")
spring("#h2l", P[1] + 0.3, 0.5, -20); spring("#h2r", P[1] + 0.4, 0.5, -20)
for n, lvl in ((1, 0.22), (3, 0.28), (2, 0.86), (4, 0.92)):
    fromto(f"#bar{n}", "{scaleX: 0}", f"{{scaleX: {lvl}}}", W[8], 1.6 if lvl > 0.5 else 1.0, "power2.out")
sfx.append(("chargement-donnees", W[8], 0.16, 1.0))
fade_out("#p2", P[2] - 0.15)

# ---- Partie 3 : étape par étape (texte court, synchronisé, overlays au bon moment) — sous-titre « karaoké » sur le téléphone
K = ["un", "texte", "court"]
kar = "".join(f'<span id="kw{i}">{w}</span> ' for i, w in enumerate(K))
stage.append(f'<div class="clip part" id="p3" data-start="{P[2] - 0.1:.2f}" data-duration="{P[3] - P[2] + 0.4:.2f}" data-track-index="1">'
             f'<div class="phone left" id="ph3"><div class="screen">{scene("ken")}{side_icons()}'
             f'<div class="kar glass" id="kar">{kar.strip()}</div>'
             f'<i class="ov o2" id="ov1">{ICON["heartg"]}</i><i class="ov o3" id="ov2">{ICON["spark"]}</i><i class="ov o4" id="ov3">{ICON["up"]}</i></div></div>'
             '<div class="steps">'
             f'<div class="glass note" id="st1"><span class="ico">{ICON["text"]}</span><span class="tx"><span class="t"><i>1</i>Texte court</span><span class="s">1 à 3 mots</span></span></div>'
             f'<div class="glass note" id="st2"><span class="ico">{ICON["sync"]}</span><span class="tx"><span class="t"><i>2</i>Synchronisé</span><span class="s">sur la voix</span></span></div>'
             f'<div class="glass note" id="st3"><span class="ico">{ICON["spark"]}</span><span class="tx"><span class="t"><i>3</i>Overlays</span><span class="s">au bon moment</span></span></div>'
             '</div></div>')
fromto("#ph3", "{opacity: 0, scale: 0.8, rotateY: -22, x: -80}", "{opacity: 1, scale: 1, rotateY: -10, x: 0}", P[2], 0.6, "power3.out")
fromto("#p3 .ken", "{scale: 1.0}", "{scale: 1.1}", P[2], P[3] - P[2], "none")
for k, t in enumerate((W[16], W[19], W[21])):         # « un texte court » / « synchronisé » / « overlays »
    spring(f"#st{k + 1}", t - 0.05, 0.55, 30)
    sfx.append(("ui", t - 0.05, 0.2, 0.5))
spring("#kar", W[16] - 0.05, 0.45, 20)
for i, t in enumerate((W[16], W[17], W[18])):         # mot surligné en or au moment où la voix le dit
    js.append(f'  tl.set("#kw{i}", {{color: "var(--gold-light)"}}, {at(t)});')
for k, t in enumerate((W[23], W[24] + 0.1, W[26])):   # overlays qui apparaissent « au bon moment »
    fromto(f"#ov{k + 1}", "{opacity: 0, scale: 0, rotation: -30}", "{opacity: 1, scale: 1, rotation: 0}", t, 0.45, "back.out(2.4)")
    sfx.append(("tic-flutter", t, 0.14, 0.5))
fade_out("#p3", P[3] - 0.15)

# ---- Partie 4 : preuve — cœurs qui montent, commentaires qui s'empilent, badge « Engagement ↑ » (sans pourcentage inventé)
hearts = "".join(f'<i class="fh" id="fh{i}">{ICON["heartg"]}</i>' for i in range(7))
COMS = ["Merci pour l'astuce", "Je teste tout de suite", "Enfin je comprends"]
coms = "".join(f'<div class="glass com" id="cm{i}"><b class="av"></b>{html.escape(c)}</div>' for i, c in enumerate(COMS))
stage.append(f'<div class="clip part" id="p4" data-start="{P[3] - 0.1:.2f}" data-duration="{P[4] - P[3] + 0.4:.2f}" data-track-index="1">'
             f'<div class="phone" id="ph4"><div class="screen">{scene("ken")}{side_icons("lit")}'
             '<div class="minicap glass big4">plus de <b>vues</b></div>'
             f'{hearts}<div class="coms">{coms}</div></div></div>'
             f'<div class="glass badge gold" id="badge"><span class="bi">{ICON["up"]}</span>Engagement</div></div>')
fromto("#ph4", "{opacity: 0, scale: 0.75, rotateX: 14}", "{opacity: 1, scale: 1, rotateX: 4}", P[3], 0.6, "power3.out")
fromto("#p4 .ken", "{scale: 1.0}", "{scale: 1.1}", P[3], P[4] - P[3], "none")
for i in range(7):
    t0 = W[29] + i * 0.32
    x = [-40, 30, -10, 50, -55, 15, 40][i]
    fromto(f"#fh{i}", "{opacity: 0, y: 0, x: 0, scale: 0.4}", f"{{opacity: 1, y: -320, x: {x}, scale: 1.1}}", t0, 1.2, "power1.out")
    fade_out(f"#fh{i}", t0 + 0.9, 0.3)
for i, t in enumerate((W[33], W[35], W[37])):
    fromto(f"#cm{i}", "{opacity: 0, x: 80, scale: 0.8}", "{opacity: 1, x: 0, scale: 1}", t, 0.45, "back.out(1.8)")
    sfx.append(("ui", t, 0.18, 0.5))
spring("#badge", W[36] - 0.05, 0.6, 20)
sfx.append(("impact-grave", W[36] - 0.05, 0.14, 1.2))
fade_out("#p4", P[4] - 0.15)

# ---- Partie 5 : écran de recherche, saisie de « Astuces visibilité TikTok », appel à l'action
Q = "Astuces visibilité TikTok"
stage.append(f'<div class="clip part" id="p5" data-start="{P[4] - 0.1:.2f}" data-duration="{MAIN - P[4] + 0.1:.2f}" data-track-index="1">'
             '<div class="phone light short" id="ph5"><div class="screen sr">'
             f'<div class="searchbar glass" id="sb"><span class="si">{ICON["search"]}</span><span id="q"></span><i class="caret" id="caret"></i></div>'
             + "".join(f'<div class="res" id="r{i}"><span class="th">{ICON["play"]}</span><span class="rl"><b></b><b></b></span></div>' for i in range(3)) +
             '</div></div>'
             f'<div class="glass note gold cta" id="cta"><span class="ico">{ICON["spark"]}</span><span class="tx"><span class="t">Teste-les</span><span class="s">tout de suite</span></span></div></div>')
fromto("#ph5", "{opacity: 0, scale: 0.8, rotateX: -12, y: 80}", "{opacity: 1, scale: 1, rotateX: 0, y: 0}", P[4], 0.6, "power3.out")
t0, t1 = W[41] - 0.05, W[43] + 0.35                   # saisie calée sur « Astuce Visibilité TikTok »
for i in range(1, len(Q) + 1):
    js.append(f'  tl.set("#q", {{textContent: {json.dumps(Q[:i])}}}, {at(t0 + (t1 - t0) * i / len(Q))});')
js.append(f'  tl.set("#q", {{textContent: ""}}, {at(P[4] - 0.1)});')
sfx.append(("clavier-apple", t0, 0.22, 0.6)); sfx.append(("clavier-apple", t0 + 0.6, 0.18, 0.6))
for i in range(3):
    fromto(f"#r{i}", "{opacity: 0, y: 40}", "{opacity: 1, y: 0}", t1 + 0.1 + i * 0.12, 0.4, "power3.out")
spring("#cta", W[45] - 0.05, 0.6, 30)
sfx.append(("ui", W[45] - 0.05, 0.22, 0.5))

# ------------------------------------------------------------------ titres de partie (bulle en haut)
LBL = [(0.05, P[1], "Sous-titres viraux"), (P[1], P[2], "Pourquoi ça marche"), (P[2], P[3], "Étape par étape"),
       (P[3], P[4], "Preuve rapide"), (P[4], MAIN, "Recherche")]
for n, (a, b, t) in enumerate(LBL):
    body.append(f'<div class="topwrap clip" id="lb{n}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="2">'
                f'<div class="glass lbl" id="lbb{n}"><span class="eyebrow">SPECIMEN AGENCY</span>{html.escape(t)}</div></div>')
    spring(f"#lbb{n}", a + 0.05, 0.6, -30)
    fade_out(f"#lbb{n}", b - 0.2)

# ------------------------------------------------------------------ zooms (style par défaut)
body.append('<div id="stage">' + "".join(stage) + '</div>')
zev = []
def punch(t, z=1.1, hold=0.7): zev.append((t, t + hold, z, 1.0, "power3.out"))
def through(t, zin=1.7):
    zev.append((t - 0.24, t, 1.0, zin, "power3.in")); zev.append((t, t + 0.42, zin * 0.75, 1.0, "power3.out"))
    js.append(f'  tl.fromTo("#stage", {{filter: "blur(0px)"}}, {{filter: "blur(10px)", duration: 0.22, ease: "power2.in", immediateRender: false}}, {at(t - 0.24)});')
    js.append(f'  tl.fromTo("#stage", {{filter: "blur(10px)"}}, {{filter: "blur(0px)", duration: 0.3, ease: "power2.out", immediateRender: false}}, {at(t)});')
    sfx.append(("whoosh-court", t - 0.2, 0.18, 0.5))
zev.append((0.55, P[1] - 0.3, 1.0, 1.22, "power2.inOut"))            # gros plan rapide de la partie 1
for t in P[1:]:
    through(t)
punch(W[12], 1.08); punch(W[19], 1.1); punch(W[35], 1.1); punch(W[43], 1.12); punch(W[48], 1.1)
zev.sort()
for n, (a, b, z0, z1, ease) in enumerate(zev):
    if n + 1 < len(zev): b = min(b, zev[n + 1][0])
    if b - a > 0.04:
        js.append(f'  tl.fromTo("#stage", {{scale: {z0:.3f}}}, {{scale: {z1:.3f}, duration: {b - a:.3f}, ease: "{ease}", immediateRender: {"true" if n == 0 else "false"}}}, {at(a)});')

# ------------------------------------------------------------------ sous-titres mot à mot dans une bulle de verre (en bas)
fix = {12: "l'engagement.", 41: "« Astuces", 42: "visibilité", 43: "TikTok »", 50: "suite !"}
keys = {1, 3, 5, 7, 11, 12, 15, 18, 19, 21, 26, 31, 35, 38, 41, 42, 43, 45, 50}
glue = {"trois", "pour", "vos", "les", "et", "par", "un", "des", "qui", "au", "bon", "plus", "de", "quand", "ces", "tout", "preuve"}
def txt(i):
    t = fix.get(i, words[i]["text"]); return t if i in fix else re.sub(r"[.,?!]$", "", t)
groups, cur = [], []
for i in range(len(words)):
    cur.append(i)
    if words[i]["text"].lower().strip(".,!") in glue and len(cur) < 3 and len(" ".join(txt(k) for k in cur)) < 15 and i + 1 < len(words):
        continue
    groups.append(cur); cur = []
if cur: groups.append(cur)
for k, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04); b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else SPEECH_END + 0.2
    label = " ".join(f"<span class='kw'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    body.append(f'<div class="capwrap clip" id="c{k}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="4"><div class="glass cap" id="cb{k}">{label}</div></div>')
    js.append(f'  tl.fromTo("#cb{k}", {{opacity: 0, scale: 0.86, y: 10}}, {{opacity: 1, scale: 1, y: 0, duration: 0.22, ease: "back.out(2.2)", immediateRender: true}}, {at(a)});')

# ------------------------------------------------------------------ écran de fin (charte)
tag = brand.get("tagline")
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/>'
           + (f'<div id="tagline">{"<br/>".join(p.strip() + "." for p in tag.rstrip(".").split("."))}</div>' if tag else "") + "</div>")
js.append(f'  tl.fromTo("#stage", {{opacity: 1}}, {{opacity: 0, duration: 0.25, immediateRender: false}}, {at(MAIN - 0.25)});')
js.append(f'  tl.fromTo("#logo", {{opacity: 0, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.7, ease: "power3.out", immediateRender: true}}, {at(MAIN + 0.05)});')
if tag:
    js.append(f'  tl.fromTo("#tagline", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.6, ease: "power3.out", immediateRender: true}}, {at(MAIN + 0.5)});')
sfx.append(("whoosh-court", MAIN - 0.25, 0.14, 0.5))

# ------------------------------------------------------------------ ressources
A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True); os.makedirs(f"{A}/sfx", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
FALLBACK = {"ui": "pop", "impact-grave": "impact-sec", "tic-flutter": "pop", "chargement-donnees": "montee-ui", "clavier-apple": "frappe-clavier"}
for n in {s[0] for s in sfx}:
    u = f"{REPO}/effets/sfx/utilisateur/{n}.wav"
    shutil.copy(u if os.path.exists(u) else f"{REPO}/effets/sfx/{FALLBACK.get(n, n)}.wav", f"{A}/sfx/{n}.wav")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/video1/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")
def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
aud = ['<audio id="voix" class="clip" src="assets/voix.wav" data-start="0" data-duration="18.76" data-volume="1" data-track-index="6"></audio>']
aud += [f'<audio id="s{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{round(min(d, length(name)), 3)}" '
        f'data-volume="{v}" data-track-index="{7 + n % 3}"></audio>' for n, (name, t, v, d) in enumerate(sfx)]

css = open(f"{BRAND_DIR}/brand.css").read()
glass = open(f"{REPO}/templates/reel-glass/glass.css").read()
STYLE = """
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font); }
#bg { position: absolute; inset: 0; background: radial-gradient(ellipse 90% 60% at 50% 42%, var(--panel-muted) 0%, var(--black) 70%); }
.blob { position: absolute; border-radius: 50%; filter: blur(90px); }
.b1 { left: -120px; top: 200px; width: 620px; height: 620px; background: var(--gold); opacity: 0.32; }
.b2 { right: -160px; top: 820px; width: 700px; height: 700px; background: var(--gold-deep); opacity: 0.38; }
.b3 { left: 260px; bottom: -160px; width: 560px; height: 560px; background: var(--gold-light); opacity: 0.18; }
.grid { position: absolute; inset: 0; opacity: 0.07;
  background-image: linear-gradient(var(--ivory) 1px, transparent 1px), linear-gradient(90deg, var(--ivory) 1px, transparent 1px);
  background-size: 90px 90px; }
#stage { position: absolute; inset: 0; transform-origin: 50% 46%; perspective: 1600px; }
.part { position: absolute; inset: 0; perspective: 1600px; }
/* téléphone stylisé (sans logo ni interface d'application réelle) */
.phone { position: absolute; left: 270px; top: 330px; width: 540px; height: 1060px; border-radius: 76px; padding: 18px;
  background: var(--black); border: 3px solid var(--gold-deep);
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.08), 0 50px 120px rgba(0, 0, 0, 0.7), 0 0 90px rgba(227, 178, 92, 0.22); transform-style: preserve-3d; }
.phone.left { left: 70px; width: 470px; height: 920px; top: 400px; }
.screen { position: relative; width: 100%; height: 100%; border-radius: 60px; overflow: hidden; background: var(--black); }
.scene, .scene svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.side { position: absolute; right: 22px; bottom: 180px; display: flex; flex-direction: column; gap: 30px; }
.side span { width: 64px; height: 64px; display: block; filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.6)); }
.side.lit span:first-child svg path { fill: var(--accent) !important; }
.prog { position: absolute; left: 26px; right: 26px; bottom: 40px; height: 6px; border-radius: 3px; background: rgba(255, 255, 255, 0.25); overflow: hidden; }
.prog i { display: block; height: 100%; background: var(--ivory); transform-origin: 0 50%; }
.words { position: absolute; left: 0; right: 0; top: 760px; display: flex; justify-content: center; gap: 18px; }
.w { padding: 22px 40px; font-weight: 700; font-size: 74px; letter-spacing: -0.03em; }
.w.eq { padding: 22px 30px; }
.glass.w.gold, .glass.colhead.gold { background: linear-gradient(160deg, rgba(var(--glass-tint-soft), 0.95) 0%, rgba(var(--glass-tint), 0.9) 100%); color: var(--black); text-shadow: none; -webkit-text-stroke: 0; }
/* mosaïque 2×2 */
.colhead { position: absolute; top: 380px; width: 430px; text-align: center; padding: 16px 0; font-weight: 700; font-size: 40px; }
.colhead.l { left: 90px; } .colhead.r { left: 560px; }
.mosaic { position: absolute; left: 90px; top: 480px; width: 900px; display: grid; grid-template-columns: 430px 430px; gap: 40px; }
.mini { position: relative; }
.mini .screen { height: 420px; border-radius: 36px; border: 3px solid var(--dark); }
.mini.on .screen { border-color: var(--accent); box-shadow: 0 0 50px rgba(227, 178, 92, 0.35); }
.mini.off .screen { filter: grayscale(1) brightness(0.55); }
.minicap { position: absolute; left: 50%; bottom: 60px; transform: translateX(-50%); white-space: nowrap; padding: 12px 26px; font-weight: 700; font-size: 34px; }
.minicap b { color: var(--accent-soft); }
.minicap.big4 { bottom: 120px; font-size: 52px; padding: 16px 36px; }
.ov { position: absolute; width: 74px; height: 74px; display: block; filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.6)); }
.ov svg { width: 100%; height: 100%; }
.o1 { right: 26px; top: 30px; } .o2 { left: 40px; top: 200px; } .o3 { right: 110px; top: 120px; } .o4 { left: 60px; top: 470px; }
.meter { display: flex; align-items: center; gap: 14px; margin-top: 18px; }
.meter .mi { width: 52px; height: 52px; flex: none; } .meter .mi svg { width: 100%; height: 100%; }
.meter .bar { flex: 1; height: 18px; border-radius: 9px; background: rgba(255, 255, 255, 0.12); overflow: hidden; }
.meter .bar i { display: block; height: 100%; background: var(--gold-grad); transform-origin: 0 50%; }
.mini.off .meter .bar i { background: var(--taupe); }
/* étapes */
.kar { position: absolute; left: 50%; bottom: 150px; transform: translateX(-50%); white-space: nowrap; padding: 14px 30px; font-weight: 700; font-size: 44px; }
.steps { position: absolute; left: 560px; top: 520px; display: flex; flex-direction: column; gap: 36px; }
.steps .note { padding: 18px 30px 18px 18px; }
.steps .note .t { font-size: 42px; } .steps .note .s { font-size: 30px; }
/* preuve */
.fh { position: absolute; right: 40px; bottom: 300px; width: 70px; height: 70px; display: block; }
.fh svg { width: 100%; height: 100%; }
.coms { position: absolute; left: 22px; right: 100px; top: 70px; display: flex; flex-direction: column; gap: 16px; }
.com { display: flex; align-items: center; gap: 14px; border-radius: 28px; padding: 14px 22px; font-weight: 700; font-size: 30px; white-space: nowrap; }
.com .av { width: 44px; height: 44px; border-radius: 50%; flex: none; background: var(--gold-grad); }
.badge { position: absolute; left: 50%; top: 1240px; transform: translateX(-50%); display: flex; align-items: center; gap: 18px;
  padding: 22px 46px; font-weight: 700; font-size: 58px; }
.badge.gold { background: linear-gradient(160deg, rgba(var(--glass-tint-soft), 0.9) 0%, rgba(var(--glass-tint), 0.82) 100%); color: var(--glass-cta-ink); text-shadow: none; }
.badge .bi { width: 66px; height: 66px; } .badge .bi svg { width: 100%; height: 100%; } .badge .bi svg path { stroke: var(--black) !important; }
/* recherche */
.phone.light .screen { background: var(--ivory); }
.sr { padding: 90px 30px 0; display: flex; flex-direction: column; gap: 26px; }
.searchbar { display: flex; align-items: center; gap: 14px; border-radius: 999px; padding: 22px 24px; font-weight: 700; font-size: 29px; min-height: 92px; white-space: nowrap;
  background: var(--black) !important; }
.searchbar .si { width: 42px; height: 42px; flex: none; } .searchbar .si svg { width: 100%; height: 100%; }
.caret { width: 4px; height: 44px; background: var(--accent); display: block; }
.res { display: flex; gap: 20px; align-items: center; }
.res .th { width: 170px; height: 220px; border-radius: 24px; background: var(--gold-grad); display: flex; align-items: center; justify-content: center; flex: none; }
.res .th svg { width: 60px; height: 60px; }
.res .rl { flex: 1; display: flex; flex-direction: column; gap: 16px; }
.res .rl b { display: block; height: 22px; border-radius: 11px; background: var(--stone); opacity: 0.6; }
.res .rl b + b { width: 60%; }
.phone.short { height: 940px; }
.cta { position: absolute; left: 50%; top: 1318px; transform: translateX(-50%); }
/* zones de texte */
.lbl { border-radius: 40px; padding: 16px 44px 20px; text-align: center; font-weight: 700; font-size: 50px; letter-spacing: -0.02em; }
.capwrap { top: 1500px !important; z-index: 5; }
.topwrap { z-index: 5; }
"""
page = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <meta name="brand" content="{BRAND}" />
    <meta name="montage-style" content="liquid-glass-motion-design" />
    <script src="assets/gsap.min.js"></script>
    <style>
{chr(10).join("      " + l for l in css.splitlines())}
{chr(10).join("      " + l for l in glass.splitlines())}
{chr(10).join("      " + l for l in STYLE.splitlines())}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      {chr(10).join("      " + b for b in body).strip()}
      {endcard}
    </div>
    {chr(10).join("    " + a for a in aud).strip()}
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
open(f"{ROOT}/montage/index.html", "w").write(page)
print(f"motion design : {DUR} s, {len(groups)} sous-titres, {len(aud)} sons")
