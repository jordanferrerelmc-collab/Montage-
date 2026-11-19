"""« Ajoute ton lieu » — version bulles « liquid glass » façon Apple, branding Specimen Agency.

assets/cut.mp4 : coupe serrée (scripts/cut.py, voix nettoyée). Bulles de verre dépoli translucides (flou d'arrière-plan,
reflet spéculaire, liseré lumineux, teinte or de la charte) qui apparaissent avec un rebond « liquide » : sous-titres,
cartes du script, accroche et appel à l'action. Rien sur le visage : bulles au-dessus de la tête, entre le menton et
les sous-titres, et sous-titres sur la poitrine. Coupes masquées par alternance de cadrage + flou « lentille ».
"""
import html, json, os, re, shutil, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-agency"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
words = json.load(open(f"{ROOT}/work/words_cut.json"))
W = [w["start"] for w in words]
segs = json.load(open(f"{ROOT}/work/segments.json"))
CUTS, acc = [], 0.0
for a, b in segs:
    CUTS.append(round(acc, 3)); acc += b - a
SPEECH_END = round(acc, 2)
END = 2.7
DUR = round(SPEECH_END + END, 2)

body, js, sfx = [], [], []
def spring(sel, t, d=0.55, y=30):
    """Entrée « liquide » : la bulle gonfle depuis un point, s'écrase légèrement puis se stabilise (sans flou CSS
    sur l'élément : il casserait le flou d'arrière-plan du verre)."""
    js.append(f'  tl.fromTo("{sel}", {{opacity: 0, scaleX: 0.55, scaleY: 0.35, y: {y}}}, {{opacity: 1, scaleX: 1, scaleY: 1, y: 0, duration: {d}, ease: "elastic.out(1, 0.62)", immediateRender: true}}, {t:.3f});')
def pop_out(sel, t):
    js.append(f'  tl.fromTo("{sel}", {{opacity: 1, scaleX: 1, scaleY: 1}}, {{opacity: 0, scaleX: 0.85, scaleY: 0.7, duration: 0.18, ease: "power2.in", immediateRender: false}}, {t:.3f});')

# ------------------------------------------------------------------ vidéo : coupes masquées (cadrage alterné), poussée lente
body.append(f'<div id="cam"><video id="v" class="clip" src="assets/cut.mp4" data-start="0" data-duration="{SPEECH_END}" '
            'data-has-audio="true" data-volume="1" data-track-index="0"></video></div>')
body.append('<div id="lens"></div>')
for k, t in enumerate(CUTS):
    nxt = CUTS[k + 1] if k + 1 < len(CUTS) else SPEECH_END
    z = 1.0 if k % 2 == 0 else 1.07
    js.append(f'  tl.fromTo("#cam", {{scale: {z:.3f}}}, {{scale: {z * 1.025:.3f}, duration: {nxt - t:.3f}, ease: "none", immediateRender: {"true" if k == 0 else "false"}}}, {t:.3f});')
    if k:   # « lentille » de verre sur la coupe : bref flou + reflet, pas de flash dur
        js.append(f'  tl.fromTo("#cam", {{filter: "blur(4px) brightness(1.05)"}}, {{filter: "blur(0px) brightness(1)", duration: 0.15, ease: "power2.out", immediateRender: false}}, {t:.3f});')
        js.append(f'  tl.fromTo("#lens", {{opacity: 0.35}}, {{opacity: 0, duration: 0.2, ease: "sine.out", immediateRender: false}}, {t:.3f});')

# ------------------------------------------------------------------ sous-titres dans une bulle de verre (1 à 3 mots)
fix = {22: "astuce :", 31: "géolocalisation.", 39: "légende,", 43: "« boulangerie", 45: "Saint-Denis »", 71: "Enregistre"}
keys = {2, 4, 9, 16, 22, 28, 31, 34, 37, 39, 43, 45, 51, 54, 56, 62, 65, 69, 70, 73, 78, 81}
glue = {"quand", "tu", "sans", "où", "la", "ne", "pas", "à", "qui", "te", "et", "petite", "chaque", "ajoute", "le", "ta", "ou", "ton",
        "en", "avec", "par", "de", "dans", "sur", "c'est", "ça", "prend", "un", "deux"}
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
    a = max(0.0, W[g[0]] - 0.04)
    b = (W[groups[k + 1][0]] - 0.04) if k + 1 < len(groups) else SPEECH_END
    label = " ".join(f"<span class='kw'>{html.escape(txt(i))}</span>" if i in keys else html.escape(txt(i)) for i in g)
    body.append(f'<div class="capwrap clip" id="c{k}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="4">'
                f'<div class="glass cap" id="cb{k}">{label}</div></div>')
    js.append(f'  tl.fromTo("#cb{k}", {{opacity: 0, scale: 0.86, y: 10}}, {{opacity: 1, scale: 1, y: 0, duration: 0.22, ease: "back.out(2.2)", immediateRender: true}}, {a:.3f});')

# ------------------------------------------------------------------ accroche : grande bulle au-dessus de la tête
HOOK_END = W[8] - 0.05
body.append(f'<div class="topwrap clip" id="hook" data-start="0" data-duration="{HOOK_END:.2f}" data-track-index="2">'
            '<div class="glass big" id="hb"><span class="eyebrow">SPECIMEN AGENCY</span>Tes futurs clients<br/><b>sont à côté</b></div></div>')
spring("#hb", 0.05, 0.7, -30)
pop_out("#hb", HOOK_END - 0.2)
sfx.append(("tic-flutter", 0.05, 0.2, 0.7))

# ------------------------------------------------------------------ bulles du script (entre le menton et les sous-titres)
PIN = ('<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7z" style="fill:var(--accent)"/>'
       '<circle cx="12" cy="9" r="2.6" style="fill:var(--black)"/></svg>')
TXT = '<svg viewBox="0 0 24 24"><path d="M4 5h16M4 10h16M4 15h10" fill="none" style="stroke:var(--accent)" stroke-width="2.6" stroke-linecap="round"/></svg>'
EYE = ('<svg viewBox="0 0 24 24"><path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" fill="none" style="stroke:var(--accent)" stroke-width="2.2"/>'
       '<circle cx="12" cy="12" r="3" style="fill:var(--accent)"/></svg>')
BOLT = '<svg viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7z" style="fill:var(--accent)"/></svg>'
SAVE = ('<svg viewBox="0 0 24 24"><path d="M4 3h13l3 3v15H4z" style="fill:var(--black)"/>'
        '<rect x="7" y="3" width="9" height="6" style="fill:var(--ivory)"/><rect x="7" y="13" width="10" height="6" rx="1" style="fill:var(--ivory)"/></svg>')
def bubble(n, a, b, icon, title, sub="", cls=""):
    inner = (f'<span class="ico">{icon}</span>' if icon else "") + f'<span class="tx"><span class="t">{title}</span>' + (f'<span class="s">{sub}</span>' if sub else "") + "</span>"
    body.append(f'<div class="midwrap clip" id="n{n}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="3">'
                f'<div class="glass note {cls}" id="nb{n}">{inner}</div></div>')
    spring(f"#nb{n}", a + 0.02)
    pop_out(f"#nb{n}", b - 0.18)
    sfx.append(("ui", a + 0.02, 0.2, 0.5))

bubble(0, W[8] - 0.05, W[21] - 0.08, EYE, "Sans lieu =", "pas de clientèle de proximité")
bubble(1, W[26] - 0.05, W[32] - 0.08, PIN, "<i>1</i> Ajoute le lieu", "géolocalisation à chaque publication")
bubble(2, W[32] + 0.1, W[42] - 0.08, TXT, "<i>2</i> Ville + métier", "dans la légende")
bubble(3, W[42] - 0.05, W[46] - 0.08, "", "boulangerie à Saint-Denis", "", cls="msg")
bubble(4, W[46] + 0.05, W[60] - 0.08, TXT, "<i>2</i> Ville + métier", "dans la légende")
bubble(5, W[64] - 0.05, W[71] - 0.08, BOLT, "Gratuit.", "2 secondes.")
bubble(6, W[71] - 0.05, SPEECH_END, SAVE, "Enregistre + partage", "à un commerçant", cls="gold")
sfx.append(("impact-grave", W[69], 0.14, 1.2))

# ------------------------------------------------------------------ écran de fin (charte)
tag = brand.get("tagline")
endcard = (f'<div class="clip" id="endcard" data-start="{SPEECH_END}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/>'
           + (f'<div id="tagline">{"<br/>".join(p.strip() + "." for p in tag.rstrip(".").split("."))}</div>' if tag else "") + "</div>")
js.append(f'  tl.fromTo("#cam", {{filter: "blur(0px)"}}, {{filter: "blur(18px)", duration: 0.3, ease: "power2.in", immediateRender: false}}, {SPEECH_END - 0.3:.3f});')
js.append(f'  tl.fromTo("#logo", {{opacity: 0, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.7, ease: "power3.out", immediateRender: true}}, {SPEECH_END + 0.05:.3f});')
if tag:
    js.append(f'  tl.fromTo("#tagline", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.6, ease: "power3.out", immediateRender: true}}, {SPEECH_END + 0.5:.3f});')
sfx.append(("whoosh-court", SPEECH_END - 0.25, 0.14, 0.5))

# ------------------------------------------------------------------ ressources (sons du pack utilisateur s'ils sont là, sinon maison)
A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True); os.makedirs(f"{A}/sfx", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
FALLBACK = {"ui": "pop", "impact-grave": "impact-sec", "tic-flutter": "pop"}
for n in {s[0] for s in sfx}:
    u = f"{REPO}/effets/sfx/utilisateur/{n}.wav"
    shutil.copy(u if os.path.exists(u) else f"{REPO}/effets/sfx/{FALLBACK.get(n, n)}.wav", f"{A}/sfx/{n}.wav")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/video1/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")
def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
aud = [f'<audio id="s{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{round(min(d, length(name)), 3)}" '
       f'data-volume="{v}" data-track-index="{6 + n % 3}"></audio>' for n, (name, t, v, d) in enumerate(sfx)]

css = open(f"{BRAND_DIR}/brand.css").read()
page = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <meta name="brand" content="{BRAND}" />
    <meta name="montage-style" content="liquid-glass-apple" />
    <script src="assets/gsap.min.js"></script>
    <style>
{chr(10).join("      " + l for l in css.splitlines())}

      /* ---- bulles « liquid glass » (façon Apple), teinte or de la charte ---- */
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font); }}
      #cam {{ position: absolute; inset: 0; transform-origin: 50% 58%; }}
      #cam video {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #lens {{ position: absolute; inset: 0; opacity: 0; pointer-events: none;
        background: radial-gradient(ellipse 75% 55% at 50% 45%, rgba(255, 255, 255, 0.5) 0%, rgba(255, 255, 255, 0) 100%); }}
      .glass {{ position: relative; color: var(--ink); border-radius: 999px;
        background: linear-gradient(160deg, rgba(255, 255, 255, 0.22) 0%, rgba(11, 11, 13, 0.30) 42%, rgba(11, 11, 13, 0.42) 100%);
        backdrop-filter: blur(30px) saturate(160%) brightness(0.82); -webkit-backdrop-filter: blur(30px) saturate(160%) brightness(0.82);
        border: 1.5px solid rgba(255, 255, 255, 0.55);
        box-shadow: inset 0 2px 1px rgba(255, 255, 255, 0.75), inset 0 -2px 6px rgba(255, 255, 255, 0.18),
          inset 0 0 22px rgba(255, 255, 255, 0.12), 0 18px 46px rgba(0, 0, 0, 0.28);
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.45); }}
      .glass::after {{ content: ""; position: absolute; left: 8%; right: 8%; top: 5%; height: 38%; border-radius: 999px; pointer-events: none;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.42) 0%, rgba(255, 255, 255, 0) 100%); }}
      .topwrap, .midwrap, .capwrap {{ position: absolute; left: var(--cap-left); width: var(--cap-width); display: flex; justify-content: center; }}
      .topwrap {{ top: 120px; }}
      .midwrap {{ top: 1215px; }}
      .capwrap {{ top: 1470px; }}
      /* sous-titres : blancs à contour noir léger, mots clés en or */
      .cap {{ padding: 16px 38px; font-weight: 700; font-size: 64px; letter-spacing: -0.015em; white-space: nowrap;
        -webkit-text-stroke: 5px rgba(0, 0, 0, 0.55); paint-order: stroke fill; }}
      .cap .kw {{ color: var(--gold-light); }}
      /* accroche */
      .big {{ border-radius: 58px; padding: 34px 64px 42px; text-align: center; font-weight: 700; font-size: 84px; line-height: 1.05; letter-spacing: -0.03em; }}
      .big b {{ color: var(--gold-light); font-weight: 700; }}
      .eyebrow {{ display: block; font-size: 26px; letter-spacing: 0.3em; margin-bottom: 14px; color: var(--ivory); opacity: 0.85; }}
      /* bulles du script, façon notification */
      .note {{ display: flex; align-items: center; gap: 22px; border-radius: 40px; padding: 22px 40px 22px 24px; white-space: nowrap; }}
      .note .ico {{ width: 82px; height: 82px; border-radius: 24px; flex: none; display: flex; align-items: center; justify-content: center;
        background: rgba(11, 11, 13, 0.55); border: 1.5px solid rgba(255, 255, 255, 0.35); }}
      .note .ico svg {{ width: 50px; height: 50px; }}
      .note .tx {{ display: flex; flex-direction: column; gap: 4px; }}
      .note .t {{ font-weight: 700; font-size: 48px; letter-spacing: -0.02em; }}
      .note .t i {{ font-style: normal; display: inline-flex; align-items: center; justify-content: center; width: 54px; height: 54px; margin-right: 10px;
        border-radius: 50%; background: var(--accent); color: var(--black); font-size: 34px; text-shadow: none; vertical-align: 4px; }}
      .note .s {{ font-weight: 700; font-size: 38px; color: var(--ivory); opacity: 0.92; }}
      .note.msg {{ border-radius: 40px 40px 40px 10px; padding: 24px 44px; }}
      .note.msg .t {{ font-size: 50px; }}
      .note.gold {{ background: linear-gradient(160deg, rgba(242, 213, 142, 0.85) 0%, rgba(227, 178, 92, 0.78) 100%); color: var(--black);
        text-shadow: none; border-color: rgba(255, 255, 255, 0.7); }}
      .note.gold .s {{ color: var(--black); }}
      .note.gold .ico {{ background: rgba(255, 255, 255, 0.35); }}
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
print(f"liquid glass : {DUR} s, {len(CUTS)} plans, {len(groups)} sous-titres, {len(aud)} sons")
