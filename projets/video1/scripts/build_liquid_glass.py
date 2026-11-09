"""Test du style « Vidéo liquide glass » (references/video-liquide-glass) sur video1 → montage-liquid/index.html.

Mesures de l'original : accroche face caméra ~3,6 s avec poussée lente, mots en italique blancs qui
apparaissent / disparaissent en flou, un mot géant en « verre » coloré derrière la tête, puis transition
en flou plein cadre + impact grave, et coupes franches sur le rythme (bruitage aigu sur les coupes).
"""
import html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = os.environ.get("BRAND", "specimen-agency")
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
words = json.load(open(f"{ROOT}/work/words_cut.json"))
W = {i: w["start"] for i, w in enumerate(words)}
OUT = f"{ROOT}/montage-liquid"

SPEECH_END = 26.05
DUR = 28.8
GLASS = {
    "specimen-agency": "linear-gradient(100deg, var(--black) 0%, var(--gold-deep) 28%, var(--ivory) 50%, var(--gold-deep) 72%, var(--black) 100%)",
    "specimen-gaming": "linear-gradient(100deg, var(--red-dark) 0%, var(--red) 28%, var(--ink) 50%, var(--red) 72%, var(--red-dark) 100%)",
}[BRAND]

js, behind, caps, sfx = [], [], [], []

def blur_in(sel, t, d=0.22, blur=16, y=0, scale=1.0):
    js.append(f'  tl.fromTo("{sel}", {{opacity: 0, filter: "blur({blur}px)", y: {y}, scale: {scale}}}, '
              f'{{opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: {d}, ease: "power2.out", immediateRender: true}}, {t:.3f});')

def blur_out(sel, t, d=0.16, blur=14):
    js.append(f'  tl.to("{sel}", {{opacity: 0, filter: "blur({blur}px)", duration: {d}, ease: "power1.in"}}, {t:.3f});')

# ------------------------------------------------------------------ sections, poussée lente, transitions « lentille »
sections = [0.0, 3.86, 8.27, 10.61, 13.50, 14.95, 18.66, 22.27, 24.17]
framing = [1.00, 1.10, 1.02, 1.12, 1.04, 1.10, 1.02, 1.12, 1.04]
for k, t in enumerate(sections):
    nxt = sections[k + 1] if k + 1 < len(sections) else SPEECH_END
    z = framing[k]
    # poussée continue (l'original : ~ +12 % sur l'accroche)
    js.append(f'  tl.fromTo("#push", {{scale: {z:.3f}}}, {{scale: {z * 1.06:.3f}, duration: {nxt - t:.3f}, ease: "none", immediateRender: {"true" if k == 0 else "false"}}}, {t:.3f});')
    if k:
        # flou plein cadre 0,22 s avant la coupe → net 0,25 s après
        js.append(f'  tl.fromTo("#cam", {{filter: "blur(0px) brightness(1)"}}, {{filter: "blur(22px) brightness(1.12)", duration: 0.22, ease: "power2.in", immediateRender: false}}, {t - 0.22:.3f});')
        js.append(f'  tl.fromTo("#cam", {{filter: "blur(22px) brightness(1.12)"}}, {{filter: "blur(0px) brightness(1)", duration: 0.28, ease: "power2.out", immediateRender: false}}, {t:.3f});')
        js.append(f'  tl.fromTo("#lens", {{opacity: 0}}, {{opacity: 0.7, duration: 0.2, ease: "sine.in", immediateRender: false}}, {t - 0.2:.3f});')
        js.append(f'  tl.to("#lens", {{opacity: 0, duration: 0.3, ease: "sine.out"}}, {t:.3f});')
        sfx.append(("whoosh-court", t - 0.12, 0.16, 0.6))
sfx.append(("impact-boom", sections[1] - 0.04, 0.32, 0.9))   # le « drop » de l'original (fin de l'accroche)

# ------------------------------------------------------------------ mots géants en verre, derrière la tête
titles = [  # (début, fin, petite ligne haute, mot géant, petite ligne basse, haut en px)
    (0.0, W[6] - 0.05, "tes vidéos", "200", "vues", 110),
    (W[24] - 0.05, sections[3] - 0.25, "non, c'est", "faux", "", 140),
    (W[36] - 0.05, sections[4] - 0.25, "je commence par le", "résultat", "", 140),
    (W[73] - 0.05, sections[8] - 0.25, "il n'y a pas de", "secret", "", 140),
]
covered = []
for n, (a, b, top, big, bot, y) in enumerate(titles):
    size = min(300, int(1150 / max(3, len(big))))
    tid = f"g{n}"
    behind.append(
        f'<div class="glass-title clip" id="{tid}" style="top:{y}px; --glass-fill: {GLASS}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="2">'
        f'<span class="it top" id="{tid}t">{html.escape(top)}</span>'
        f'<span class="glass" id="{tid}g" style="font-size:{size}px">{html.escape(big)}</span>'
        + (f'<span class="it bot" id="{tid}b">{html.escape(bot)}</span>' if bot else "") + "</div>")
    blur_in(f"#{tid}t", a + 0.02)
    blur_in(f"#{tid}g", a + 0.14, d=0.32, blur=26, scale=1.12)
    if bot:
        blur_in(f"#{tid}b", a + 0.45)
    js.append(f'  tl.fromTo("#{tid}g", {{backgroundPosition: "0% 50%"}}, {{backgroundPosition: "100% 50%", duration: {b - a:.3f}, ease: "none", immediateRender: true}}, {a:.3f});')
    blur_out(f"#{tid}", b - 0.18)
    covered.append((a, b))

# ------------------------------------------------------------------ sous-titres italiques (1 à 3 mots), flou entrant / sortant
fix = {4: "200", 19: "« bonjour,", 23: "de… »", 41: "1.", 43: "/ après", 44: "2.", 58: "3.", 79: "envoie"}
keys = {9, 26, 40, 42, 43, 49, 55, 63, 66, 78, 83}
glue = {"le", "la", "les", "de", "du", "un", "une", "à", "a", "ce", "je", "tu", "il", "y", "n'y", "en", "et", "ou",
        "si", "par", "que", "qui", "pas", "c'est", "n'est", "font", "tes", "tous", "soit", "ça"}

def txt(i):
    t = fix.get(i, words[i]["text"])
    return t if i in fix else re.sub(r"[.,]$", "", t)

groups, cur = [], []
for i in range(len(words)):
    cur.append(i)
    joined = " ".join(txt(k) for k in cur)
    if txt(i).lower() in glue and len(cur) < 3 and len(joined) < 14 and i + 1 < len(words):
        continue
    groups.append(cur); cur = []
if cur: groups.append(cur)

ROWS = [1270, 1310]          # deux hauteurs qui alternent, comme les mots qui « montent » dans l'original
n = 0
for gi, g in enumerate(groups):
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[gi + 1][0]] - 0.04) if gi + 1 < len(groups) else SPEECH_END
    if any(ca - 0.01 <= a < cb for ca, cb in covered):
        continue                                    # le titre en verre porte déjà ces mots
    label = " ".join(f"<span class='k'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    caps.append(f'<div class="lg-cap it clip" id="c{n}" style="top:{ROWS[n % 2]}px" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="4">{label}</div>')
    blur_in(f"#c{n}", a, d=0.16, blur=12, y=10)
    if b - a > 0.45:
        blur_out(f"#c{n}", b - 0.12, d=0.12, blur=10)
    n += 1

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{SPEECH_END}" data-duration="{DUR - SPEECH_END:.2f}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f'  tl.fromTo("#cam", {{filter: "blur(0px) brightness(1)"}}, {{filter: "blur(26px) brightness(1.15)", duration: 0.3, ease: "power2.in", immediateRender: false}}, {SPEECH_END - 0.3:.3f});')
js.append(f'  tl.fromTo("#logo", {{opacity: 0, scale: 1.08, filter: "blur(20px)"}}, {{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power3.out", immediateRender: true}}, {SPEECH_END + 0.05:.3f});')
sfx.append(("impact-sec", SPEECH_END, 0.3, 0.5))

sfx_html = [f'<audio id="sfx{k}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{d}" '
            f'data-volume="{v}" data-track-index="{6 + k % 2}"></audio>' for k, (name, t, v, d) in enumerate(sfx)]

# ------------------------------------------------------------------ assemblage
A = f"{OUT}/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
for f in ("cut.mp4", "subject.webm"):
    if not os.path.exists(f"{A}/{f}"):
        os.link(f"{ROOT}/montage/assets/{f}", f"{A}/{f}")
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{ROOT}/montage/hyperframes.json", f"{OUT}/hyperframes.json")
tpl = open(f"{REPO}/templates/reel-liquid-glass/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", f"{DUR}").replace("{{SUBJECT_DUR}}", "26.0")
          .replace("{{SOFTEN}}", "block").replace("{{BEHIND}}", "\n        ".join(behind)).replace("{{BROLL}}", "")
          .replace("{{CAPTIONS}}", "\n      ".join(caps)).replace("{{ENDCARD}}", endcard)
          .replace("{{SFX}}", "\n    ".join(sfx_html)).replace("{{JS}}", "\n".join(js)))
open(f"{OUT}/index.html", "w").write(out)
print(f"liquid glass ({BRAND}) : {len(caps)} sous-titres, {len(behind)} mots en verre, {len(sfx_html)} sons")
