"""« Ajoute ton lieu » — Reel Specimen Agency, style éditorial (templates/reel-editorial), script minuté de l'utilisateur.

Son : voix nettoyée (scripts/clean-voice.sh) dans assets/cut.mp4 (scripts/cut.sh : blancs et 2e prise retirés).
Grands titres derrière la tête (sujet détouré), cartes du script entre le menton et les sous-titres (jamais sur le visage
ni sur les sous-titres), sous-titres mot à mot blancs à contour noir, halos doux sur les coupes, CTA doré, logo de fin.
"""
import html, json, os, re, shutil, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-agency"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
words = json.load(open(f"{ROOT}/work/words_cut.json"))
W = [w["start"] for w in words]
SPEECH_END = 30.47
END = 2.7
DUR = round(SPEECH_END + END, 2)
JOINS = [11.33, 18.57, 23.17]                     # raccords de scripts/cut.sh

js, caps_html, behind, cards, sfx = [], [], [], [], []

# ------------------------------------------------------------------ sous-titres mot à mot (1 à 3 mots), blancs à contour noir
fix = {22: "astuce :", 31: "géolocalisation.", 39: "légende,", 43: "« boulangerie", 45: "Saint-Denis »", 69: "deux", 71: "Enregistre"}
keys = {2, 4, 9, 16, 22, 28, 31, 34, 37, 39, 43, 45, 51, 54, 56, 62, 65, 69, 70, 73, 78, 81}
glue = {"quand", "tu", "sans", "où", "la", "ne", "pas", "à", "qui", "te", "et", "petite", "chaque", "ajoute", "le", "ta", "ou", "ton",
        "en", "avec", "par", "de", "dans", "sur", "c'est", "ça", "prend", "un"}
def txt(i):
    t = fix.get(i, words[i]["text"])
    return t if i in fix else re.sub(r"[.,?!]$", "", t)
groups, cur = [], []
for i in range(len(words)):
    cur.append(i)
    joined = " ".join(txt(k) for k in cur)
    if words[i]["text"].lower().strip(".,") in glue and len(cur) < 3 and len(joined) < 15 and i + 1 < len(words):
        continue
    groups.append(cur); cur = []
if cur: groups.append(cur)
for k, g in enumerate(groups):
    start = max(0.0, W[g[0]] - 0.04)
    end = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else SPEECH_END
    label = " ".join(f"<span class='kw'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    caps_html.append(f'<div class="cap clip" id="c{k}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="4">{label}</div>')
    js.append(f'  tl.fromTo("#c{k}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: 0.12, ease: "power2.out", immediateRender: true}}, {start:.3f});')

# ------------------------------------------------------------------ cadrage : zooms lents ancrés au menton, halos doux sur les coupes
sections = [0.0, W[21], JOINS[0], JOINS[1], JOINS[2], W[71]]
framing = [1.00, 1.08, 1.02, 1.10, 1.03, 1.08]
for k, t in enumerate(sections):
    nxt = sections[k + 1] if k + 1 < len(sections) else SPEECH_END
    z = framing[k]
    if k:
        js.append(f'  tl.fromTo("#bloom", {{opacity: 0}}, {{opacity: 0.7, duration: 0.16, ease: "sine.in", immediateRender: false}}, {t - 0.16:.3f});')
        js.append(f'  tl.fromTo("#bloom", {{opacity: 0.7}}, {{opacity: 0, duration: 0.34, ease: "sine.out", immediateRender: false}}, {t:.3f});')
        sfx.append(("whoosh-court", t - 0.2, 0.12, 0.5))
    js.append(f'  tl.fromTo("#cam", {{scale: {z:.3f}}}, {{scale: {z * 1.04:.3f}, duration: {nxt - t:.3f}, ease: "none", immediateRender: {"true" if k == 0 else "false"}}}, {t:.3f});')
# micro-saut discret sur « Saint-Denis » et « deux secondes »
for t in (W[45], W[69]):
    js.append(f'  tl.fromTo("#punch", {{scale: 1.0}}, {{scale: 1.045, duration: 0.08, ease: "power1.out", immediateRender: false}}, {t:.3f});')
    js.append(f'  tl.fromTo("#punch", {{scale: 1.045}}, {{scale: 1.0, duration: 0.35, ease: "power2.out", immediateRender: false}}, {t + 0.5:.3f});')

# ------------------------------------------------------------------ grands titres derrière la tête (or → blanc)
def title(n, start, end, small, big, top=40):
    size = min(190, int(1250 / max(4, len(big))))
    behind.append(f'<div class="behind clip" id="t{n}" style="--title-top:{top}px" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="2">'
                  f'<span class="small">{html.escape(small)}</span><span class="huge" style="font-size:{size}px; color:var(--accent)">{html.escape(big)}</span></div>')
    js.append(f'  tl.fromTo("#t{n} .small", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: true}}, {start:.3f});')
    js.append(f'  tl.fromTo("#t{n} .huge", {{opacity: 0, scale: 1.12}}, {{opacity: 1, scale: 1, duration: 0.35, ease: "power3.out", immediateRender: true}}, {start + 0.08:.3f});')
    js.append(f'  tl.set("#t{n} .huge", {{color: "var(--ink)"}}, {start + 0.7:.3f});')     # or → blanc (bascule nette)
    js.append(f'  tl.fromTo("#t{n}", {{opacity: 1}}, {{opacity: 0, duration: 0.2, immediateRender: false}}, {end - 0.2:.3f});')

title(0, 0.0, W[8] - 0.05, "tes futurs clients", "SONT À CÔTÉ")         # accroche
title(1, W[21], W[26] - 0.1, "petite", "ASTUCE")
title(2, W[64], W[71] - 0.15, "c'est", "GRATUIT")

# ------------------------------------------------------------------ cartes du script (entre le menton et les sous-titres)
def card(n, start, end, inner, light=False, cta=False, wrap=False):
    cls = ("pill-cta" if cta else ("note light" if light else "note")) + (" wrap" if wrap else "")
    cards.append(f'<div class="{cls} clip" id="k{n}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">{inner}</div>')
    js.append(f'  tl.fromTo("#k{n}", {{opacity: 0, y: 40, scale: 0.92}}, {{opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "back.out(1.6)", immediateRender: true}}, {start:.3f});')
    js.append(f'  tl.fromTo("#k{n}", {{opacity: 1}}, {{opacity: 0, duration: 0.2, immediateRender: false}}, {end - 0.2:.3f});')
    sfx.append(("ui", start, 0.22, 0.5))

PIN = ('<svg class="ico" viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7z" style="fill:var(--accent)"/>'
       '<circle cx="12" cy="9" r="2.6" style="fill:var(--black)"/></svg>')                   # 📍 aux couleurs de la charte
SAVE = ('<svg class="ico" viewBox="0 0 24 24"><path d="M4 3h13l3 3v15H4z" style="fill:var(--black)"/>'
        '<rect x="7" y="3" width="9" height="6" style="fill:var(--ivory)"/><rect x="7" y="13" width="10" height="6" rx="1" style="fill:var(--ivory)"/></svg>')
card(0, W[8] - 0.05, W[21] - 0.1, "Sans lieu = <b>pas de clientèle</b><br/>de proximité", wrap=True)
card(1, W[26] - 0.05, JOINS[0] - 0.1, "<span class='num'>1</span> Ajoute le lieu " + PIN)
card(2, JOINS[0] + 0.15, W[42] - 0.1, "<span class='num'>2</span> Ville + métier dans la légende")
card(3, W[42] - 0.05, JOINS[1] - 0.1, "« boulangerie à Saint-Denis »", light=True)
card(4, JOINS[1] + 0.15, JOINS[2] - 0.1, "<span class='num'>2</span> Ville + métier dans la légende")
card(5, JOINS[2] + 0.15, W[71] - 0.1, "Gratuit. <b>2 secondes.</b>")
card(6, W[71] - 0.05, SPEECH_END, SAVE + "<span>Enregistre + partage<br/>à un commerçant</span>", cta=True)
sfx.append(("impact-grave", W[69], 0.16, 1.2))          # « deux secondes » : impact grave discret

# ------------------------------------------------------------------ écran de fin
tag = brand.get("tagline")
endcard = (f'<div class="clip" id="endcard" data-start="{SPEECH_END}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/>'
           + (f'<div id="tagline">{"<br/>".join(p.strip() + "." for p in tag.rstrip(".").split("."))}</div>' if tag else "") + "</div>")
js.append(f'  tl.fromTo("#bloom", {{opacity: 0}}, {{opacity: 0.9, duration: 0.2, immediateRender: false}}, {SPEECH_END - 0.2:.3f});')
js.append(f'  tl.fromTo("#bloom", {{opacity: 0.9}}, {{opacity: 0, duration: 0.5, immediateRender: false}}, {SPEECH_END:.3f});')
js.append(f'  tl.fromTo("#logo", {{opacity: 0, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.7, ease: "power3.out", immediateRender: true}}, {SPEECH_END + 0.05:.3f});')
if tag:
    js.append(f'  tl.fromTo("#tagline", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.6, ease: "power3.out", immediateRender: true}}, {SPEECH_END + 0.5:.3f});')
sfx.append(("whoosh-court", SPEECH_END - 0.2, 0.14, 0.5))

# ------------------------------------------------------------------ ressources
A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True); os.makedirs(f"{A}/sfx", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
SRC = {"whoosh-court": f"{REPO}/effets/sfx/whoosh-court.wav"}
for n in ("ui", "impact-grave"):                         # sons fournis par l'utilisateur (non versionnés) ; repli : maison
    u = f"{REPO}/effets/sfx/utilisateur/{n}.wav"
    SRC[n] = u if os.path.exists(u) else f"{REPO}/effets/sfx/{'pop' if n == 'ui' else 'impact-sec'}.wav"
for n, p in SRC.items():
    shutil.copy(p, f"{A}/sfx/{n}.wav")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/video1/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")
def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
sfx_html = [f'<audio id="sfx{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{round(min(d, length(name)), 3)}" '
            f'data-volume="{v}" data-track-index="{6 + n % 3}"></audio>' for n, (name, t, v, d) in enumerate(sfx)]

EXTRA_CSS = """
      /* visage : zooms ancrés au menton ; rien sur le visage ni sur les sous-titres */
      #root #cam, #root #punch { transform-origin: 50% 58%; }
      #root .behind .small { font-size: 58px; }
      /* sous-titres blancs à contour noir, centrés, mots clés en or */
      #root .cap { top: 1470px; left: var(--cap-left); width: var(--cap-width); height: 110px; font-size: 72px;
        -webkit-text-stroke: 10px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 4px 18px rgba(0, 0, 0, 0.55); }
      #root .cap .kw { color: var(--accent-soft, var(--accent)); margin: 0 0.22em; }
      /* cartes du script : bande entre le menton et les sous-titres */
      .note, .pill-cta { position: absolute; left: 50%; top: 1270px; transform: translateX(-50%); max-width: var(--cap-width);
        display: flex; align-items: center; justify-content: center; gap: 18px; padding: 22px 36px; border-radius: 30px; white-space: nowrap;
        font-weight: 700; font-size: 42px; letter-spacing: -0.01em; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4); }
      .note { background: var(--panel); color: var(--ink); border: 3px solid var(--accent); }
      .note b { color: var(--accent-soft, var(--accent)); font-weight: 700; }
      .note.light { background: var(--ivory); color: var(--black); }
      .note .num { display: inline-flex; align-items: center; justify-content: center; width: 60px; height: 60px; border-radius: 50%;
        background: var(--accent); color: var(--black); font-size: 38px; flex: none; }
      .note.wrap { display: block; text-align: center; line-height: 1.25; }
      .pill-cta span { text-align: left; line-height: 1.15; }
      .note .ico, .pill-cta .ico { width: 56px; height: 56px; flex: none; }
      .pill-cta { border-radius: 999px; background: var(--gold-grad); color: var(--black); font-size: 40px; padding: 24px 40px; }
"""
tpl = open(f"{REPO}/templates/reel-editorial/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()) + EXTRA_CSS)
          .replace("{{BRAND}}", BRAND)
          .replace('src="assets/cut.mp4" data-start="0" data-duration="{{DUR}}"', f'src="assets/cut.mp4" data-start="0" data-duration="{SPEECH_END}"')
          .replace("{{DUR}}", f"{DUR}").replace("{{SUBJECT_DUR}}", f"{SPEECH_END}").replace("{{SOFTEN}}", "none")
          .replace("{{BEHIND}}", "\n        ".join(behind)).replace("{{CARDS}}", "\n      ".join(cards))
          .replace("{{CAPTIONS}}", "\n      ".join(caps_html)).replace("{{ENDCARD}}", endcard)
          .replace("{{SFX}}", "\n    ".join(sfx_html)).replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"ajoute ton lieu : {DUR} s, {len(groups)} sous-titres, {len(behind)} titres, {len(cards)} cartes, {len(sfx_html)} sons")
