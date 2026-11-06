"""Génère montage/index.html (HyperFrames) à partir de la transcription recalée."""
import json, html, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = os.environ.get("BRAND", "specimen-agency")            # charte verrouillée par défaut
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
words = json.load(open(f"{ROOT}/work/words_cut.json"))
SPEECH_END = 26.05  # fin de la vidéo parlée
DUR = 28.6          # + écran de fin avec le logo

# --- corrections de texte (index du mot -> texte affiché) ---
fix = {19: "« BONJOUR,", 23: "DE… »", 41: "1.", 42: "AVANT", 43: "/ APRÈS", 44: "2.", 58: "3."}
def label(i):
    t = fix.get(i, words[i]["text"])
    if i not in fix:
        t = re.sub(r"[.,]$", "", t)
    return t.upper()

# groupes de sous-titres : (premier mot, dernier mot, {mot: classe couleur})
groups = [
    (0, 2, {2: "hl-pink"}), (3, 5, {4: "hl-red", 5: "hl-red"}), (6, 9, {9: "hl-red"}), (10, 11, {11: "hl-yellow"}),
    (12, 15, {}), (16, 18, {}), (19, 23, {}),
    (24, 26, {26: "hl-red"}), (27, 31, {}),
    (32, 35, {}), (36, 40, {40: "hl-green"}),
    (41, 43, {41: "hl-yellow", 42: "hl-yellow", 43: "hl-yellow"}),
    (44, 46, {44: "hl-yellow", 46: "hl-pink"}), (47, 49, {49: "hl-pink"}), (50, 53, {}), (54, 55, {55: "hl-green"}),
    (56, 58, {58: "hl-yellow"}), (59, 61, {}), (62, 63, {63: "hl-pink"}), (64, 66, {66: "hl-pink"}), (67, 68, {}),
    (69, 72, {72: "hl-green"}), (73, 78, {78: "hl-yellow"}),
    (79, 83, {83: "hl-pink"}), (84, 86, {86: "hl-yellow"}),
]

LEAD = 0.05  # le texte apparaît très légèrement avant la voix
caps_html, caps_js = [], []
for gi, (a, b, hl) in enumerate(groups):
    start = max(0.0, words[a]["start"] - LEAD)
    end = (words[groups[gi + 1][0]]["start"] - LEAD) if gi + 1 < len(groups) else SPEECH_END
    spans = []
    for i in range(a, b + 1):
        cls = "w " + hl.get(i, "")
        spans.append(f'<span class="{cls.strip()}" id="w{i}">{html.escape(label(i))}</span>')
    caps_html.append(f'<div class="cap clip" id="g{gi}" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                     f'data-track-index="2">{" ".join(spans)}</div>')
    caps_js.append(f'  tl.fromTo("#g{gi}", {{scale: 0.6, y: 30}}, {{scale: 1, y: 0, duration: 0.22, ease: "back.out(2.5)"}}, {start:.3f});')
    for i in range(a, b + 1):
        ws = max(start, words[i]["start"] - LEAD)
        caps_js.append(f'  tl.fromTo("#w{i}", {{y: -16}}, {{y: 0, duration: 0.2, ease: "back.out(3)"}}, {ws:.3f});')

# --- transitions : (temps, cadrage) — flash blanc + zoom « whip » ---
sections = [(0.0, 1.00), (3.86, 1.20), (8.27, 1.00), (10.61, 1.16), (13.50, 1.00), (14.95, 1.22),
            (18.66, 1.04), (22.27, 1.20), (24.17, 1.00)]
micro = [1.98, 3.24, 4.40, 4.80, 9.52, 16.30, 20.30]   # micro-coupes : petit saut de cadrage
trans_js, sfx_html = [], []
for k, (t, z) in enumerate(sections):
    nxt = sections[k + 1][0] if k + 1 < len(sections) else SPEECH_END
    trans_js.append(f'  tl.fromTo("#cam", {{scale: {z * 1.18:.3f}, rotation: {(-1.5 if k % 2 else 1.5)}}}, '
                    f'{{scale: {z:.3f}, rotation: 0, duration: 0.32, ease: "expo.out"}}, {t:.3f});')
    trans_js.append(f'  tl.to("#cam", {{scale: {z * 1.05:.3f}, duration: {nxt - t - 0.32:.3f}, ease: "none"}}, {t + 0.32:.3f});')
    trans_js.append(f'  tl.fromTo("#flash", {{opacity: 0.9}}, {{opacity: 0, duration: 0.2, ease: "power2.out"}}, {t:.3f});')
    if k:
        sfx_html.append(f'<audio class="clip" src="assets/sfx/whoosh.wav" data-start="{max(0, t - 0.18):.3f}" data-duration="0.45" data-volume="0.35" data-track-index="5"></audio>')
for n, t in enumerate(micro):
    trans_js.append(f'  tl.to("#punch", {{scale: {1.07 if n % 2 == 0 else 1.0}, duration: 0.1, ease: "power2.out"}}, {t:.3f});')

def pop(t, vol=0.4):
    sfx_html.append(f'<audio class="clip" src="assets/sfx/pop.wav" data-start="{t:.3f}" data-duration="0.12" data-volume="{vol}" data-track-index="6"></audio>')

W = {x: words[x]["start"] for x in range(len(words))}

# --- illustrations (zone haute) ---
ill = []
def card(id_, start, end, inner, cls=""):
    ill.append(f'<div class="ill clip {cls}" id="{id_}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">{inner}</div>')

EYE = '<svg viewBox="0 0 64 64" class="ico"><path d="M4 32s10-18 28-18 28 18 28 18-10 18-28 18S4 32 4 32z" fill="none" style="stroke:var(--ink)" stroke-width="5"/><circle cx="32" cy="32" r="9" style="fill:var(--ink)"/></svg>'
card("i-views", W[4] - 0.1, W[6] - 0.05,
     f'<div class="panel">{EYE}<div class="big"><span id="cnt">200</span> <small>vues</small></div>'
     '<svg viewBox="0 0 300 90" class="spark"><polyline id="sparkline" points="0,20 60,35 120,30 180,60 240,70 300,82" fill="none" style="stroke:var(--gold)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg></div>')
card("i-algo", W[8] - 0.05, W[10] - 0.05,
     '<div class="panel"><div class="chip">ALGO</div><svg viewBox="0 0 100 100" class="xmark"><path d="M15 15L85 85M85 15L15 85" style="stroke:var(--gold)" stroke-width="16" stroke-linecap="round"/></svg></div>')
card("i-arrow", W[10] - 0.05, sections[1][0],
     '<svg viewBox="0 0 100 140" class="arrow"><path d="M50 5v100M15 75l35 40 35-40" fill="none" style="stroke:var(--gold)" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>')
card("i-timer", sections[1][0] + 0.1, W[19] - 0.05,
     '<div class="panel row"><svg viewBox="0 0 64 64" class="ico"><circle cx="32" cy="36" r="22" fill="none" style="stroke:var(--ink)" stroke-width="5"/><path d="M32 36V22M26 6h12" style="stroke:var(--ink)" stroke-width="5" stroke-linecap="round"/></svg>'
     '<div><div class="kicker">TU AS</div><div class="big"><span class="num" id="n3">3</span> <small>SECONDES</small></div></div></div>')
card("i-bubble", W[19] - 0.05, sections[2][0],
     '<div class="bubble">Bonjour, je vais parler de…</div><div class="zzz" id="zzz">Z<sup>z</sup><sup><sup>z</sup></sup></div>')
card("i-faux", W[26] - 0.08, sections[3][0], '<div class="stamp" id="stamp">FAUX</div>')
card("i-method", sections[3][0] + 0.1, W[36] + 0.1,
     '<div class="panel row"><svg viewBox="0 0 64 64" class="ico"><path d="M36 4L12 36h18l-4 24 26-34H34z" style="fill:var(--gold)"/></svg><div class="big">MA MÉTHODE</div></div>')
card("i-result", W[36] + 0.1, sections[4][0],
     '<div class="panel row green"><svg viewBox="0 0 64 64" class="ico"><path d="M18 8h28v14a14 14 0 0 1-28 0zM18 12H8v6a10 10 0 0 0 10 10M46 12h10v6a10 10 0 0 1-10 10M32 36v10M22 56h20M26 46h12v10H26z" fill="none" style="stroke:var(--ink)" stroke-width="5" stroke-linejoin="round"/></svg><div class="big">LE RÉSULTAT<br><small>D\'ABORD</small></div></div>')
card("i-step1", sections[4][0], sections[5][0],
     '<div class="steprow"><div class="num-badge">1</div><div class="ba"><div class="half before"><span>AVANT</span>'
     '<svg viewBox="0 0 100 50"><polyline points="0,40 50,38 100,41" fill="none" style="stroke:var(--taupe)" stroke-width="6"/></svg></div>'
     '<div class="half after" id="after"><span>APRÈS</span><svg viewBox="0 0 100 50"><polyline points="0,45 40,32 70,20 100,4" fill="none" style="stroke:var(--gold-light)" stroke-width="7" stroke-linecap="round"/></svg></div></div></div>')
bars = "".join(f'<i class="bar {"gap" if k in (2, 3, 6, 7) else ""}" style="height:{h}px"></i>'
               for k, h in enumerate([60, 110, 8, 8, 90, 140, 8, 8, 100, 70, 120]))
card("i-step2", sections[5][0], sections[6][0],
     f'<div class="steprow"><div class="num-badge">2</div><div class="panel col"><div class="wave" id="wave">{bars}</div>'
     '<div class="kicker">ZÉRO BLANC</div></div></div>'
     '<svg viewBox="0 0 64 64" class="scissors" id="sc"><circle cx="16" cy="48" r="9" fill="none" style="stroke:var(--ink)" stroke-width="5"/><circle cx="16" cy="16" r="9" fill="none" style="stroke:var(--ink)" stroke-width="5"/><path d="M23 42L58 10M23 22l35 32" style="stroke:var(--ink)" stroke-width="5" stroke-linecap="round"/></svg>')
card("i-step3", sections[6][0], sections[7][0],
     '<div class="steprow"><div class="num-badge">3</div><div class="icons">'
     '<div class="eng" id="e-com"><svg viewBox="0 0 64 64" class="ico"><path d="M8 12h48v32H28l-12 10V44H8z" style="fill:var(--ink)"/></svg><b>+128</b></div>'
     '<div class="eng" id="e-share"><svg viewBox="0 0 64 64" class="ico"><path d="M6 30L58 8 44 58 32 36z" style="fill:var(--ink)"/></svg><b>+54</b></div></div></div>')
card("i-secret", sections[7][0], sections[8][0],
     '<div class="panel row green"><svg viewBox="0 0 64 64" class="ico"><path d="M12 34l14 14 26-30" fill="none" style="stroke:var(--ink)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
     '<div class="chart">' + "".join(f'<i class="cbar" style="height:{h}px"></i>' for h in (30, 50, 75, 105, 140)) + '</div></div>')
card("i-cta", sections[8][0], SPEECH_END,
     '<div class="cta" id="cta"><svg viewBox="0 0 64 64" class="ico plane" id="plane"><path d="M6 30L58 8 44 58 32 36z" style="fill:var(--black)"/></svg>ENVOIE À UN POTE</div>')

ill_js = f'''
  // vues : le compteur tremble, la courbe s'effondre
  tl.from("#i-views", {{scale: 0.5, opacity: 0, duration: 0.25, ease: "back.out(2)"}}, {W[4] - 0.1:.3f});
  tl.fromTo("#sparkline", {{strokeDasharray: 1, strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: 0.8, ease: "power2.out"}}, {W[4]:.3f});
  tl.from("#i-algo", {{scale: 0.5, opacity: 0, duration: 0.2, ease: "back.out(2)"}}, {W[8] - 0.05:.3f});
  tl.from("#i-algo .xmark", {{scale: 2.2, opacity: 0, duration: 0.2, ease: "power3.in"}}, {W[9]:.3f});
  tl.from("#i-arrow", {{y: -60, opacity: 0, duration: 0.18}}, {W[10] - 0.05:.3f});
  tl.to("#i-arrow", {{y: 25, duration: 0.18, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {W[10] + 0.15:.3f});
  tl.from("#i-timer", {{x: -500, duration: 0.3, ease: "expo.out"}}, {sections[1][0] + 0.1:.3f});
  tl.from("#i-bubble .bubble", {{scale: 0.3, opacity: 0, transformOrigin: "20% 100%", duration: 0.25, ease: "back.out(2)"}}, {W[19] - 0.05:.3f});
  tl.from("#zzz", {{y: 40, opacity: 0, duration: 0.5}}, {W[21]:.3f});
  tl.from("#stamp", {{scale: 3, opacity: 0, rotation: -25, duration: 0.18, ease: "power4.in"}}, {W[26] - 0.08:.3f});
  tl.fromTo("#punch", {{x: -18}}, {{x: 0, duration: 0.3, ease: "elastic.out(1.2, 0.3)"}}, {W[26] + 0.1:.3f});
  tl.fromTo("#redflash", {{opacity: 0.55}}, {{opacity: 0, duration: 0.35, immediateRender: false}}, {W[26] + 0.1:.3f});
  tl.from("#i-method", {{y: -80, opacity: 0, duration: 0.25, ease: "back.out(2)"}}, {sections[3][0] + 0.1:.3f});
  tl.from("#i-result", {{scale: 0.4, opacity: 0, duration: 0.25, ease: "back.out(2.5)"}}, {W[36] + 0.1:.3f});
  tl.fromTo("#i-result .panel", {{scale: 1.15}}, {{scale: 1, duration: 0.3, ease: "back.out(3)"}}, {W[40] - 0.05:.3f});
  tl.from("#i-step1 .num-badge", {{scale: 0, duration: 0.2, ease: "back.out(3)"}}, {sections[4][0] + 0.05:.3f});
  tl.from("#i-step1 .before", {{x: -300, opacity: 0, duration: 0.25, ease: "expo.out"}}, {W[42] - 0.05:.3f});
  tl.from("#after", {{x: 300, opacity: 0, duration: 0.25, ease: "expo.out"}}, {W[43] - 0.05:.3f});
  tl.from("#i-step2 .num-badge", {{scale: 0, duration: 0.2, ease: "back.out(3)"}}, {sections[5][0] + 0.05:.3f});
  tl.from("#i-step2 .panel", {{x: 400, opacity: 0, duration: 0.28, ease: "expo.out"}}, {sections[5][0] + 0.1:.3f});
  tl.fromTo("#sc", {{x: -420, rotation: -20}}, {{x: 420, rotation: 10, duration: 0.6, ease: "power2.inOut"}}, {W[46]:.3f});
  tl.to("#wave .gap", {{scaleX: 0, duration: 0.3, ease: "power3.in"}}, {W[49]:.3f});
  tl.from("#i-step3 .num-badge", {{scale: 0, duration: 0.2, ease: "back.out(3)"}}, {sections[6][0] + 0.05:.3f});
  tl.from("#e-com", {{scale: 0, duration: 0.25, ease: "back.out(3)"}}, {W[63] - 0.05:.3f});
  tl.from("#e-share", {{scale: 0, duration: 0.25, ease: "back.out(3)"}}, {W[66] - 0.05:.3f});
  tl.to(["#e-com", "#e-share"], {{y: -12, duration: 0.2, yoyo: true, repeat: 1}}, {W[68]:.3f});
  tl.from("#i-secret", {{scale: 0.4, opacity: 0, duration: 0.25, ease: "back.out(2.5)"}}, {sections[7][0] + 0.05:.3f});
  tl.from("#i-secret .cbar", {{scaleY: 0, transformOrigin: "50% 100%", stagger: 0.08, duration: 0.3, ease: "back.out(2)"}}, {sections[7][0] + 0.15:.3f});
  tl.from("#cta", {{y: -200, opacity: 0, duration: 0.3, ease: "back.out(2)"}}, {sections[8][0] + 0.05:.3f});
  tl.to("#cta", {{scale: 1.06, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {sections[8][0] + 0.4:.3f});
  tl.fromTo("#plane", {{x: 0, y: 0}}, {{x: 14, y: -10, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {sections[8][0] + 0.4:.3f});
'''
# 3 → 2 → 1 (compte à rebours)
tstart = sections[1][0] + 0.4
for k, n in enumerate(["3", "2", "1"]):
    ill_js += f'  tl.set("#n3", {{textContent: "{n}"}}, {tstart + k * 0.8:.3f});\n'
    ill_js += f'  tl.fromTo("#n3", {{scale: 1.5}}, {{scale: 1, duration: 0.2}}, {tstart + k * 0.8:.3f});\n'

for t in [W[4] - 0.1, W[8] - 0.05, W[19] - 0.05, W[36] + 0.1, W[42] - 0.05, W[43] - 0.05, W[63] - 0.05, W[66] - 0.05,
          sections[7][0] + 0.05, sections[8][0] + 0.05]:
    pop(t)
sfx_html.append(f'<audio class="clip" src="assets/sfx/buzz.wav" data-start="{W[26] - 0.05:.3f}" data-duration="0.35" data-volume="0.45" data-track-index="7"></audio>')
sfx_html.append(f'<audio class="clip" src="assets/sfx/impact.wav" data-start="{W[26] - 0.05:.3f}" data-duration="0.45" data-volume="0.5" data-track-index="8"></audio>')
sfx_html.append(f'<audio class="clip" src="assets/sfx/ding.wav" data-start="{W[40]:.3f}" data-duration="0.6" data-volume="0.3" data-track-index="7"></audio>')
sfx_html.append(f'<audio class="clip" src="assets/sfx/whoosh.wav" data-start="{W[46]:.3f}" data-duration="0.45" data-volume="0.3" data-track-index="7"></audio>')

endcard = (f'<div class="clip" id="endcard" data-start="{SPEECH_END}" data-duration="{DUR - SPEECH_END:.2f}" data-track-index="4">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{brand["name"]}"/>'
           f'<div id="tagline">{"<br/>".join(p.strip() + "." for p in brand["tagline"].rstrip(".").split("."))}</div></div>')
ill_js += f'''
  // écran de fin Specimen Agency
  tl.fromTo("#flash", {{opacity: 0.9}}, {{opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false}}, {SPEECH_END:.3f});
  tl.from("#logo", {{scale: 0.6, opacity: 0, rotation: -8, duration: 0.6, ease: "back.out(1.6)"}}, {SPEECH_END + 0.05:.3f});
  tl.from("#tagline", {{y: 40, opacity: 0, duration: 0.5, ease: "power3.out"}}, {SPEECH_END + 0.5:.3f});
  tl.fromTo("#logo", {{scale: 1}}, {{scale: 1.04, duration: {DUR - SPEECH_END - 0.65:.2f}, ease: "none", immediateRender: false}}, {SPEECH_END + 0.65:.3f});
'''
sfx_html.append(f'<audio class="clip" src="assets/sfx/whoosh.wav" data-start="{SPEECH_END - 0.15:.3f}" data-duration="0.45" data-volume="0.35" data-track-index="5"></audio>')
sfx_html.append(f'<audio class="clip" src="assets/sfx/ding.wav" data-start="{SPEECH_END + 0.5:.3f}" data-duration="0.6" data-volume="0.3" data-track-index="6"></audio>')
sfx_html = [h.replace('<audio ', f'<audio id="sfx{n}" ', 1) for n, h in enumerate(sfx_html)]
tpl = open(f"{REPO}/templates/reel-vertical/template.html").read()
brand_css = open(f"{BRAND_DIR}/brand.css").read()
tpl = tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in brand_css.splitlines()))
os.makedirs(f"{ROOT}/montage/assets/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{ROOT}/montage/assets/brand/logo.png")
shutil.copytree(f"{BRAND_DIR}/fonts", f"{ROOT}/montage/assets/brand/fonts", dirs_exist_ok=True)
out = (tpl.replace("{{DUR}}", f"{DUR}")
          .replace("{{CAPTIONS}}", "\n      ".join(caps_html) + "\n      " + endcard)
          .replace("{{ILLUSTRATIONS}}", "\n      ".join(ill))
          .replace("{{SFX}}", "\n    ".join(sfx_html))
          .replace("{{JS}}", "\n".join(trans_js + caps_js) + ill_js))
open(f"{ROOT}/montage/index.html", "w").write(out)
print("index.html écrit :", len(groups), "groupes de sous-titres,", len(ill), "illustrations,", len(sfx_html), "sons")
