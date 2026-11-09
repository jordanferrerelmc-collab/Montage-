"""Générateur des démos d'application aux couleurs Specimen (skill html-demo adapté).

Usage dans un projet (projets/<nom>/scripts/build.py) :

    import sys; sys.path.insert(0, f"{REPO}/templates/app-demo")
    from build_app_demo import build
    build(root=ROOT, brand="specimen-gaming", steps_js=f"{ROOT}/scripts/steps.js",
          kicker="SPECIMEN GAMING · TACTIQUE", title="Ma 4-3-1-2<br><span class='a'>en 4 étapes</span>",
          tabs=["Tactiques", "4-3-1-2"], label="Tactique", images={"thumb.jpg": "/chemin/image.jpg"})

steps.js définit `const STEPS = [...]` (API html-demo : id, name, dur, html, draw(t, $)) et, en plus :
  say    : sous-titre affiché pendant l'étape (HTML, mots clés dans <span class='a'>) ;
  clicks : instants (s, relatifs à l'étape) des clics → bruitage « clic » ;
  keys   : [[début, fin], …] des frappes au clavier → bruitage « frappe-clavier ».
Les durées et les sons sont lus dans steps.js (source unique) avec node.
"""
import html, json, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
# colonne utile de chaque marque (gauche, largeur) : TikTok évite la colonne d'icônes à droite
LAYOUT = {"specimen-agency": (90, 900), "specimen-gaming": (110, 860)}   # colonne centrée, marges égales

STUB = "const ease=()=>0,typed=()=>'',cue=()=>0,held=()=>false,glide=()=>({});"


def read_steps(path):
    src = open(path).read()
    code = (STUB + src + ";console.log(JSON.stringify(STEPS.map(s=>({name:s.name,dur:s.dur,"
            "say:s.say||'',clicks:s.clicks||[],keys:s.keys||[]}))))")
    return src, json.loads(subprocess.check_output(["node", "-e", code], text=True))


def build(root, brand, steps_js, kicker, title, tabs, label, images=None,
          win_in=0.7, start=1.3, hold=0.8, end=2.4, extra_sfx=()):
    """Écrit root/montage/index.html et copie les ressources. Renvoie la durée totale."""
    spec = json.load(open(f"{REPO}/brand/{brand}/brand.json"))
    src, steps = read_steps(steps_js)
    total = sum(s["dur"] for s in steps)
    main = start + total + hold
    dur = round(main + end, 2)
    left, width = LAYOUT[brand]
    win_l, win_w, win_t = left - 20, width + 40, 600
    win_h = win_w * 750 / 1200 + 60 + 100           # scène + barre de titre + barre d'étapes
    say_t = int(win_t + win_h + 50)

    js, says, audio = [], [], []
    last_say = ""

    def sfx(name, t, vol=0.3, d=0.4):
        audio.append((name, t, vol, d))

    sfx("whoosh-long", 0.0, 0.3, 1.1)
    sfx("montee-ui", win_in, 0.25, 0.6)
    acc = start
    for i, s in enumerate(steps):
        a, b = acc, acc + s["dur"]
        if s["say"]:
            sid = f"say{i}"
            says.append(f'<div class="say clip" id="{sid}" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="3">{s["say"]}</div>')
            js.append(f'      blurIn("#{sid}", {a + 0.05:.2f}, {{ d: 0.35 }});')
            last_say = f", #{sid}"
            if i < len(steps) - 1:
                js.append(f'      blurOut("#{sid}", {b - 0.3:.2f});')
        for c in s["clicks"]:
            sfx("clic", a + c, 0.4, 0.15)
        for k0, k1 in s["keys"]:
            sfx("frappe-clavier", a + k0, 0.22, round(k1 - k0, 2))
        if i:
            sfx("whoosh-court", a - 0.05, 0.14, 0.5)
        acc = b
    sfx("validation", start + total - 0.1, 0.25, 0.8)
    for e in extra_sfx:
        sfx(*e)

    # sortie : fondu au noir, logo
    js.append(f'      blurOut("#head, #win{last_say}", {main - 0.45:.2f});')
    js.append(f'      tl.fromTo("#blackout", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, immediateRender: false }}, {main - 0.3:.2f});')
    js.append(f'      tl.fromTo("#logo", {{ opacity: 0, scale: 1.1, filter: "blur(20px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power3.out", immediateRender: true }}, {main + 0.05:.2f});')
    sfx("impact-boom", main, 0.35, 0.9)
    endcard = (f'<div class="clip" id="endcard" data-start="{main:.2f}" data-duration="{end}" data-track-index="5">'
               f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(spec["name"])}"/></div>')

    import wave
    def length(name):
        with wave.open(f"{REPO}/effets/sfx/{name}.wav") as w:
            return w.getnframes() / w.getframerate()

    aud, tracks = [], {}
    for n, (name, t, vol, d) in enumerate(audio):
        t = max(0.0, t); tr = 6
        d = round(min(d, length(name)), 3)
        while any(not (t >= e2 or t + d <= s2) for s2, e2 in tracks.get(tr, [])):
            tr += 1
        tracks.setdefault(tr, []).append((t, t + d))
        aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

    # ressources
    m = f"{root}/montage"
    A = f"{m}/assets"
    os.makedirs(f"{A}/brand", exist_ok=True)
    shutil.copy(f"{REPO}/brand/{brand}/{spec['logo']}", f"{A}/brand/logo.png")
    shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{REPO}/brand/{brand}/fonts", f"{A}/brand/fonts")
    shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx")
    shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
    for f in ("step-window.js", "step-window.css", "specimen-window.css", "app-demo.js"):
        shutil.copy(f"{HERE}/{f}", f"{A}/{f}")
    for dst, srcf in (images or {}).items():
        shutil.copy(srcf, f"{A}/{dst}")
    if not os.path.exists(f"{m}/hyperframes.json"):
        shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", f"{m}/hyperframes.json")

    css = open(f"{REPO}/brand/{brand}/brand.css").read()
    rep = {
        "{{BRAND_CSS}}": "\n".join("      " + l for l in css.splitlines()),
        "{{BRAND}}": brand, "{{DUR}}": str(dur), "{{KICKER}}": kicker, "{{TITLE}}": title,
        "{{LEFT}}": str(left), "{{WIDTH}}": str(width), "{{HEAD_TOP}}": "260",
        "{{WIN_LEFT}}": str(win_l), "{{WIN_TOP}}": str(win_t), "{{WIN_W}}": str(win_w), "{{SAY_TOP}}": str(say_t),
        "{{SAYS}}": "\n      ".join(says), "{{ENDCARD}}": endcard, "{{AUDIO}}": "\n    ".join(aud),
        "{{STEPS_JS}}": "\n".join("      " + l for l in src.strip().splitlines()),
        "{{TABS}}": json.dumps(tabs, ensure_ascii=False), "{{LABEL}}": json.dumps(label, ensure_ascii=False),
        "{{WIN_START}}": str(start), "{{WIN_IN}}": str(win_in), "{{HALO_REPEAT}}": str(int(dur / 1.6)),
        "{{JS}}": "\n".join(js),
    }
    out = open(f"{HERE}/template.html").read()
    for k, v in rep.items():
        out = out.replace(k, v)
    open(f"{m}/index.html", "w").write(out)
    print(f"démo {brand} : {dur} s, {len(steps)} étapes, {len(aud)} sons → {m}/index.html")
    return dur
