"""« Reste authentique » — Reel Specimen Agency, style éditorial (templates/reel-editorial).

Son : voix nettoyée par scripts/clean_voice.sh (RNNoise + égalisation voix), déjà dans assets/cut.mp4.
Sujet détouré (assets/subject.webm) pour les grands titres derrière la tête. Sous-titres centrés sous le menton
(jamais sur le visage), zooms ancrés au menton, halos doux entre les parties, écran de fin avec le logo.
"""
import html, json, os, shutil, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-agency"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
SPEECH_END = 16.66
END = 2.7
DUR = round(SPEECH_END + END, 2)

# Sous-titres : texte relu à la main (la voix, enregistrée en voiture, est mal reconnue par la transcription) ;
# horaires = ceux de la transcription « large-v3-turbo » sur la voix nettoyée. (début, texte, mot clé ?)
CAPS = [(0.30, "Pourquoi", 0), (0.61, "on m'a pas", 0), (1.21, "appris ça", 0), (1.64, "plus tôt ?", 1), (2.41, "Pourquoi ?", 1),
        (3.13, "Les gars,", 0), (3.74, "ce qui fait que", 0), (4.31, "cette entreprise", 0), (5.31, "fonctionne,", 1), (6.23, "ou cette", 0),
        (7.07, "marque,", 0), (8.00, "ou peu importe :", 0), (8.60, "reste", 0), (9.03, "authentique", 1), (10.03, "N'invente pas", 0),
        (10.68, "une", 0), (10.93, "personnalité,", 1), (11.88, "reste", 0), (12.41, "comme tu es.", 1), (13.02, "Et le travail", 0),
        (13.60, "va payer", 1), (13.99, "naturellement.", 0), (14.96, "Abandonne pas,", 1), (15.73, "et sois", 0), (16.15, "le meilleur.", 1)]

js, caps_html, behind, sfx = [], [], [], []
for k, (t, label, key) in enumerate(CAPS):
    end = CAPS[k + 1][0] - 0.04 if k + 1 < len(CAPS) else SPEECH_END
    start = max(0.0, t - 0.04)
    caps_html.append(f'<div class="cap clip{" key" if key else ""}" id="c{k}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                     f'data-track-index="4">{html.escape(label)}</div>')
    js.append(f'  tl.fromTo("#c{k}", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: 0.12, ease: "power2.out", immediateRender: true}}, {start:.3f});')

# ------------------------------------------------------------------ cadrage : zooms lents, halos doux entre les parties
sections = [0.0, 3.13, 8.60, 10.03, 13.02, 14.96]
framing = [1.00, 1.08, 1.00, 1.10, 1.02, 1.10]
for k, t in enumerate(sections):
    nxt = sections[k + 1] if k + 1 < len(sections) else SPEECH_END
    z = framing[k]
    if k:
        js.append(f'  tl.fromTo("#bloom", {{opacity: 0}}, {{opacity: 0.75, duration: 0.16, ease: "sine.in", immediateRender: false}}, {t - 0.16:.3f});')
        js.append(f'  tl.fromTo("#bloom", {{opacity: 0.75}}, {{opacity: 0, duration: 0.34, ease: "sine.out", immediateRender: false}}, {t:.3f});')
        sfx.append(("whoosh-court", t - 0.2, 0.12, 0.5))
    js.append(f'  tl.fromTo("#cam", {{scale: {z:.3f}}}, {{scale: {z * 1.04:.3f}, duration: {nxt - t:.3f}, ease: "none", immediateRender: {"true" if k == 0 else "false"}}}, {t:.3f});')
# micro-saut discret sur le second « Pourquoi ? »
js.append('  tl.fromTo("#punch", {scale: 1.0}, {scale: 1.045, duration: 0.08, ease: "power1.out", immediateRender: false}, 2.41);')
js.append('  tl.fromTo("#punch", {scale: 1.045}, {scale: 1.0, duration: 0.3, ease: "power2.out", immediateRender: false}, 3.0);')

# ------------------------------------------------------------------ grands titres derrière la tête (or → blanc)
def title(n, start, end, small, big, top=230):
    size = min(200, int(1250 / max(4, len(big))))
    behind.append(f'<div class="behind clip" id="t{n}" style="--title-top:{top}px" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="2">'
                  f'<span class="small">{html.escape(small)}</span><span class="huge" style="font-size:{size}px">{html.escape(big)}</span></div>')
    js.append(f'  tl.fromTo("#t{n} .small", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: true}}, {start:.3f});')
    js.append(f'  tl.fromTo("#t{n} .huge", {{opacity: 0, scale: 1.12}}, {{opacity: 1, scale: 1, duration: 0.35, ease: "power3.out", immediateRender: true}}, {start + 0.08:.3f});')
    js.append(f'  tl.fromTo("#t{n} .huge", {{color: "var(--accent)"}}, {{color: "var(--ink)", duration: 0.5, ease: "none", immediateRender: false}}, {start + 0.6:.3f});')
    js.append(f'  tl.fromTo("#t{n}", {{opacity: 1}}, {{opacity: 0, duration: 0.2, immediateRender: false}}, {end - 0.2:.3f});')

title(0, 0.30, 3.05, "pourquoi on m'a pas appris ça", "plus tôt ?")
title(1, 8.60, 9.95, "reste", "authentique")
title(2, 13.02, 14.90, "le travail va", "payer")
title(3, 15.73, SPEECH_END, "et sois", "le meilleur")

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

A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx", ignore=shutil.ignore_patterns("reactions", "openverse"))
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
if not os.path.exists(f"{ROOT}/montage/hyperframes.json"):
    shutil.copy(f"{REPO}/projets/video1/montage/hyperframes.json", f"{ROOT}/montage/hyperframes.json")
def length(name):
    with wave.open(f"{A}/sfx/{name}.wav") as w:
        return w.getnframes() / w.getframerate()
sfx_html = [f'<audio id="sfx{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{round(min(d, length(name)), 3)}" '
            f'data-volume="{v}" data-track-index="{6 + n % 2}"></audio>' for n, (name, t, v, d) in enumerate(sfx)]

# règles propres à ce montage (spécificité #root : passent après celles du modèle)
EXTRA_CSS = """
      /* visage : sous-titres sous le menton, zooms ancrés au menton (le visage ne descend pas sur le texte) */
      #root #cam, #root #punch { transform-origin: 50% 58%; }
      #root .cap { top: 1330px; left: var(--cap-left); width: var(--cap-width); font-size: 72px;
        -webkit-text-stroke: 10px rgba(0, 0, 0, 0.9); paint-order: stroke fill; text-shadow: 0 4px 18px rgba(0, 0, 0, 0.6); }
      #root .cap.key { font-size: 84px; color: var(--accent-soft, var(--accent)); }
"""
tpl = open(f"{REPO}/templates/reel-editorial/template.html").read()
css = open(f"{BRAND_DIR}/brand.css").read()
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()) + EXTRA_CSS)
          .replace("{{BRAND}}", BRAND)
          .replace('src="assets/cut.mp4" data-start="0" data-duration="{{DUR}}"', f'src="assets/cut.mp4" data-start="0" data-duration="{SPEECH_END}"')
          .replace("{{DUR}}", f"{DUR}").replace("{{SUBJECT_DUR}}", f"{SPEECH_END}").replace("{{SOFTEN}}", "none")
          .replace("{{BEHIND}}", "\n        ".join(behind)).replace("{{CARDS}}", "")
          .replace("{{CAPTIONS}}", "\n      ".join(caps_html)).replace("{{ENDCARD}}", endcard)
          .replace("{{SFX}}", "\n    ".join(sfx_html)).replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"reste authentique : {DUR} s, {len(CAPS)} sous-titres, {len(behind)} titres, {len(sfx_html)} sons")
