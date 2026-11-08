"""TOP 3 des attaquants les plus pénibles en FUT Champions — style « gaming premium » (Specimen Gaming).

Voix off clonée (work/voix_off.wav), mots horodatés (work/words.json), cartes fournies par l'utilisateur,
détourées (work/<nom>_card.png). Révélation mystère de chaque carte, stats calées sur la voix.
"""
import difflib, html, json, os, re, shutil, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
heard = json.load(open(f"{ROOT}/work/words.json"))
S = json.load(open(f"{ROOT}/work/sections.json"))
script = json.load(open(f"{ROOT}/scripts/sections.json"))
VOICE_END = S["outro"][1]
MAIN = round(VOICE_END + 1.4, 2)
END = 2.2
DUR = round(MAIN + END, 2)

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9'-]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))

# affichage : nombres dits en toutes lettres → chiffres, « R neuf » → « R9 », « Numéro trois » → « N°3 »
NUM = {"quatre-vingt-quatorze": "94", "quatre-vingt-treize": "93", "quatre-vingt-onze": "91", "quatre-vingt-dix": "90",
       "quatre-vingt-six": "86", "trois": "3", "deux": "2", "un": "1"}

def align():
    toks = []
    for s in script:
        for w in s["text"].split():
            toks.append({"text": w, "sec": s["id"]})
    hw = [h for h in heard]
    a = [norm(t["text"]).replace("-", "") for t in toks]
    b = [norm(h["text"]).replace("-", "") for h in hw]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                toks[i1 + k]["start"], toks[i1 + k]["end"] = hw[j1 + k]["start"], hw[j1 + k]["end"]
        elif tag == "replace" and j2 > j1:
            t0, t1, n = hw[j1]["start"], hw[j2 - 1]["end"], i2 - i1
            for k in range(n):
                toks[i1 + k]["start"], toks[i1 + k]["end"] = t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n
    for i, t in enumerate(toks):
        if "start" not in t:
            prev = next((toks[k]["end"] for k in range(i - 1, -1, -1) if "end" in toks[k] and toks[k]["sec"] == t["sec"]), S[t["sec"]][0])
            t["start"], t["end"] = prev, prev + 0.22
    out, i = [], 0
    while i < len(toks):
        n0 = norm(toks[i]["text"]).strip(",.!?…")
        n1 = norm(toks[i + 1]["text"]).strip(",.!?…") if i + 1 < len(toks) else ""
        if n0 == "numero" and n1 in ("trois", "deux", "un"):
            out.append({**toks[i], "disp": f"N°{NUM[n1]}", "end": toks[i + 1]["end"], "key": True}); i += 2; continue
        if toks[i]["text"] in ("3.", "2.", "1.") and (i == 0 or toks[i - 1]["sec"] != toks[i]["sec"]):
            out.append({**toks[i], "disp": f"N°{toks[i]['text'][0]}", "key": True}); i += 1; continue
        if n0 == "r" and n1 == "neuf":
            out.append({**toks[i], "disp": "R9", "end": toks[i + 1]["end"], "key": True}); i += 2; continue
        d = toks[i]["text"]
        base = n0.rstrip(",")
        if base in NUM and base.startswith("quatre-vingt"):
            d = NUM[base] + re.sub(r"^[^,.!?…]*", "", d)
        out.append({**toks[i], "disp": d}); i += 1
    return out

words = align()
def T(w, sec, after=None):
    w = norm(w)
    a = S[sec][0] if after is None else after
    for x in words:
        n = norm(x["text"])
        if x["sec"] == sec and x["start"] >= a - 0.05 and (n.startswith(w) or n.split("'")[-1].startswith(w)):
            return x["start"]
    raise SystemExit(f"mot introuvable : {w} ({sec})")

body, js, audio = [], [], []
def sfx(name, t, vol=0.35, d=0.5): audio.append((name, max(0.0, t), vol, d))

js.append(f"  fx.breathe(tl, '#halo', 0, {MAIN});")
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="tracker"><span class="lbl">TOP 3</span>' + "".join(f'<div class="slot" id="slot{i}"></div>' for i in range(3)) + "</div>")

MYSTERY = ('<svg viewBox="0 0 100 136" style="width:100%; height:100%"><path d="M50 4 L94 18 V96 Q94 118 50 132 Q6 118 6 96 V18 Z" '
           'style="fill:var(--black)" opacity="0.95"/><text x="50" y="84" text-anchor="middle" font-size="52" font-weight="700" '
           'style="fill:var(--silver); font-family:var(--font)">?</text></svg>')

# ------------------------------------------------------------------ accroche
h0, h1 = S["hook"]
t_vecu = T("sais", "hook")
minis = "".join(f'<div class="mini" id="m{i}" style="width:250px; height:340px">{MYSTERY}</div>' for i in range(3))
body.append(f'<div class="clip" id="hook" data-start="0" data-duration="{h1 + 0.3:.2f}" data-track-index="2">'
            '<div class="bigtitle" style="top:250px; font-size:112px"><div class="kicker" id="hk">FUT CHAMPIONS · CE WEEK-END</div>'
            '<div id="h1">Ces <span class="acc">3</span> attaquants</div><div id="h2">t\'ont rendu fou</div></div>'
            f'<div style="position:absolute; left:70px; top:720px; display:flex; gap:45px">{minis}</div>'
            '<div class="ctanote" id="hn" style="top:1130px; width:940px; text-align:left; font-size:44px">Je sais exactement ce que t\'as vécu…</div></div>')
js.append("  fx.blurIn(tl, '#hk', 0.1);")
js.append("  fx.blurIn(tl, '#h1', 0.3);")
js.append("  fx.blurIn(tl, '#h2', 0.55);")
js.append("  tl.fromTo('#hook .mini', {opacity: 0, y: 60, filter: 'blur(12px)'}, {opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.45, ease: 'back.out(1.6)', stagger: 0.15, immediateRender: true}, 0.9);")
js.append(f"  fx.blurIn(tl, '#hn', {t_vecu - 0.1:.2f}, {{blur: 10}});")
js.append(f"  fx.blurOut(tl, '#hook', {h1 + 0.05:.2f});")
sfx("whoosh-long", 0.0, 0.3, 1.1)
for i in range(3): sfx("pop", 0.9 + 0.15 * i, 0.22, 0.12)

# ------------------------------------------------------------------ étapes du classement
RANKS = [  # section, rang, mot du nom, image, poste, badge, stats [(valeur, étiquette, mot déclencheur)], note, mot de la note, mot du badge
    ("n3", 3, "chawinga", "chawinga", "87 · AILIÈRE GAUCHE", "Fusée", [("94", "VITESSE", "94")], "Elle passe <b>quand même</b>", "clignes", "insupportable"),
    ("n2", 2, "pajor", "pajor", "89 · BUTEUSE", "Finisseuse", [("93", "VITESSE", "93"), ("91", "TIR", "91")], "Un demi-mètre = <b>but</b>", "laisses", "defends"),
    ("n1", 1, "ferran", "ferran", "86 · BUTEUR", "Mode R9", [("90", "VITESSE", "90"), ("86", "TIR", "86")], "Chaque frappe = <b>but</b>", "chaque", "mec"),
]
for k, (sec, rank, nameword, img, sub, badge, stats, note, noteword, badgeword) in enumerate(RANKS):
    s, e = S[sec][0], (S[RANKS[k + 1][0]][0] if k + 1 < len(RANKS) else S["outro"][0])
    sid = f"r{rank}"
    t_name = T(nameword, sec)
    rv = t_name - 0.05
    stat_times, after = [], s
    for v, l, w in stats:
        tt = T(w, sec, after); stat_times.append(tt); after = tt + 0.3
    t_note, t_badge = T(noteword, sec), T(badgeword, sec)
    name = {"chawinga": "Chawinga", "pajor": "Pajor", "ferran": "Ferran Torres"}[nameword]
    statbox = "".join(f'<div class="stat" id="{sid}s{j}"><div class="v" id="{sid}v{j}">0</div><div class="l">{l}</div></div>' for j, (v, l, w) in enumerate(stats))
    body.append(f'<div class="clip" id="{sid}" data-start="{s - 0.05:.2f}" data-duration="{e - s + 0.05:.2f}" data-track-index="2">'
                f'<div class="rank"><div class="no" id="{sid}no"><small>N°</small><b>{rank}</b></div>'
                f'<div class="txt"><div class="name" id="{sid}nm">{html.escape(name)}</div><div class="sub" id="{sid}sb">{sub}</div></div></div>'
                f'<div class="stagecard"><div class="ring" id="{sid}rg"></div>'
                f'<div class="mystery" id="{sid}my">{MYSTERY}</div>'
                f'<img class="cardimg" id="{sid}cv" src="assets/cards/{img}.png" alt="{html.escape(name)}"/></div>'
                f'<div class="side"><div class="badge" id="{sid}bd"><svg viewBox="0 0 24 24" class="ico"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z" style="fill:var(--accent)"/></svg>'
                f'<div><div class="bt">STYLE</div><div class="bv">{badge}</div></div></div>{statbox}</div>'
                f'<div class="note" id="{sid}nt">→ {note}</div></div>')
    js.append(f"  fx.blurIn(tl, '#{sid}no', {s:.2f}, {{blur: 24, y: 0, scale: 1.2}});")
    js.append(f"  tl.fromTo('#{sid}my', {{opacity: 0, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.35, ease: 'power2.out', immediateRender: true}}, {s + 0.1:.2f});")
    js.append(f"  tl.set('#{sid}cv', {{opacity: 0}}, {s - 0.05:.2f});")
    js.append(f"  tl.fromTo('#{sid}nm', {{opacity: 0.45, filter: 'blur(22px)'}}, {{opacity: 1, filter: 'blur(0px)', duration: 0.4, ease: 'power2.out', immediateRender: true}}, {rv:.2f});")
    js.append(f"  fx.blurIn(tl, '#{sid}sb', {rv + 0.15:.2f}, {{blur: 10}});")
    js.append(f"  fx.mysteryReveal(tl, '#{sid}my', '#{sid}cv', '#{sid}rg', {rv:.2f});")
    js.append(f"  fx.breathe(tl, '#{sid}cv', {rv + 0.6:.2f}, {e - rv - 1.0:.2f}, {{min: 0.92, max: 1, period: 1.4}});")
    js.append(f"  fx.trackerFill(tl, '#slot{2 - k}', {rv:.2f});")
    sfx("riser", rv - 1.4, 0.2, 1.4); sfx("impact-sec", rv, 0.5, 0.35); sfx("ding", rv + 0.1, 0.18, 0.7)
    for j, ((v, l, w), tt) in enumerate(zip(stats, stat_times)):
        js.append(f"  fx.slideBlur(tl, '#{sid}s{j}', {tt - 0.1:.2f}, {{x: 60}});")
        js.append(f"  fx.countUp(tl, '#{sid}v{j}', 0, {v}, {tt:.2f}, 0.6);")
        sfx("clic", tt - 0.1, 0.35, 0.05)
    js.append(f"  fx.slideBlur(tl, '#{sid}bd', {t_badge - 0.1:.2f}, {{x: 60}});")
    js.append(f"  fx.blurIn(tl, '#{sid}nt', {t_note - 0.1:.2f}, {{blur: 12, y: 16}});")
    sfx("whoosh-court", t_badge - 0.2, 0.18, 0.6)
    js.append(f"  fx.blurOut(tl, '#{sid}', {e - 0.3:.2f});")

# ------------------------------------------------------------------ conclusion
o0, o1 = S["outro"]
t_com = T("commentaire", "outro")
ICON = {
    "save": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--ink)"/></svg>',
    "like": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z" style="fill:var(--ink)"/></svg>',
    "sub": '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 1-5 4-9 10-10z" style="fill:var(--ink)"/></svg>',
}
grid = "".join(f'<div class="cta-btn">{ICON[k]}{l}</div>' for k, l in [("save", "Enregistre"), ("like", "Like"), ("sub", "Abonne-toi"), ("share", "Partage")])
body.append(f'<div class="clip" id="outro" data-start="{o0 - 0.05:.2f}" data-duration="{MAIN - o0 + 0.05:.2f}" data-track-index="2">'
            '<div class="bigtitle" style="top:250px; font-size:100px"><div id="o1">Et toi,</div><div id="o2">quel joueur t\'a fait</div>'
            '<div id="o3"><span class="acc">péter un câble ?</span></div></div>'
            f'<div class="ctagrid" id="og" style="top:760px">{grid}</div>'
            '<div class="ctanote" id="on" style="top:1260px">Dis-le en commentaire ↓</div></div>')
js.append(f"  fx.blurIn(tl, '#o1', {o0:.2f});")
js.append(f"  fx.blurIn(tl, '#o2', {o0 + 0.25:.2f});")
js.append(f"  fx.blurIn(tl, '#o3', {o0 + 0.5:.2f});")
js.append(f"  fx.ctaGrid(tl, '#og', {o0 + 1.0:.2f});")
js.append(f"  fx.blurIn(tl, '#on', {t_com - 0.1:.2f}, {{blur: 10}});")
for i in range(4): sfx("pop", o0 + 1.0 + 0.12 * i, 0.22, 0.12)

# ------------------------------------------------------------------ sous-titres mot à mot (1 à 3 mots), sauf pendant la conclusion affichée en grand
KEY = {"chawinga", "pajor", "ferran", "torres", "vitesse", "tir", "insupportable", "pire", "termine", "but", "commentaire", "champions", "fut", "souffrance", "quel"}
groups, cur = [], []
for i, x in enumerate(words):
    if x["sec"] == "outro":
        break
    cur.append(i)
    nxt_sec = words[i + 1]["sec"] if i + 1 < len(words) else None
    if re.search(r"[.!?,:…]$", x["text"]) or len(cur) >= 3 or sum(len(words[k]["disp"]) for k in cur) > 14 or nxt_sec != x["sec"]:
        groups.append(cur); cur = []
if cur: groups.append(cur)
for gi, g in enumerate(groups):
    st = max(0.0, words[g[0]]["start"] - 0.04)
    nxt = words[groups[gi + 1][0]]["start"] - 0.04 if gi + 1 < len(groups) else S["n1"][1] + 0.2
    en = min(nxt, S[words[g[0]]["sec"]][1] + 0.25)
    parts = []
    for k in g:
        d = re.sub(r"[.,!?:;…]+$", "", words[k]["disp"])
        key = words[k].get("key") or norm(words[k]["text"]).strip(",.!?") in KEY or d.isdigit()
        parts.append(f"<span class='k' style='margin-left:0'>{html.escape(d)}</span>" if key else html.escape(d))
    body.append(f'<div class="cap clip" id="c{gi}" data-start="{st:.2f}" data-duration="{max(0.2, en - st):.2f}" data-track-index="4" '
                f'style="gap:0 18px; flex-wrap:wrap">{" ".join(parts)}</div>')
    js.append(f"  fx.blurIn(tl, '#c{gi}', {st:.2f}, {{blur: 10, y: 14, d: 0.22}});")

# ------------------------------------------------------------------ écran de fin, audio, assemblage
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {MAIN - 0.3:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.4, 0.35)

aud = [f'<audio id="voice" class="clip" src="assets/voix_off.wav" data-start="0" data-duration="{VOICE_END + 0.2:.2f}" data-volume="1" data-track-index="0"></audio>']
tracks = {}
for n, (name, t, vol, d) in enumerate(audio):
    tr = 6
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

OUTDIR = f"{ROOT}/montage"
A = f"{OUTDIR}/assets"
os.makedirs(f"{A}/brand", exist_ok=True); os.makedirs(f"{A}/cards", exist_ok=True)
shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", OUTDIR)
open(f"{OUTDIR}/meta.json", "w").write('{"id":"fut-top3-attaquants","name":"fut-top3-attaquants"}')
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
for c in ("chawinga", "pajor", "ferran"):
    shutil.copy(f"{ROOT}/work/{c}_card.png", f"{A}/cards/{c}.png")
shutil.copy(f"{ROOT}/work/voix_off.wav", f"{A}/voix_off.wav")
tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
extra = ("      .cardimg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;\n"
         "        filter: drop-shadow(0 0 40px rgba(218, 61, 57, 0.55)) drop-shadow(0 30px 50px rgba(0, 0, 0, 0.6)); }\n"
         "      .mini { opacity: 0.95; }\n")
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()) + "\n" + extra)
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{OUTDIR}/index.html", "w").write(out)
print(f"TOP 3 attaquants : {DUR} s (voix {VOICE_END:.1f} s)")
