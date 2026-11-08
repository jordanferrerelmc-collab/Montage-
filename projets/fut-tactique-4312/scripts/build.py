"""Tactique 4-3-1-2 FC 27 (Specimen Gaming, style « gaming premium »).

Voix de l'utilisateur (src/voix.mp3) + ses captures (src/equipe.jpg, src/tactique.jpg).
Une « caméra » parcourt les captures et zoome sur chaque joueur quand il est cité ; une fiche
nom / rôle / consigne glisse en dessous. Sous-titres = paroles réelles, noms corrigés.
"""
import html, json, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
raw = json.load(open(f"{ROOT}/work/tr/transcript.json"))
VOICE_END = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{ROOT}/src/voix.mp3"]))
MAIN = round(VOICE_END + 0.6, 2)
END = 2.2
DUR = round(MAIN + END, 2)
K = 2576 / 2000            # repères mesurés sur une base 2000 px, captures en 2576 px

# ------------------------------------------------------------------ mots : corrections d'orthographe (noms, rôles)
FIX = {"Féleur": "Feller", "renarder": "renard des", "surface,": "surfaces,", "Shawinga": "Chawinga", "Lopez": "López",
       "désolé,": "dézoner,", "Karchawi": "Karchaoui", "Carrera": "Carreras", "Garcia": "García", "passe-courte": "passes courtes",
       "fuite": "FUT", "fut": "FUT", "FC-27.": "FC 27.", "FC-27": "FC 27", "4-3-1-2": "4-3-1-2"}
words = []
i = 0
while i < len(raw):
    x = dict(raw[i]); t = x["text"]
    if t == "Chéreten" and i + 1 < len(raw):
        x["text"], x["end"] = "Schertenleib", raw[i + 1]["end"]; words.append(x); i += 2; continue
    if t == "c'est" and i > 0 and raw[i - 1]["text"] == "Carrera":
        t = "et"
    x["text"] = FIX.get(t, t)
    words.append(x); i += 1

def W(token, after=0.0):
    tok = token.lower()
    for x in words:
        if x["start"] >= after - 0.05 and re.sub(r"[.,!?:;]+$", "", x["text"]).lower().startswith(tok):
            return x["start"]
    raise SystemExit(f"mot introuvable : {token} après {after}")

SEC = {"hook": 0.0, "att": W("devant"), "mil": W("maintenant", 28), "def": W("passons"), "reg": W("maintenant", 65), "fin": W("voilà")}

body, js, audio = [], [], []
def sfx(name, t, vol=0.3, d=0.5): audio.append((name, max(0.0, t), vol, d))

js.append(f"  fx.breathe(tl, '#halo', 0, {MAIN});")
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="tracker"><span class="lbl">TACTIQUE</span>' + "".join(f'<div class="slot" id="slot{i}"></div>' for i in range(4)) + "</div>")

# ------------------------------------------------------------------ caméra sur les captures
CAM_W, CAM_H, CAM_X, CAM_Y = 940, 780, 70, 470
body.append(f'<div id="cam" style="position:absolute; left:{CAM_X}px; top:{CAM_Y}px; width:{CAM_W}px; height:{CAM_H}px; border-radius:34px; '
            'overflow:hidden; border:4px solid var(--accent); background:var(--panel); box-shadow:0 0 60px rgba(218, 61, 57, 0.5), 0 30px 80px rgba(0, 0, 0, 0.6); opacity:0">'
            '<img id="imgE" src="assets/equipe.jpg" style="position:absolute; left:0; top:0; width:2576px; height:1449px; transform-origin:0 0"/>'
            '<img id="imgT" src="assets/tactique.jpg" style="position:absolute; left:0; top:0; width:2576px; height:1449px; transform-origin:0 0; opacity:0"/>'
            '<div class="ring" id="camring"></div></div>')

def view(img, cx, cy, s):
    """transformation qui centre le point (cx, cy) de la capture (base 2000 px) dans la caméra, au zoom s"""
    X, Y = cx * K, cy * K
    return f"{{x: {CAM_W / 2 - X * s:.1f}, y: {CAM_H / 2 - Y * s:.1f}, scale: {s}}}"

STATE = {}   # dernier cadrage de chaque capture : chaque mouvement part d'un état explicite (rendu déterministe)
MOVES = []   # (temps, img, cadrage) ; triés avant émission

def move(img, t, cx, cy, s, d=0.6, snd=True):
    MOVES.append((t, img, (cx, cy, s), d))
    if snd: sfx("whoosh-court", t - 0.05, 0.14, 0.6)

def setv(img, t, cx, cy, s):
    STATE[img] = (cx, cy, s)
    js.append(f"  tl.set('#{img}', {view(img, cx, cy, s)}, {t:.2f});")

def flush_moves():
    for t, img, (cx, cy, s), d in sorted(MOVES, key=lambda m: m[0]):
        a = STATE.get(img, (cx, cy, s))
        js.append(f"  tl.fromTo('#{img}', {view(img, *a)}, {{...{view(img, cx, cy, s)}, duration: {d}, ease: 'power3.inOut', immediateRender: false}}, {t:.2f});")
        STATE[img] = (cx, cy, s)

OV_E = (1000, 560, 0.45)       # vue d'ensemble de l'équipe
OV_T = (1003, 520, 0.62)       # vue d'ensemble de la tactique
POS = {"feller": (880, 350), "chawinga": (1125, 350), "lopez": (1003, 405), "karchaoui": (862, 500), "pedri": (1143, 500),
       "schertenleib": (1003, 548), "bacha": (698, 622), "valverde": (1306, 622), "carreras": (861, 640), "garcia_dc": (1144, 640),
       "gk": (1003, 700), "dispositif": (718, 860), "construction": (1000, 860), "approche": (1281, 860), "code": (1000, 238)}

# ------------------------------------------------------------------ accroche : l'équipe, puis zoom sur « 4-3-1-2 »
t_form = W("4-3-1-2"); t_role = W("rôle")
setv("imgE", 0, *OV_E)
js.append("  tl.fromTo('#cam', {opacity: 0, scale: 0.9, filter: 'blur(14px)'}, {opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.5, ease: 'power3.out', immediateRender: false}, 0.1);")
move("imgE", t_form - 0.2, 480, 905, 1.35)
js.append(f"  fx.shockwave(tl, '#camring', {t_form:.2f}, {{to: 1.4}});")
sfx("impact-sec", t_form, 0.45, 0.35)
setv("imgT", 0, *OV_T)
js.append(f"  tl.to('#imgE', {{opacity: 0, duration: 0.4}}, {t_role - 0.3:.2f});")
js.append(f"  tl.to('#imgT', {{opacity: 1, duration: 0.4}}, {t_role - 0.3:.2f});")
body.append(f'<div class="clip" id="hook" data-start="0" data-duration="{SEC["att"] - 0.1:.2f}" data-track-index="2">'
            '<div class="rank" style="top:240px"><div class="txt"><div class="sub" id="hk0" style="letter-spacing:0.12em">FC 27 · FUT CHAMPIONS</div>'
            '<div class="name" id="hk1" style="font-size:96px">Ma tactique <span style="color:var(--accent-soft)">4-3-1-2</span></div></div></div></div>')
js.append("  fx.blurIn(tl, '#hk0', 0.15, {blur: 10});")
js.append(f"  fx.blurIn(tl, '#hk1', {t_form - 0.1:.2f}, {{blur: 22}});")
js.append(f"  fx.blurOut(tl, '#hook', {SEC['att'] - 0.4:.2f});")
sfx("whoosh-long", 0, 0.3, 1.1)

# ------------------------------------------------------------------ sections : en-tête + fiches joueurs
def header(sid, n, title, start, end, slot):
    body.append(f'<div class="clip" id="{sid}" data-start="{start:.2f}" data-duration="{end - start:.2f}" data-track-index="2">'
                f'<div class="rank" style="top:230px"><div class="no" id="{sid}no"><b style="font-size:150px">{n:02d}</b></div>'
                f'<div class="txt"><div class="name" id="{sid}nm">{title}</div><div class="sub" id="{sid}sb">TACTIQUE 4-3-1-2</div></div></div></div>')
    js.append(f"  fx.blurIn(tl, '#{sid}no', {start + 0.05:.2f}, {{blur: 24, y: 0, scale: 1.2}});")
    js.append(f"  fx.blurIn(tl, '#{sid}nm', {start + 0.15:.2f});")
    js.append(f"  fx.blurIn(tl, '#{sid}sb', {start + 0.3:.2f}, {{blur: 10}});")
    js.append(f"  fx.trackerFill(tl, '#slot{slot}', {start + 0.1:.2f});")
    js.append(f"  fx.blurOut(tl, '#{sid}', {end - 0.35:.2f});")
    sfx("riser", start - 1.0, 0.16, 1.0); sfx("impact-sec", start, 0.35, 0.35)

fid = [0]
def fiche(start, end, name, role, instr, pos, zoom=2.1):
    i = fid[0]; fid[0] += 1
    body.append(f'<div class="clip" id="f{i}" data-start="{start - 0.05:.2f}" data-duration="{end - start + 0.05:.2f}" data-track-index="3" '
                'style="position:absolute; left:70px; top:1275px; display:flex; align-items:center; gap:22px">'
                f'<div class="stat" id="f{i}a" style="width:auto; padding:16px 28px"><div class="v" style="font-size:62px">{html.escape(name)}</div>'
                f'<div class="l">{html.escape(role.upper())}</div></div>'
                f'<div class="badge" id="f{i}b"><svg viewBox="0 0 24 24" class="ico"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z" style="fill:var(--accent)"/></svg>'
                f'<div><div class="bt">CONSIGNE</div><div class="bv">{html.escape(instr)}</div></div></div></div>')
    js.append(f"  fx.slideBlur(tl, '#f{i}a', {start - 0.05:.2f}, {{x: -60}});")
    js.append(f"  fx.slideBlur(tl, '#f{i}b', {start + 0.35:.2f}, {{x: 60}});")
    js.append(f"  fx.blurOut(tl, '#f{i}', {end - 0.25:.2f}, {{d: 0.2}});")
    if pos:
        move("imgT", start - 0.35, *POS[pos], zoom)
    sfx("clic", start - 0.05, 0.3, 0.05)

def seq(items, sec_end):
    for k, (tok, after, name, role, instr, pos) in enumerate(items):
        st = W(tok, after)
        en = W(items[k + 1][0], items[k + 1][1]) - 0.1 if k + 1 < len(items) else sec_end
        fiche(st, en, name, role, instr, pos)

# attaque
header("hA", 1, "L'attaque", SEC["att"], SEC["mil"], 0)
move("imgT", SEC["att"], 1003, 400, 1.0)
seq([("feller", 0, "Feller", "Renard des surfaces", "Soutenir", "feller"),
     ("chawinga", 0, "Chawinga", "Fausse 9", "Attaquer", "chawinga"),
     ("lópez", 0, "López", "Meneuse de jeu", "Dézoner", "lopez")], SEC["mil"] - 0.2)
# milieu
header("hM", 2, "Le milieu", SEC["mil"], SEC["def"], 1)
move("imgT", SEC["mil"], 1003, 520, 1.0)
seq([("karchaoui", 0, "Karchaoui", "Box-to-box", "Gagner le ballon", "karchaoui"),
     ("schertenleib", 0, "Schertenleib", "Meneuse de jeu", "Défendre", "schertenleib"),
     ("pedri", 0, "Pedri", "Meneur de jeu", "Attaquer", "pedri")], SEC["def"] - 0.2)
# défense
header("hD", 3, "La défense", SEC["def"], SEC["reg"], 2)
move("imgT", SEC["def"], 1003, 640, 0.9)
t_axe = W("l'axe", 57)
seq([("bacha", 0, "Bacha", "Piston", "Soutenir", "bacha"),
     ("valverde", 0, "Valverde", "Défenseur latéral", "Polyvalence", "valverde"),
     ("carreras", 0, "Carreras & García", "Défenseurs", "Défendre", None),
     ("gardien", 62, "García", "Gardien", "Équilibré", "gk")], SEC["reg"] - 0.2)
move("imgT", t_axe, 1003, 640, 1.25)        # les deux centraux ensemble
# réglages
header("hR", 4, "Les réglages", SEC["reg"], SEC["fin"], 3)
move("imgT", SEC["reg"], 1000, 860, 0.9)
t_cons, t_appr = W("construction"), W("approche")
fiche(t_cons, t_appr - 0.1, "Passes courtes", "Style de construction", "Garder le ballon", "construction")
fiche(t_appr, SEC["fin"] - 0.2, "Haute", "Approche défensive", "Presser", "approche")

# ------------------------------------------------------------------ conclusion : code, CTA
F = SEC["fin"]
t_code, t_enr, t_com, t_abo = W("code"), W("enregistre"), W("commentaire"), W("abonne-toi")
move("imgT", F, 1003, 520, 0.62)
move("imgT", t_code - 0.3, 1000, 238, 1.5)
body.append(f'<div class="clip" id="fin1" data-start="{F:.2f}" data-duration="{t_enr - F:.2f}" data-track-index="2">'
            '<div class="rank" style="top:240px"><div class="txt"><div class="sub" id="fa" style="letter-spacing:0.12em">À TESTER SUR FC 27</div>'
            '<div class="name" id="fb" style="font-size:96px">Ma <span style="color:var(--accent-soft)">4-3-1-2</span> perso</div></div></div>'
            '<div class="pricepill" id="codepill" style="position:absolute; left:540px; top:1300px; bottom:auto; font-size:54px; padding:18px 44px">CODE : Mpk&amp;2iGeW4At</div></div>')
js.append(f"  fx.blurIn(tl, '#fa', {F + 0.05:.2f}, {{blur: 10}});")
js.append(f"  fx.blurIn(tl, '#fb', {F + 0.2:.2f});")
js.append(f"  fx.blurIn(tl, '#codepill', {t_code:.2f}, {{blur: 14, y: 20}});")
js.append(f"  fx.shockwave(tl, '#camring', {t_code:.2f}, {{to: 1.4}});")
sfx("impact-sec", t_code, 0.4, 0.35); sfx("ding", t_code + 0.1, 0.2, 0.7)
js.append(f"  fx.blurOut(tl, ['#fin1', '#cam'], {t_enr - 0.35:.2f});")
ICON = {
    "save": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--ink)"/></svg>',
    "like": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z" style="fill:var(--ink)"/></svg>',
    "sub": '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 1-5 4-9 10-10z" style="fill:var(--ink)"/></svg>',
}
grid = "".join(f'<div class="cta-btn" id="cb{k}">{ICON[k]}{l}</div>' for k, l in [("save", "Enregistre"), ("like", "Like"), ("sub", "Abonne-toi"), ("share", "Partage")])
body.append(f'<div class="clip" id="fin2" data-start="{t_enr - 0.1:.2f}" data-duration="{MAIN - t_enr + 0.1:.2f}" data-track-index="2">'
            '<div class="bigtitle" style="top:250px; font-size:96px"><div id="q1">Et toi,</div><div id="q2">tu joues <span class="acc">quelle formation ?</span></div></div>'
            f'<div class="ctagrid" id="og" style="top:700px">{grid}</div>'
            '<div class="ctanote" id="on" style="top:1200px">Réponds en commentaire ↓</div>'
            '<div class="pricepill" style="position:absolute; left:540px; top:1300px; bottom:auto; font-size:40px">CODE : Mpk&amp;2iGeW4At</div></div>')
js.append(f"  fx.ctaGrid(tl, '#og', {t_enr - 0.05:.2f});")
js.append(f"  tl.fromTo('#cbsave', {{scale: 1.15}}, {{scale: 1, duration: 0.3, ease: 'back.out(3)', immediateRender: false}}, {t_enr + 0.5:.2f});")
js.append(f"  fx.blurIn(tl, '#q1', {t_com - 0.6:.2f});")
js.append(f"  fx.blurIn(tl, '#q2', {t_com - 0.35:.2f});")
js.append(f"  fx.blurIn(tl, '#on', {t_com:.2f}, {{blur: 10}});")
js.append(f"  tl.fromTo('#cbsub', {{scale: 1.18}}, {{scale: 1, duration: 0.35, ease: 'back.out(3)', immediateRender: false}}, {t_abo:.2f});")
for k in range(4): sfx("pop", t_enr - 0.05 + 0.12 * k, 0.2, 0.12)
sfx("clic", t_abo, 0.4, 0.05)

flush_moves()

# ------------------------------------------------------------------ sous-titres mot à mot
NAMES = {"feller", "chawinga", "lópez", "karchaoui", "schertenleib", "pedri", "bacha", "valverde", "carreras", "garcía", "4-3-1-2"}
ROLES = {"renard", "fausse", "meneuse", "meneur", "box-to-box", "piston", "défenseur", "gardien", "soutenir", "attaquer", "dézoner",
         "défendre", "polyvalence", "équilibré", "construction", "passes", "courtes", "haute", "code", "commentaire", "abonne-toi"}
groups, cur = [], []
for i, x in enumerate(words):
    cur.append(i)
    gap = words[i + 1]["start"] - x["end"] if i + 1 < len(words) else 9
    if re.search(r"[.!?,:]$", x["text"]) or len(cur) >= 3 or gap > 0.35 or sum(len(words[k]["text"]) for k in cur) > 15:
        groups.append(cur); cur = []
if cur: groups.append(cur)
for gi, g in enumerate(groups):
    st = max(0.0, words[g[0]]["start"] - 0.04)
    en = (words[groups[gi + 1][0]]["start"] - 0.04) if gi + 1 < len(groups) else VOICE_END
    if st >= t_enr - 0.1:       # la fin est déjà écrite en grand
        break
    parts = []
    for k in g:
        d = re.sub(r"[.,!?:;]+$", "", words[k]["text"])
        key = d.lower() in NAMES or d.lower() in ROLES
        parts.append(f"<span class='k' style='margin-left:0'>{html.escape(d)}</span>" if key else html.escape(d))
    body.append(f'<div class="cap clip" id="c{gi}" data-start="{st:.2f}" data-duration="{min(en, t_enr - 0.1) - st:.2f}" data-track-index="4" '
                f'style="top:1450px; gap:0 18px; flex-wrap:wrap">{" ".join(parts)}</div>')
    js.append(f"  fx.blurIn(tl, '#c{gi}', {st:.2f}, {{blur: 10, y: 14, d: 0.22}});")

# ------------------------------------------------------------------ fin, audio, assemblage
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {MAIN - 0.3:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.4, 0.35)
aud = [f'<audio id="voice" class="clip" src="assets/voix.wav" data-start="0" data-duration="{VOICE_END:.2f}" data-volume="1" data-track-index="0"></audio>']
tracks = {}
for n, (name, t, vol, d) in enumerate(audio):
    tr = 6
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

OUT = f"{ROOT}/montage"; A = f"{OUT}/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", OUT)
open(f"{OUT}/meta.json", "w").write('{"id":"fut-tactique-4312","name":"fut-tactique-4312"}')
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
for f in ("equipe.jpg", "tactique.jpg"):
    shutil.copy(f"{ROOT}/src/{f}", f"{A}/{f}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/src/voix.mp3", "-af", "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=9",
                "-ar", "48000", "-ac", "1", f"{A}/voix.wav"], check=True)
tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{OUT}/index.html", "w").write(out)
print(f"tactique 4-3-1-2 : {DUR} s, sections {', '.join(f'{k}={v:.1f}' for k, v in SEC.items())}")
