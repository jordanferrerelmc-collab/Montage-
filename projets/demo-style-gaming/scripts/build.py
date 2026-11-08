"""Démo du style « gaming premium » (Specimen Gaming) : TOP 3 des compos, révélations mystère.

Montre toutes les animations de templates/reel-gaming/gaming-fx.js aux couleurs de la charte.
Visuels 100 % originaux (schémas de formation), aucun élément du jeu ni du créateur de référence.
"""
import html, json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-gaming"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
TPL = f"{REPO}/templates/reel-gaming"
DUR, END = 25.0, 2.4
MAIN = DUR - END

# formation -> lignes (de la défense à l'attaque)
FORMS = {"4-2-3-1": [4, 2, 3, 1], "4-4-2": [4, 4, 2], "4-3-1-2": [4, 3, 1, 2]}

def pitch(form, sid):
    """Schéma de terrain vertical (SVG) avec les joueurs de la formation."""
    lines = FORMS[form]
    dots = ['<circle cx="50" cy="128" r="5.5" style="fill:var(--silver)"/>']          # gardien
    n = len(lines)
    for i, k in enumerate(lines):
        y = 112 - (i + 1) * (92 / (n + 0.4))
        for j in range(k):
            x = 50 if k == 1 else 14 + j * (72 / (k - 1))
            col = "var(--accent)" if i == n - 1 else "var(--ink)"
            dots.append(f'<circle class="pl" cx="{x:.1f}" cy="{y:.1f}" r="5.5" style="fill:{col}"/>')
    return (f'<svg id="{sid}" viewBox="0 0 100 140" style="width:100%; height:100%">'
            '<rect x="4" y="4" width="92" height="132" rx="6" fill="none" style="stroke:var(--silver)" stroke-width="1" opacity="0.5"/>'
            '<line x1="4" y1="70" x2="96" y2="70" style="stroke:var(--silver)" stroke-width="1" opacity="0.5"/>'
            '<circle cx="50" cy="70" r="12" fill="none" style="stroke:var(--silver)" stroke-width="1" opacity="0.5"/>'
            '<rect x="28" y="4" width="44" height="18" fill="none" style="stroke:var(--silver)" stroke-width="1" opacity="0.5"/>'
            '<rect x="28" y="118" width="44" height="18" fill="none" style="stroke:var(--silver)" stroke-width="1" opacity="0.5"/>'
            + "".join(dots) + "</svg>")

MYSTERY = ('<svg viewBox="0 0 100 136"><path d="M50 4 L94 18 V96 Q94 118 50 132 Q6 118 6 96 V18 Z" style="fill:var(--black)" '
           'stroke-width="2" opacity="0.95"/><text x="50" y="84" text-anchor="middle" font-size="52" font-weight="700" '
           'style="fill:var(--dark); font-family:var(--font)">?</text></svg>')

ICON = {
    "save": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--ink)"/></svg>',
    "like": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.5-8 11-8 11z" style="fill:var(--ink)"/></svg>',
    "sub": '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--ink)"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 1-5 4-9 10-10z" style="fill:var(--ink)"/></svg>',
    "star": '<svg viewBox="0 0 24 24" class="ico"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.8 5.5 21l2-7.5L2 9h7z" style="fill:var(--accent)"/></svg>',
}

body, js, audio = [], [], []
def sfx(name, t, vol=0.35, d=0.5):
    audio.append((name, t, vol, d))

def clip(cid, start, end, inner, cls="", style=""):
    body.append(f'<div class="clip {cls}" id="{cid}" data-start="{start:.2f}" data-duration="{end - start:.2f}" data-track-index="2" style="{style}">{inner}</div>')

# ------------------------------------------------------------------ fond, halo, signature, progression
js.append(f"  fx.breathe(tl, '#halo', 0, {MAIN});")
body.append('<div class="handle">SPECIMEN GAMING</div>')
body.append('<div class="tracker"><span class="lbl">TOP 3</span>'
            + "".join(f'<div class="slot" id="slot{i}"></div>' for i in range(3)) + "</div>")

# ------------------------------------------------------------------ intro : titre + grille CTA
clip("intro", 0, 3.2,
     '<div class="bigtitle" style="top:330px"><div class="kicker" id="ik">FUT CHAMPIONS</div>'
     '<div id="it1">Les compos</div><div id="it2">les plus <span class="acc">jouées</span></div></div>')
js.append("  fx.blurIn(tl, '#ik', 0.1);")
js.append("  fx.blurIn(tl, '#it1', 0.3);")
js.append("  fx.blurIn(tl, '#it2', 0.5);")
sfx("whoosh-long", 0.0, 0.35, 1.1)
js.append("  fx.blurOut(tl, '#intro', 1.6);")
grid = "".join(f'<div class="cta-btn">{ICON[k]}{lbl}</div>' for k, lbl in [("save", "Enregistre"), ("like", "Like"), ("sub", "Abonne-toi"), ("share", "Partage")])
clip("cta", 1.75, 3.6, f'<div class="ctagrid" id="ctag">{grid}</div><div class="ctanote" id="ctan">Reste jusqu\'au bout : le N°1 va te surprendre</div>')
js.append("  fx.ctaGrid(tl, '#ctag', 1.8, 3.25);")
js.append("  fx.blurIn(tl, '#ctan', 2.3, {blur: 10});")
js.append("  fx.blurOut(tl, '#ctan', 3.25);")
for i in range(4):
    sfx("pop", 1.8 + 0.12 * i, 0.22, 0.12)

# ------------------------------------------------------------------ étapes du classement
STEPS = [  # (rang, formation, sous-titre, badge, stats [(valeur, étiquette)], note, compteur)
    (3, "4-2-3-1", "Polyvalente", "Équilibrée", [("2", "MDC"), ("3", "MOC")], "Solide <b>au milieu</b>", 18450),
    (2, "4-4-2", "Classique", "Contre-attaque", [("4", "MILIEUX"), ("2", "ATT")], "Rapide <b>en transition</b>", 26300),
    (1, "4-3-1-2", "La plus jouée", "Partout", [("1", "MOC"), ("2", "ATT")], "Tu la croises <b>à chaque match</b>", 41900),
]
t0, SLOT = 3.6, 6.2
caps = []
for k, (rank, form, sub, badge, stats, note, count) in enumerate(STEPS):
    s = t0 + k * SLOT
    e = s + SLOT
    rv = s + 1.3                      # moment de la révélation
    sid = f"st{k}"
    statbox = "".join(f'<div class="stat" id="{sid}s{j}"><div class="v">{v}</div><div class="l">{l}</div></div>' for j, (v, l) in enumerate(stats))
    clip(sid, s, e,
         f'<div class="rank"><div class="no" id="{sid}no"><small>N°</small><b>{rank}</b></div>'
         f'<div class="txt"><div class="name" id="{sid}nm">{form}</div><div class="sub" id="{sid}sb">{sub}</div></div></div>'
         f'<div class="stagecard"><div class="ring" id="{sid}rg"></div>'
         f'<div class="mystery" id="{sid}my">{MYSTERY}</div>'
         f'<div class="cardvis" id="{sid}cv">{pitch(form, sid + "pt")}</div>'
         f'<div class="pricepill" id="{sid}pp"><span id="{sid}ct">0</span> matchs</div></div>'
         f'<div class="side"><div class="badge" id="{sid}bd">{ICON["star"]}<div><div class="bt">STYLE</div><div class="bv">{badge}</div></div></div>{statbox}</div>'
         f'<div class="note" id="{sid}nt">→ {note}</div>')
    # entrée : numéro + silhouette mystère, nom flouté
    js.append(f"  fx.blurIn(tl, '#{sid}no', {s + 0.05:.2f}, {{blur: 24, y: 0, scale: 1.2}});")
    js.append(f"  tl.fromTo('#{sid}my', {{opacity: 0, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.35, ease: 'power2.out', immediateRender: true}}, {s + 0.15:.2f});")
    js.append(f"  tl.set('#{sid}cv', {{opacity: 0}}, {s:.2f});")
    js.append(f"  tl.set('#{sid}pp', {{opacity: 0}}, {s:.2f});")
    js.append(f"  tl.fromTo('#{sid}nm', {{opacity: 0.5, filter: 'blur(22px)'}}, {{opacity: 1, filter: 'blur(0px)', duration: 0.4, ease: 'power2.out', immediateRender: true}}, {rv:.2f});")
    js.append(f"  fx.blurIn(tl, '#{sid}sb', {rv + 0.15:.2f}, {{blur: 10}});")
    # révélation : carte + onde de choc + compteur
    js.append(f"  fx.mysteryReveal(tl, '#{sid}my', '#{sid}cv', '#{sid}rg', {rv:.2f});")
    js.append(f"  tl.fromTo('#{sid}pt .pl', {{scale: 0, transformOrigin: '50% 50%'}}, {{scale: 1, duration: 0.3, ease: 'back.out(3)', stagger: 0.04, immediateRender: true}}, {rv + 0.25:.2f});")
    js.append(f"  fx.blurIn(tl, '#{sid}pp', {rv + 0.35:.2f}, {{blur: 8, y: 10}});")
    js.append(f"  fx.countUp(tl, '#{sid}ct', 0, {count}, {rv + 0.4:.2f}, 1.1);")
    sfx("impact-sec", rv, 0.45, 0.35); sfx("riser", rv - 1.2, 0.18, 1.2); sfx("ding", rv + 0.1, 0.18, 0.7)
    # colonne : badge puis stats, puis note
    js.append(f"  fx.slideBlur(tl, '#{sid}bd', {rv + 0.9:.2f}, {{x: 60}});")
    js.append(f"  fx.slideBlur(tl, '#{sid} .stat', {rv + 1.4:.2f}, {{x: 60, stagger: 0.2}});")
    js.append(f"  fx.blurIn(tl, '#{sid}nt', {rv + 2.3:.2f}, {{blur: 12, y: 16}});")
    sfx("whoosh-court", rv + 0.8, 0.18, 0.6); sfx("clic", rv + 1.4, 0.3, 0.05); sfx("clic", rv + 1.6, 0.3, 0.05)
    js.append(f"  fx.trackerFill(tl, '#slot{2 - k}', {rv:.2f});")
    js.append(f"  fx.blurOut(tl, '#{sid}', {e - 0.35:.2f});")
    caps += [(s + 0.1, f"Numéro <span class='k'>{rank}</span>"), (rv, f"<span class='k' style='margin-left:0'>{form}</span>"),
             (rv + 1.3, sub.lower())]

# ------------------------------------------------------------------ outro
o = t0 + 3 * SLOT
clip("outro", o, MAIN,
     '<div class="bigtitle" style="top:520px"><div id="ot1">Partage à ton pote</div><div id="ot2">qui joue en <span class="acc">4-3-1-2</span></div>'
     '<div class="kicker" id="ot3" style="margin-top:40px">SPECIMEN GAMING · FC</div></div>')
js.append(f"  fx.blurIn(tl, '#ot1', {o + 0.1:.2f});")
js.append(f"  fx.blurIn(tl, '#ot2', {o + 0.35:.2f});")
js.append(f"  fx.blurIn(tl, '#ot3', {o + 0.7:.2f}, {{blur: 10}});")
sfx("whoosh-long", o - 0.2, 0.3, 1.1)
caps.append((o + 0.1, "Partage <span class='k'>à ton pote</span>"))

# sous-titres (horaires fixes dans la démo ; en vrai montage : calés sur la voix off)
for i, (t, txt) in enumerate(caps):
    end = caps[i + 1][0] if i + 1 < len(caps) else MAIN
    body.append(f'<div class="cap clip" id="c{i}" data-start="{t:.2f}" data-duration="{end - t:.2f}" data-track-index="4">{txt}</div>')
    js.append(f"  fx.blurIn(tl, '#c{i}', {t:.2f}, {{blur: 10, y: 14, d: 0.25}});")

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f"  tl.fromTo('#blackout', {{opacity: 0}}, {{opacity: 1, duration: 0.3, immediateRender: false}}, {MAIN - 0.3:.2f});")
js.append(f"  fx.blurIn(tl, '#logo', {MAIN + 0.05:.2f}, {{blur: 20, y: 0, scale: 1.1, d: 0.6}});")
sfx("impact-boom", MAIN, 0.4, 0.9)

aud, tracks = [], {}
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t); tr = 6
    while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{TPL}/gaming-fx.js", f"{A}/gaming-fx.js")
tpl = open(f"{TPL}/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR))
          .replace("{{BODY}}", "\n      ".join(body)).replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"démo style gaming : {DUR} s, {len(body)} blocs, {len(aud)} sons")
