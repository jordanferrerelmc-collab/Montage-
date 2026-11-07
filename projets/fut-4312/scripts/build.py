"""TikTok Specimen Gaming : « Tout le monde joue en 4-3-1-2 en FUT Champions ».

Fond : capture de l'utilisateur (work/backdrop.mp4, cadre centré sur fond flouté) + son du jeu en ambiance.
Voix off clonée (work/voix_off.wav), sous-titres dynamiques = texte exact du script calé sur la transcription.
Graphismes originaux : titre d'accroche, compteur de 4-3-1-2, tampon « ABUSÉ », question finale.
"""
import difflib, html, json, os, re, shutil, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = os.environ.get("BRAND", "specimen-gaming")
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
heard = json.load(open(f"{ROOT}/work/words.json"))
S = json.load(open(f"{ROOT}/work/sections.json"))
script = json.load(open(f"{ROOT}/scripts/sections.json"))
CLIP_LEN = 18.2
VOICE_END = S["s4"][1]
MAIN_END = max(CLIP_LEN, VOICE_END + 0.3)
END_LEN = 1.8
DUR = round(MAIN_END + END_LEN, 2)

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
            nxt = next((toks[k]["start"] for k in range(i + 1, len(toks)) if "start" in toks[k]), S[t["sec"]][1])
            t["start"], t["end"] = prev, max(prev + 0.05, min(nxt, prev + 0.3))
    out, i = [], 0       # « quatre, trois, un, deux » s'affiche « 4-3-1-2 »
    while i < len(toks):
        if [norm(x["text"]) for x in toks[i:i + 4]] == ["quatre", "trois", "un", "deux"]:
            out.append({**toks[i], "text": "4-3-1-2 !", "end": toks[i + 3]["end"]}); i += 4
        else:
            out.append(toks[i]); i += 1
    return out

words = align()
def T(word, after=0.0):
    w = norm(word)
    for x in words:
        n = norm(x["text"])
        if x["start"] >= after - 0.05 and (n.startswith(w) or n.split("'")[-1].startswith(w)):
            return x["start"]
    raise SystemExit(f"mot introuvable : {word}")

js, scenes, audio = [], [], []
def sfx(name, t, vol=0.4, dur=0.5):
    audio.append((name, max(0.0, t), vol, dur))
def pop(sel, t, fr="scale: 0.3, opacity: 0", d=0.3, ease="back.out(2.2)", name="pop", vol=0.3, snd=True):
    js.append(f'  tl.from("{sel}", {{{fr}, duration: {d}, ease: "{ease}"}}, {t:.3f});')
    if snd: sfx(name, t, vol, 0.15)
def punch(t, z=1.08, big=False):
    js.append(f'  tl.fromTo("#stage", {{scale: {z + 0.06:.2f}}}, {{scale: 1, duration: 0.3, ease: "expo.out", immediateRender: false}}, {t:.3f});')
    js.append(f'  tl.fromTo("#flash", {{opacity: {0.8 if big else 0.5}}}, {{opacity: 0, duration: 0.2, immediateRender: false}}, {t:.3f});')
    sfx("whoosh", t - 0.15, 0.3, 0.45)

# ------------------------------------------------------------------ temps clés
t_devine = T("devine")
t_encore = T("encore")
t_meneur = T("meneur")
t_parait = T("parait")
t_resultat = T("resultat")
t_abuse = T("abuse")
t_toi = T("toi", t_abuse)

# ------------------------------------------------------------------ fond (capture) : zooms sur l'action
js.append(f'  tl.fromTo("#broll", {{scale: 1}}, {{scale: 1.06, duration: {t_encore:.2f}, ease: "none"}}, 0);')
# zoom sur le panneau « 4-3-1-2 » de l'adversaire (à droite du cadre) au moment où il est cité
js.append(f'  tl.to("#broll", {{scale: 1.75, x: -330, y: 230, duration: 0.35, ease: "expo.out"}}, {t_encore - 0.05:.3f});')
js.append(f'  tl.to("#broll", {{scale: 1.0, x: 0, y: 0, duration: 0.4, ease: "expo.inOut"}}, {t_meneur - 0.2:.3f});')
js.append(f'  tl.to("#broll", {{scale: 1.1, duration: {max(0.5, t_resultat - t_meneur):.2f}, ease: "none"}}, {t_meneur + 0.2:.3f});')
js.append(f'  tl.to("#broll", {{scale: 1.0, duration: 0.3, ease: "expo.out"}}, {t_resultat - 0.05:.3f});')

# ------------------------------------------------------------------ titre d'accroche (haut)
scenes.append(f'<div class="clip" id="hook" data-start="0" data-duration="{MAIN_END:.2f}" data-track-index="2" '
              'style="position:absolute; left:0; top:190px; width:1080px; text-align:center">'
              '<div class="h2 stroke" id="hk1" style="font-size:58px">EN FUT CHAMPIONS, TOUT LE MONDE JOUE EN</div>'
              '<div class="h1 acc stroke" id="hk2" style="font-size:150px; margin-top:6px">4-3-1-2 ?!</div></div>')
pop("#hk1", 0.05, fr="y: -80, opacity: 0", ease="back.out(2)", name="whoosh", vol=0.3)
pop("#hk2", 0.25, fr="scale: 2.4, opacity: 0", d=0.22, ease="power4.in", name="impact", vol=0.45)
js.append(f'  tl.fromTo("#hk2", {{rotation: 0}}, {{rotation: -3, duration: 0.12, yoyo: true, repeat: 3, immediateRender: false}}, {t_encore:.3f});')

# ------------------------------------------------------------------ compteur de 4-3-1-2 croisés
scenes.append(f'<div class="clip" id="counter" data-start="{t_encore - 0.05:.3f}" data-duration="{MAIN_END - t_encore + 0.05:.3f}" data-track-index="3" '
              'style="position:absolute; left:650px; top:1000px; transform:rotate(-4deg)">'
              '<div class="panel" style="padding:16px 26px; gap:2px; flex-direction:row; align-items:center; gap:18px">'
              '<div style="font-weight:700; font-size:28px; line-height:1.1; letter-spacing:0.06em; text-align:left">4-3-1-2<br/>CROISÉS</div>'
              '<div class="h1 acc" id="cnt" style="font-size:84px">1</div></div></div>')
pop("#counter", t_encore - 0.05, fr="scale: 0, rotation: -30", ease="back.out(3)", name="impact", vol=0.35)
n, t = 1, t_encore + 0.6
step = 0.55
while t < t_abuse:
    n += 1 if n < 5 else (3 if n < 20 else 9)
    js.append(f'  tl.set("#cnt", {{textContent: "{n}"}}, {t:.3f});')
    js.append(f'  tl.fromTo("#cnt", {{scale: 1.4}}, {{scale: 1, duration: 0.15, immediateRender: false}}, {t:.3f});')
    sfx("click", t, 0.35, 0.06)
    t += step; step = max(0.18, step * 0.85)
js.append(f'  tl.set("#cnt", {{textContent: "∞"}}, {t_abuse:.3f});')

# ------------------------------------------------------------------ tampon « ABUSÉ »
scenes.append(f'<div class="clip" id="abuse" data-start="{t_abuse - 0.05:.3f}" data-duration="{t_toi - t_abuse:.3f}" data-track-index="4" '
              'style="position:absolute; left:0; top:560px; width:1080px; display:flex; justify-content:center">'
              '<div class="stamp" id="stampx">ABUSÉ</div></div>')
pop("#stampx", t_abuse - 0.05, fr="scale: 3, opacity: 0, rotation: -25", d=0.18, ease="power4.in", name="impact", vol=0.5)
js.append(f'  tl.fromTo("#accentflash", {{opacity: 0.55}}, {{opacity: 0, duration: 0.35, immediateRender: false}}, {t_abuse:.3f});')
js.append(f'  tl.fromTo("#broll", {{x: -22}}, {{x: 0, duration: 0.35, ease: "elastic.out(1.2, 0.3)", immediateRender: false}}, {t_abuse + 0.05:.3f});')
sfx("buzz", t_abuse - 0.05, 0.4, 0.35)

# ------------------------------------------------------------------ question finale
scenes.append(f'<div class="clip" id="ask" data-start="{t_toi - 0.05:.3f}" data-duration="{MAIN_END - t_toi + 0.05:.3f}" data-track-index="4" '
              'style="position:absolute; left:0; top:560px; width:1080px; display:flex; flex-direction:column; align-items:center; gap:24px">'
              '<div class="cta" id="askc" style="font-size:64px; white-space:nowrap">ET TOI, T\'EN CROISES COMBIEN ?</div>'
              '<span class="tag" id="askt" style="font-size:40px">Réponds en commentaire ↓</span></div>')
pop("#askc", t_toi - 0.05, fr="x: -600, opacity: 0", ease="expo.out", name="whoosh", vol=0.3)
pop("#askt", t_toi + 0.5, fr="y: 60, opacity: 0", ease="back.out(2)")

# punchs sur les temps forts
for tt, big in [(t_devine, False), (t_encore, True), (t_parait, False), (t_resultat, True)]:
    punch(tt, big=big)

# ------------------------------------------------------------------ sous-titres dynamiques
KEY = {"fut", "champions", "devine", "4-3-1-2", "meneur", "attaquants", "forte", "jeu", "abuse", "combien", "ca"}
groups, cur = [], []
for i, x in enumerate(words):
    cur.append(i)
    gap = (words[i + 1]["start"] - x["end"]) if i + 1 < len(words) else 9
    if re.search(r"[.!?,:…]$", x["text"]) or len(cur) >= 3 or gap > 0.35 or sum(len(words[k]["text"]) for k in cur) > 15:
        groups.append(cur); cur = []
if cur: groups.append(cur)
caps = []
for gi, g in enumerate(groups):
    st = max(0.0, words[g[0]]["start"] - 0.04)
    en = (words[groups[gi + 1][0]]["start"] - 0.04) if gi + 1 < len(groups) else MAIN_END
    spans = []
    for k in g:
        t_ = words[k]["text"] if words[k]["text"].startswith("4-3-1-2") else re.sub(r"[.,!?:;…]+$", "", words[k]["text"])
        key = norm(words[k]["text"]) in KEY or words[k]["text"].startswith("4-3-1-2")
        spans.append(f'<span class="{"w hl" if key else "w"}" id="w{k}">{html.escape(t_.upper())}</span>')
    caps.append(f'<div class="cap clip" id="g{gi}" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="5">{" ".join(spans)}</div>')
    js.append(f'  tl.from("#g{gi}", {{scale: 0.6, y: 30, rotation: {-3 if gi % 2 else 3}, duration: 0.16, ease: "back.out(2.5)"}}, {st:.3f});')
    for k in g:
        js.append(f'  tl.fromTo("#w{k}", {{y: -16}}, {{y: 0, duration: 0.18, ease: "back.out(3)"}}, {max(st, words[k]["start"] - 0.03):.3f});')

# ------------------------------------------------------------------ fond animé, progression, fin
js.append(f'  tl.fromTo("#progress", {{scaleX: 0}}, {{scaleX: 1, duration: {MAIN_END:.2f}, ease: "none"}}, 0);')
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN_END:.3f}" data-duration="{END_LEN}" data-track-index="6">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f'  tl.fromTo("#flash", {{opacity: 0.9}}, {{opacity: 0, duration: 0.3, immediateRender: false}}, {MAIN_END:.3f});')
js.append(f'  tl.from("#logo", {{scale: 0.6, opacity: 0, duration: 0.45, ease: "back.out(1.8)"}}, {MAIN_END + 0.05:.3f});')
sfx("impact", MAIN_END, 0.45, 0.45)

# ------------------------------------------------------------------ audio
aud = [f'<audio id="voice" class="clip" src="assets/voix_off.wav" data-start="0" data-duration="{VOICE_END + 0.2:.3f}" data-volume="1" data-track-index="0"></audio>',
       f'<audio id="game" class="clip" src="assets/game.wav" data-start="0" data-duration="{CLIP_LEN:.2f}" data-volume="0.22" data-fade-out="0.6" data-track-index="1"></audio>']
tracks = {}
for n_, (name, t_, vol, d) in enumerate(audio):
    tr = 7
    while any(not (t_ >= e or t_ + d <= s0) for s0, e in tracks.get(tr, [])):
        tr += 1
    tracks.setdefault(tr, []).append((t_, t_ + d))
    aud.append(f'<audio id="sfx{n_}" class="clip" src="assets/sfx/{name}.wav" data-start="{t_:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True)
shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
for f in ("voix_off.wav", "game.wav"):
    shutil.copy(f"{ROOT}/work/{f}", f"{A}/{f}")
shutil.copy(f"{ROOT}/work/backdrop.mp4", f"{A}/broll.mp4")
tpl = open(f"{REPO}/templates/reel-faceless/template.html").read()
brand_css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in brand_css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", f"{DUR}")
          .replace("{{STREAKS}}", "")
          .replace("{{BACKDROP}}", f'<video id="broll" class="clip" src="assets/broll.mp4" data-start="0" data-duration="{CLIP_LEN:.2f}" muted data-track-index="1"></video><div id="dim"></div>')
          .replace("{{SCENES}}", "\n        ".join(scenes))
          .replace("{{CAPTIONS}}", "\n      ".join(caps))
          .replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud))
          .replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"index.html ({BRAND}) : {DUR} s (capture {CLIP_LEN} s, voix {VOICE_END:.1f} s), {len(caps)} sous-titres")
