"""Bibliothèque du style « motion design clair » (templates/reel-motion) — voir README.md.

    import sys; sys.path.insert(0, f"{REPO}/templates/reel-motion"); from motion import Motion
    m = Motion(REPO, ROOT, BRAND)                          # BRAND = specimen-agency | specimen-gaming
    m.scene("s1", 0.0, 1.5)                                # ouvre un clip (scène) : tout ce qui suit va dedans
    m.say("s1", [(0.06, "Trois", "kw"), (0.25, "mots", ""), (1.15, "vues.", "pill")], end=1.45)
    m.add('<div class="slot" style="top:430px;height:900px"><div class="phone" id="ph">…</div></div>')
    m.pop("#ph", 0.0); m.bob("#ph", 0.5, 1.5)
    m.through(1.5)                                         # transition zoom + flou entre deux parties
    m.sound("ui", 0.6, 0.2)
    m.write(main_end=19.0, voice="assets/voix.wav", voice_dur=18.76)

Toutes les animations sont des tweens GSAP déterministes (fromTo à valeurs explicites) sur une timeline en pause :
le rendu HyperFrames peut sauter à n'importe quelle image.
"""
import html, json, os, shutil, wave

HERE = os.path.dirname(os.path.abspath(__file__))

ICONS = {   # pictos maison (aucun logo tiers), couleurs = variables de la charte
    "eye": '<svg viewBox="0 0 24 24"><path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.2"/><circle cx="12" cy="12" r="3.2" style="fill:var(--mo-kw)"/></svg>',
    "up": '<svg viewBox="0 0 24 24"><path d="M4 17l6-6 4 4 6-7M14 8h6v6" fill="none" style="stroke:var(--mo-kw)" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.4-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.6-8 11-8 11z" style="fill:var(--mo-kw)"/></svg>',
    "bubble": '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z" style="fill:var(--mo-ink)"/></svg>',
    "share": '<svg viewBox="0 0 24 24"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 1-5 4-9 10-10z" style="fill:var(--mo-ink)"/></svg>',
    "text": '<svg viewBox="0 0 24 24"><path d="M5 6h14M12 6v13" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.8" stroke-linecap="round"/></svg>',
    "sync": '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3M18 3v4h-4M6 21v-4h4" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "spark": '<svg viewBox="0 0 24 24"><path d="M12 2l2.2 6.6L21 11l-6.8 2.4L12 20l-2.2-6.6L3 11l6.8-2.4z" style="fill:var(--mo-kw)"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.4"/><path d="M15.5 15.5 21 21" style="stroke:var(--mo-ink)" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "play": '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" style="fill:var(--mo-on-accent)"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z" style="fill:var(--mo-kw)"/></svg>',
}


def person(bg="var(--mo-accent)", glow="var(--mo-accent-2)", wide=False):
    """Écran de vidéo stylisé : personnage face caméra (illustration originale, couleurs de la charte).
    wide=True pour un cadre paysage (lecteur, fenêtre de montage) : le personnage reste entier."""
    if wide:
        return ('<div class="scene"><svg viewBox="0 0 160 100" preserveAspectRatio="xMidYMid slice">'
                f'<rect width="160" height="100" style="fill:{bg}"/><circle cx="128" cy="18" r="34" style="fill:{glow}" opacity="0.7"/>'
                '<circle cx="80" cy="42" r="15" style="fill:var(--mo-card)"/>'
                '<path d="M48 100c0-27 14-44 32-44s32 17 32 44z" style="fill:var(--mo-ink)"/></svg></div>')
    return ('<div class="scene"><svg viewBox="0 0 100 160" preserveAspectRatio="xMidYMid slice">'
            f'<rect width="100" height="160" style="fill:{bg}"/><circle cx="76" cy="34" r="38" style="fill:{glow}" opacity="0.7"/>'
            '<circle cx="50" cy="66" r="17" style="fill:var(--mo-card)"/>'
            '<path d="M16 160c0-31 15-54 34-54s34 23 34 54z" style="fill:var(--mo-ink)"/></svg></div>')


class Motion:
    def __init__(self, repo, root, brand):
        self.repo, self.root, self.brand = repo, root, brand
        self.brand_dir = f"{repo}/brand/{brand}"
        self.info = json.load(open(f"{self.brand_dir}/brand.json"))
        self.body, self.js, self.sfx = [], [], []
        self._open = None          # scène en cours (liste de lignes HTML)
        self.stage = []            # contenu animé par la caméra (#push / #trans), rempli par scene() / close()
        self.n = 0

    # ------------------------------------------------------------------ outils
    def uid(self, p="m"):
        self.n += 1
        return f"{p}{self.n}"

    def tw(self, sel, a, b, t, d, ease="power3.out", first=True):
        self.js.append(f'  tl.fromTo("{sel}", {a}, {{...{b}, duration: {d:.3f}, ease: "{ease}", immediateRender: {"true" if first else "false"}}}, {max(0, t):.3f});')

    def add(self, h):
        (self._open if self._open is not None else self.body).append(h)

    # ------------------------------------------------------------------ scènes (clips HyperFrames)
    def scene(self, sid, start, end):
        self.close()
        self._open = [f'<div class="clip" id="{sid}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="1">']

    def close(self):
        if self._open is not None:
            self._open.append("</div>")
            self.stage.extend(self._open)
            self._open = None

    # ------------------------------------------------------------------ entrées / sorties
    def pop(self, sel, t, d=0.55, scale=0.6, y=40, sound=None, vol=0.2):
        """Entrée signature : ressort + défloutage."""
        self.tw(sel, f'{{opacity: 0, scale: {scale}, y: {y}, filter: "blur(16px)"}}', '{opacity: 1, scale: 1, y: 0, filter: "blur(0px)"}',
                t, d, "back.out(1.7)")
        if sound:
            self.sound(sound, t - 0.02, vol)

    def out(self, sel, t, d=0.28):
        self.tw(sel, '{opacity: 1, scale: 1, filter: "blur(0px)"}', '{opacity: 0, scale: 0.9, filter: "blur(14px)"}', t, d, "power2.in", False)

    def slide(self, sel, t, dx=0, dy=60, d=0.5):
        self.tw(sel, f'{{opacity: 0, x: {dx}, y: {dy}, filter: "blur(10px)"}}', '{opacity: 1, x: 0, y: 0, filter: "blur(0px)"}', t, d, "power3.out")

    def bob(self, sel, t0, t1, amp=10, period=1.8):
        """Flottement lent (aller-retour) : les cartes « respirent » sans jamais s'arrêter."""
        half = period / 2
        rep = max(0, int((t1 - t0) / half) - 1)
        self.js.append(f'  tl.fromTo("{sel}", {{y: 0}}, {{y: {-amp}, duration: {half:.3f}, ease: "sine.inOut", repeat: {rep}, yoyo: true, '
                       f'immediateRender: false}}, {t0:.3f});')

    def shock(self, sel, t, to=1.6):
        self.tw(sel, '{opacity: 0.9, scale: 0.45}', f'{{opacity: 0, scale: {to}}}', t, 0.6, "power2.out", False)

    def tick(self, sel, t, sound=True):
        """Coche qui se dessine (pastille couleur charte)."""
        self.tw(sel, '{opacity: 0, scale: 0.4}', '{opacity: 1, scale: 1}', t, 0.4, "back.out(2.2)")
        self.tw(f"{sel} path", "{strokeDashoffset: 30}", "{strokeDashoffset: 0}", t + 0.08, 0.3, "power2.out")
        if sound:
            self.sound("validation", t, 0.14)

    def grow(self, sel, t, d=0.8, axis="scaleY"):
        self.tw(sel, f"{{{axis}: 0}}", f"{{{axis}: 1}}", t, d, "power3.out")

    def type(self, sel, text, t, cps=16):
        """Texte tapé lettre par lettre (proxy GSAP, déterministe)."""
        d = len(text) / cps
        self.js.append(f'  (function () {{ const el = document.querySelector("{sel}"), s = {json.dumps(text)}, o = {{n: 0}};'
                       f' tl.fromTo(o, {{n: 0}}, {{n: s.length, duration: {d:.3f}, ease: "none", immediateRender: true,'
                       f' onUpdate: () => {{ el.textContent = s.slice(0, Math.round(o.n)); }} }}, {t:.3f}); }})();')
        return t + d

    def count(self, sel, t, d, v0, v1, sep=" "):
        """Compteur qui défile (à n'utiliser qu'avec un VRAI chiffre donné par l'utilisateur)."""
        self.js.append(f'  (function () {{ const el = document.querySelector("{sel}"), o = {{v: {v0}}};'
                       f' tl.fromTo(o, {{v: {v0}}}, {{v: {v1}, duration: {d:.3f}, ease: "power2.out", immediateRender: true,'
                       f' onUpdate: () => {{ el.textContent = Math.round(o.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, "{sep}"); }} }}, {t:.3f}); }})();')

    # ------------------------------------------------------------------ la phrase en haut (mot à mot)
    def say(self, sid, words, end, top=None, size=None):
        """words = [(début, mot, "" | "kw" | "pill")] ; la phrase se défloute mot à mot puis s'efface à `end`."""
        st = []
        if top is not None: st.append(f"top:{top}px")
        if size is not None: st.append(f"font-size:{size}px")
        spans = []
        for k, (t, w, kind) in enumerate(words):
            wid = f"{sid}w{k}"
            if kind == "pill":
                spans.append(f'<span class="pill" id="{wid}"><i></i>{html.escape(w)}</span>')
                self.tw(f"#{wid}", '{opacity: 0, scale: 0.5, filter: "blur(12px)"}', '{opacity: 1, scale: 1, filter: "blur(0px)"}', t - 0.04, 0.45, "back.out(2)")
                self.sound("clic-focus", t - 0.04, 0.18)
            else:
                spans.append(f'<span class="sw{" kw" if kind == "kw" else ""}" id="{wid}">{html.escape(w)}</span>')
                self.tw(f"#{wid}", '{opacity: 0, y: 16, filter: "blur(10px)"}', '{opacity: 1, y: 0, filter: "blur(0px)"}', t - 0.04, 0.3, "power2.out")
        self.add(f'<div class="say" id="{sid}"{(" style=" + chr(34) + ";".join(st) + chr(34)) if st else ""}>{"".join(spans)}</div>')
        self.out(f"#{sid}", end - 0.22, 0.22)

    # ------------------------------------------------------------------ caméra
    def push(self, t0, t1, z0=1.0, z1=1.05):
        self.tw("#push", f"{{scale: {z0}}}", f"{{scale: {z1}}}", t0, t1 - t0, "none", t0 == 0)

    def through(self, t, zin=1.35):
        """Transition zoom entre deux parties : on plonge (flou), la partie suivante arrive en dézoomant."""
        self.tw("#trans", '{scale: 1, filter: "blur(0px)"}', f'{{scale: {zin}, filter: "blur(14px)"}}', t - 0.24, 0.24, "power3.in", False)
        self.tw("#trans", f'{{scale: {2 - zin * 0.8:.3f}, filter: "blur(14px)"}}', '{scale: 1, filter: "blur(0px)"}', t, 0.42, "power3.out", False)
        self.sound("whoosh-court", t - 0.22, 0.16)

    def punch(self, t, z=1.06, hold=0.5):
        """Coup de zoom sur un mot fort (fenêtre courte, jamais en même temps qu'une transition)."""
        self.tw("#trans", "{scale: 1}", f"{{scale: {z}}}", t, 0.16, "power3.out", False)
        self.tw("#trans", f"{{scale: {z}}}", "{scale: 1}", t + hold, 0.4, "power2.inOut", False)

    # ------------------------------------------------------------------ son
    def sound(self, name, t, vol=0.2):
        self.sfx.append((name, t, vol))

    # ------------------------------------------------------------------ page complète
    def write(self, main_end, voice, voice_dur, end=2.7, extra_css="", title="motion"):
        self.close()
        A = f"{self.root}/montage/assets"
        os.makedirs(f"{A}/brand", exist_ok=True)
        shutil.copy(f"{self.brand_dir}/{self.info['logo']}", f"{A}/brand/logo.png")
        shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{self.brand_dir}/fonts", f"{A}/brand/fonts")
        shutil.copy(f"{self.repo}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
        os.makedirs(f"{A}/sfx", exist_ok=True)
        if not os.path.exists(f"{self.root}/montage/hyperframes.json"):
            shutil.copy(f"{self.repo}/projets/video1/montage/hyperframes.json", f"{self.root}/montage/hyperframes.json")
        aud, used = [], {}
        for k, (name, t, vol) in enumerate(sorted(self.sfx, key=lambda s: s[1])):
            src = next((p for p in (f"{self.repo}/effets/sfx/utilisateur/{name}.wav", f"{self.repo}/effets/sfx/{name}.wav") if os.path.exists(p)), None)
            if not src:
                print(f"  (son absent, ignoré : {name})"); continue
            shutil.copy(src, f"{A}/sfx/{name}.wav")
            with wave.open(src) as w:
                ln = round(min(w.getnframes() / w.getframerate(), 1.6), 3)
            aud.append(f'<audio id="sfx{k}" class="clip" src="assets/sfx/{name}.wav" data-start="{max(0, t):.3f}" data-duration="{ln}" '
                       f'data-volume="{vol}" data-track-index="{7 + k % 4}"></audio>')
            used[name] = used.get(name, 0) + 1
        dur = round(main_end + end, 2)
        tag = self.info.get("tagline")
        endcard = (f'<div class="clip" id="endcard" data-start="{main_end}" data-duration="{end}" data-track-index="5">'
                   f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(self.info["name"])}"/>'
                   + (f'<div id="tagline">{"<br/>".join(p.strip() + "." for p in tag.rstrip(".").split("."))}</div>' if tag else "") + "</div>")
        self.tw("#logo", "{opacity: 0, scale: 0.9}", "{opacity: 1, scale: 1}", main_end + 0.05, 0.7)
        if tag:
            self.tw("#tagline", "{opacity: 0, y: 30}", "{opacity: 1, y: 0}", main_end + 0.5, 0.6)
        self.through(main_end, 1.25)
        dots = "".join(f'<i class="dot{" s" if k % 2 else ""}" id="dot{k}" style="left:{x}px;top:{y}px"></i>'
                       for k, (x, y) in enumerate([(130, 560), (930, 470), (200, 1180), (880, 1080), (520, 1560), (960, 1500), (110, 1580)]))
        for k in range(7):
            self.tw(f"#dot{k}", "{x: 0, y: 0}", f"{{x: {(-1) ** k * 40}, y: {-60 - 15 * k}}}", 0, main_end, "sine.inOut")
        sig = '<div class="sig">SPECIMEN GAMING</div>' if self.brand == "specimen-gaming" else ""
        css = open(f"{self.brand_dir}/brand.css").read()
        mcss = open(f"{HERE}/motion.css").read()
        ind = lambda s, n: "\n".join(" " * n + l for l in s.splitlines())
        page = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <meta name="brand" content="{self.brand}" />
    <meta name="montage-style" content="motion-design-clair" />
    <script src="assets/gsap.min.js"></script>
    <style>
{ind(css, 6)}
{ind(mcss, 6)}
{ind(extra_css, 6)}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
      <div id="bg"></div>
      <div id="deco"><div class="sun"></div><div class="ground"></div>{dots}</div>
      <div id="push"><div id="trans">
{ind(chr(10).join(self.stage), 8)}
      </div></div>
      {sig}
      {endcard}
    </div>
    <audio id="voix" class="clip" src="{voice}" data-start="0" data-duration="{voice_dur}" data-volume="1" data-track-index="6"></audio>
{ind(chr(10).join(aud), 4)}
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.js)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
        open(f"{self.root}/montage/index.html", "w").write(page)
        print(f"{title} : {dur} s, {len(aud)} sons ({', '.join(f'{k}×{v}' for k, v in used.items())})")
        return dur

