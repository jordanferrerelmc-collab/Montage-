"""« Encore un 4-3-1-2 » remonté dans le style « gaming premium » (templates/reel-gaming).

Réutilise la voix off et les mots horodatés du projet (work/voix_off.wav, work/words.json) et la capture
de l'utilisateur (work/capture_card.mp4 : 16,3 s + arrêt sur image), affichée dans la carte centrale.
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
VOICE_END = S["s4"][1]
MAIN = round(VOICE_END + 1.6, 2)          # la grille CTA reste un peu après la voix
END = 2.2
DUR = round(MAIN + END, 2)

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9']", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))

def align():
    toks = [{"text": w, "sec": s["id"]} for s in script for w in s["text"].split()]
    a, b = [norm(t["text"]) for t in toks], [norm(h["text"]) for h in heard]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                toks[i1 + k]["start"], toks[i1 + k]["end"] = heard[j1 + k]["start"], heard[j1 + k]["end"]
        elif tag == "replace" and j2 > j1:
            t0, t1, n = heard[j1]["start"], heard[j2 - 1]["end"], i2 - i1
            for k in range(n):
                toks[i1 + k]["start"], toks[i1 + k]["end"] = t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n
    for i, t in enumerate(toks):
        if "start" not in t:
            prev = next((toks[k]["end"] for k in range(i - 1, -1, -1) if "end" in toks[k]), S[t["sec"]][0])
            t["start"], t["end"] = prev, prev + 0.25
    out, i = [], 0
    while i < len(toks):
        if [norm(x["text"]) for x in toks[i:i + 4]] == ["quatre", "trois", "un", "deux"]:
            out.append({**toks[i], "text": "4-3-1-2 !", "end": toks[i + 3]["end"]}); i += 4
        else:
            out.append(toks[i]); i += 1
    return out

words = align()
def T(w, after=0.0):
    w = norm(w)
    for x in words:
        n = norm(x["text"])
        if x["start"] >= after - 0.05 and (n.startswith(w) or n.split("'")[-1].startswith(w)):
            return x["start"]
    raise SystemExit(f"mot introuvable : {w}")

t_devine, t_compo = T("devine"), T("4-3-1-2")
t_meneur, t_att, t_parait = T("meneur"), T("attaquants"), T("parait")
t_res, t_abuse, t_toi = T("resultat"), T("abuse"), T("toi", T("abuse"))

body, js, audio = [], [], []
def sfx(name, t, vol=0.35, d=0.5): audio.append((name, max(0.0, t), vol, d))

# ------------------------------------------------------------------ fond, halo, signature
js.append(f"  fx.breathe(tl, '#halo', 0, {MAIN});")
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="tracker"><span class="lbl">FUT CHAMPIONS</span></div>')

# ------------------------------------------------------------------ en-tête : « ? » puis « 4-3-1-2 »
body.append(f'<div class="clip" id="hdr" data-start="0" data-duration="{t_toi - 0.1:.2f}" data-track-index="2">'
            '<div class="rank"><div class="no" id="hno"><b id="hq">?</b></div>'
            '<div class="txt"><div class="name" id="hnm">Je lance mon match</div><div class="sub" id="hsb">et devine quoi…</div></div></div></div>')
js.append("  fx.blurIn(tl, '#hno', 0.15, {blur: 24, y: 0, scale: 1.2});")
js.append("  fx.blurIn(tl, '#hnm', 0.3);")
js.append(f"  fx.blurIn(tl, '#hsb', {t_devine - 0.1:.2f}, {{blur: 10}});")
# bascule de l'en-tête au moment de la révélation
js.append(f"  fx.blurOut(tl, ['#hnm', '#hsb', '#hq'], {t_compo - 0.25:.2f}, {{d: 0.2}});")
js.append(f"  tl.set('#hq', {{textContent: '1'}}, {t_compo - 0.04:.2f});")
js.append(f"  tl.set('#hnm', {{textContent: '4-3-1-2'}}, {t_compo - 0.04:.2f});")
js.append(f"  tl.set('#hsb', {{textContent: 'La compo n°1 en FUT Champions'}}, {t_compo - 0.04:.2f});")
js.append(f"  tl.set('#hno', {{innerHTML: '<small>N°</small><b>1</b>'}}, {t_compo - 0.04:.2f});")
js.append(f"  tl.fromTo('#hnm', {{opacity: 0.4, filter: 'blur(22px)'}}, {{opacity: 1, filter: 'blur(0px)', duration: 0.4, ease: 'power2.out', immediateRender: false}}, {t_compo:.2f});")
js.append(f"  fx.blurIn(tl, '#hno', {t_compo:.2f}, {{blur: 24, y: 0, scale: 1.25}});")
js.append(f"  fx.blurIn(tl, '#hsb', {t_compo + 0.2:.2f}, {{blur: 10}});")

# ------------------------------------------------------------------ carte centrale : capture → mystère → révélation
MYST = ('<svg viewBox="0 0 160 90" style="width:100%; height:100%"><rect x="0" y="0" width="160" height="90" style="fill:var(--black)"/>'
        '<text x="80" y="62" text-anchor="middle" font-size="52" font-weight="700" style="fill:var(--silver); font-family:var(--font)">?</text></svg>')
body.append('<div id="card" style="position:absolute; left:70px; top:560px; width:940px; height:529px">'
            '<div class="ring" id="rg"></div>'
            '<div class="cardvis" id="cv" style="opacity:0"><video id="cap" class="clip" src="assets/capture.mp4" data-start="0" '
            f'data-duration="{t_toi - 0.1:.2f}" muted data-track-index="1" style="width:100%; height:100%; object-fit:cover; transform-origin:88% 30%"></video></div>'
            f'<div class="cardvis mystery" id="my" style="opacity:0">{MYST}</div>'
            '<div class="pricepill" id="pp"><span id="ct">1</span> × 4-3-1-2 croisés</div></div>')
js.append("  tl.fromTo('#cv', {opacity: 0, scale: 0.9, filter: 'blur(14px)'}, {opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.5, ease: 'power3.out', immediateRender: true}, 0.1);")
js.append("  tl.set('#pp', {opacity: 0}, 0);")
sfx("whoosh-long", 0.0, 0.3, 1.1)
# « devine quoi » : la carte devient mystère
js.append(f"  tl.to('#cv', {{opacity: 0, filter: 'blur(14px)', scale: 0.96, duration: 0.3}}, {t_devine + 0.3:.2f});")
js.append(f"  tl.to('#my', {{opacity: 1, duration: 0.3}}, {t_devine + 0.3:.2f});")
sfx("riser", t_compo - 2.0, 0.22, 2.0)
# révélation sur « 4-3-1-2 » + zoom sur le panneau adverse
js.append(f"  fx.mysteryReveal(tl, '#my', '#cv', '#rg', {t_compo:.2f}, {{to: 1.5}});")
js.append(f"  tl.fromTo('#cap', {{scale: 1}}, {{scale: 1.9, duration: 0.45, ease: 'power3.out', immediateRender: false}}, {max(t_compo, 6.75):.2f});")
js.append(f"  tl.to('#cap', {{scale: 1, duration: 0.5, ease: 'power3.inOut'}}, {t_meneur - 0.15:.2f});")
sfx("impact-sec", t_compo, 0.5, 0.35); sfx("ding", t_compo + 0.1, 0.2, 0.7)
# compteur de 4-3-1-2 croisés
js.append(f"  fx.blurIn(tl, '#pp', {t_compo + 0.5:.2f}, {{blur: 8, y: 10}});")
js.append(f"  fx.countUp(tl, '#ct', 1, 37, {t_res:.2f}, {t_abuse - t_res:.2f});")
js.append(f"  tl.set('#ct', {{textContent: '∞'}}, {t_abuse:.2f});")
js.append(f"  tl.fromTo('#pp', {{scale: 1.25}}, {{scale: 1, duration: 0.35, ease: 'back.out(3)', immediateRender: false}}, {t_abuse:.2f});")
# « abusé » : nouvelle onde de choc + halo plus intense
js.append(f"  fx.shockwave(tl, '#rg', {t_abuse:.2f}, {{to: 1.7, d: 0.9}});")
js.append(f"  tl.fromTo('#halo', {{opacity: 0.9, scale: 1.1}}, {{opacity: 0.45, scale: 1, duration: 0.8, immediateRender: false}}, {t_abuse:.2f});")
sfx("impact-boom", t_abuse, 0.35, 0.9)
js.append(f"  fx.blurOut(tl, ['#card', '#hdr'], {t_toi - 0.4:.2f});")

# ------------------------------------------------------------------ stats et badge (rangée sous la carte)
body.append(f'<div class="clip" id="row" data-start="{t_meneur - 0.1:.2f}" data-duration="{t_toi - t_meneur:.2f}" data-track-index="2" '
            'style="position:absolute; left:70px; top:1140px; display:flex; gap:22px; align-items:center">'
            '<div class="stat" id="s1" style="width:230px"><div class="v">1</div><div class="l">MENEUR</div></div>'
            '<div class="stat" id="s2" style="width:230px"><div class="v">2</div><div class="l">ATTAQUANTS</div></div>'
            '<div class="badge" id="bd"><svg viewBox="0 0 24 24" class="ico"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z" style="fill:var(--accent)"/></svg>'
            '<div><div class="bt">RÉPUTATION</div><div class="bv">La plus<br/>forte ?</div></div></div></div>')
js.append(f"  fx.slideBlur(tl, '#s1', {t_meneur - 0.1:.2f}, {{x: -60}});")
js.append(f"  fx.slideBlur(tl, '#s2', {t_att - 0.1:.2f}, {{x: -60}});")
js.append(f"  fx.slideBlur(tl, '#bd', {t_parait:.2f}, {{x: 60}});")
for t in (t_meneur - 0.1, t_att - 0.1): sfx("clic", t, 0.35, 0.05)
sfx("whoosh-court", t_parait - 0.1, 0.2, 0.6)
body.append(f'<div class="note clip" id="nt" data-start="{t_res - 0.1:.2f}" data-duration="{t_toi - t_res:.2f}" data-track-index="2" style="top:1340px">'
            '→ On ne croise <b>plus que ça</b></div>')
js.append(f"  fx.blurIn(tl, '#nt', {t_res:.2f}, {{blur: 12, y: 16}});")

# ------------------------------------------------------------------ fin : question + grille CTA
ICON = {
    "save": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--ink)"/></svg>',
    "like": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z" style="fill:var(--ink)"/></svg>',
    "sub": '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 1-5 4-9 10-10z" style="fill:var(--ink)"/></svg>',
}
grid = "".join(f'<div class="cta-btn">{ICON[k]}{l}</div>' for k, l in [("save", "Enregistre"), ("like", "Like"), ("sub", "Abonne-toi"), ("share", "Partage")])
body.append(f'<div class="clip" id="outro" data-start="{t_toi - 0.1:.2f}" data-duration="{MAIN - t_toi + 0.1:.2f}" data-track-index="2">'
            '<div class="bigtitle" style="top:260px; font-size:104px"><div id="o1">Et toi,</div><div id="o2">t\'en croises <span class="acc">combien ?</span></div></div>'
            f'<div class="ctagrid" id="og" style="top:700px">{grid}</div>'
            '<div class="ctanote" id="on" style="top:1200px">Réponds en commentaire ↓</div></div>')
js.append(f"  fx.blurIn(tl, '#o1', {t_toi - 0.05:.2f});")
js.append(f"  fx.blurIn(tl, '#o2', {t_toi + 0.2:.2f});")
js.append(f"  fx.ctaGrid(tl, '#og', {t_toi + 0.7:.2f});")
js.append(f"  fx.blurIn(tl, '#on', {t_toi + 1.3:.2f}, {{blur: 10}});")
for i in range(4): sfx("pop", t_toi + 0.7 + 0.12 * i, 0.22, 0.12)

# ------------------------------------------------------------------ sous-titres mot à mot (1 à 3 mots)
KEY = {"fut", "champions", "devine", "4-3-1-2", "meneur", "attaquants", "forte", "abuse", "combien"}
groups, cur = [], []
for i, x in enumerate(words):
    cur.append(i)
    if re.search(r"[.!?,:…]$", x["text"]) or len(cur) >= 3 or sum(len(words[k]["text"]) for k in cur) > 14:
        groups.append(cur); cur = []
if cur: groups.append(cur)
for gi, g in enumerate(groups):
    st = max(0.0, words[g[0]]["start"] - 0.04)
    en = (words[groups[gi + 1][0]]["start"] - 0.04) if gi + 1 < len(groups) else VOICE_END + 0.3
    if st >= t_toi - 0.1:      # la question finale est déjà affichée en grand
        break
    parts = []
    for k in g:
        t = words[k]["text"] if words[k]["text"].startswith("4-3-1-2") else re.sub(r"[.,!?:;…]+$", "", words[k]["text"])
        key = norm(words[k]["text"]) in KEY or t.startswith("4-3-1-2")
        parts.append(f"<span class='k' style='margin-left:0'>{html.escape(t)}</span>" if key else html.escape(t))
    body.append(f'<div class="cap clip" id="c{gi}" data-start="{st:.2f}" data-duration="{min(en, t_toi - 0.1) - st:.2f}" data-track-index="4" '
                f'style="gap:0 18px; flex-wrap:wrap">{" ".join(parts)}</div>')
    js.append(f"  fx.blurIn(tl, '#c{gi}', {st:.2f}, {{blur: 10, y: 14, d: 0.22}});")

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {MAIN - 0.3:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-sec", MAIN, 0.4, 0.35)

aud = [f'<audio id="voice" class="clip" src="assets/voix_off.wav" data-start="0" data-duration="{VOICE_END + 0.2:.2f}" data-volume="1" data-track-index="0"></audio>',
       '<audio id="game" class="clip" src="assets/game.wav" data-start="0" data-duration="16.3" data-volume="0.18" data-fade-out="0.8" data-track-index="1"></audio>']
tracks = {}
for n, (name, t, vol, d) in enumerate(audio):
    tr = 6
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

OUTDIR = f"{ROOT}/montage-premium"
A = f"{OUTDIR}/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{ROOT}/montage/hyperframes.json", OUTDIR)
open(f"{OUTDIR}/meta.json", "w").write('{"id":"fut-4312-premium","name":"fut-4312-premium"}')
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
for src, dst in [("work/capture_card.mp4", "capture.mp4"), ("work/voix_off.wav", "voix_off.wav"), ("work/game.wav", "game.wav")]:
    shutil.copy(f"{ROOT}/{src}", f"{A}/{dst}")
tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{OUTDIR}/index.html", "w").write(out)
print(f"4-3-1-2 (gaming premium) : {DUR} s, voix {VOICE_END:.1f} s")
