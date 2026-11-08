"""Démo motion design 3D (templates/motion-3d/motion3d.js) aux couleurs de Specimen Agency.

Intro halo → téléphone 3D avec interface animée → cartes de services → locaux isométriques → logo lumineux.
Tout le contenu est original (aucun élément de la vidéo de référence).
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = os.environ.get("BRAND", "specimen-agency")
BD = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BD}/brand.json"))
DUR = 15.0
OUT = f"{ROOT}/montage"; A = f"{OUT}/assets"

HTML = """<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <meta name="brand" content="{BRAND}" />
    <meta name="montage-style" content="motion-3d" />
    <script src="assets/gsap.min.js"></script>
    <script type="importmap">{{"imports": {{"three": "./assets/vendor/three/three.module.js", "three/addons/": "./assets/vendor/three/addons/", "motion3d": "./assets/motion3d.js"}}}}</script>
    <style>
{CSS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--black); }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font); color: var(--ink); }}
      #gl {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .t {{ position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }}
      .k {{ font-weight: 700; font-size: 36px; letter-spacing: 0.22em; color: var(--gold); }}
      .h {{ font-weight: 700; font-size: 118px; letter-spacing: -0.04em; line-height: 0.95; }}
      .h .a {{ color: var(--gold); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920"></canvas>
      <div class="t" id="t1" style="top:190px"><div class="k">SPECIMEN AGENCY</div><div class="h">Votre <span class="a">image.</span></div></div>
      <div class="t" id="t2" style="top:190px"><div class="k">MONTAGE · CONTENU · STRATÉGIE</div><div class="h" style="font-size:96px">On s'occupe <span class="a">de tout.</span></div></div>
      <div class="t" id="t3" style="top:330px"><div class="h">Notre <span class="a">expertise.</span></div></div>
    </div>
    <script type="module">
      import {{ THREE, createStage, canvasScreen, phone, card, isoBuilding, glowOrb, logoPlane, brandColor, bindTimeline }} from "motion3d";
      const gold = getComputedStyle(document.documentElement).getPropertyValue("--gold").trim();
      const ivory = getComputedStyle(document.documentElement).getPropertyValue("--ivory").trim();
      const black = getComputedStyle(document.documentElement).getPropertyValue("--black").trim();
      const font = "Specimen Heros";
      await document.fonts.load(`700 40px "${{font}}"`);
      const logoImg = new Image(); logoImg.src = "assets/brand/logo.png"; await logoImg.decode();

      const stage = createStage(document.getElementById("gl"), {{ bloom: 0.5 }});
      const {{ scene, camera }} = stage;
      const st = {{ orb: 0.01, orbOp: 0, ph: 0, rotY: -1.1, rotX: 0.15, px: 0, py: -6, ui: 0, cards: 0, bld: 0, bRot: 0.6, logo: 0, cam: 10 }};

      // --- intro : orbe lumineux
      const orb = glowOrb({{ size: 1 }}); scene.add(orb);

      // --- téléphone : écran = interface dessinée (profil d'agence, compteur, grille de contenus)
      const scr = canvasScreen(540, 1130, (c, w, h, t) => {{
        c.fillStyle = black; c.fillRect(0, 0, w, h);
        const p = st.ui;
        c.save(); c.globalAlpha = Math.min(1, p * 3);
        c.drawImage(logoImg, w / 2 - 80, 110, 160, 160);
        c.fillStyle = ivory; c.font = `700 40px "${{font}}"`; c.textAlign = "center"; c.fillText("Specimen Agency", w / 2, 320);
        c.fillStyle = gold; c.font = `700 22px "${{font}}"`; c.fillText("VOTRE IMAGE. NOTRE EXPERTISE.", w / 2, 360);
        const n = Math.round(Math.min(1, Math.max(0, (p - 0.15) / 0.5)) * 128);
        [["Projets", n], ["Vidéos", Math.round(n * 2.4)], ["Clients", Math.round(n / 3)]].forEach(([l, v], i) => {{
          const x = 90 + i * 180; c.fillStyle = ivory; c.font = `700 40px "${{font}}"`; c.fillText(String(v), x, 450);
          c.fillStyle = gold; c.font = `700 20px "${{font}}"`; c.fillText(l.toUpperCase(), x, 480); }});
        c.fillStyle = gold; c.beginPath(); c.roundRect(60, 520, w - 120, 64, 32); c.fill();
        c.fillStyle = black; c.font = `700 28px "${{font}}"`; c.fillText("Nous contacter", w / 2, 562);
        for (let i = 0; i < 9; i++) {{                     // grille de contenus qui apparaît
          const a = Math.min(1, Math.max(0, (p - 0.35 - i * 0.05) / 0.12)); if (a <= 0) continue;
          const gx = 24 + (i % 3) * 167, gy = 620 + Math.floor(i / 3) * 167;
          c.globalAlpha = a; c.fillStyle = i % 2 ? gold : ivory; c.globalAlpha = a * (i % 2 ? 0.85 : 0.18);
          c.beginPath(); c.roundRect(gx, gy + (1 - a) * 30, 158, 158, 14); c.fill(); }}
        c.restore();
      }});
      const ph = phone({{ screen: scr }}); ph.scale.setScalar(0.92); scene.add(ph);

      // --- cartes de services (texte original)
      const mkCard = (title, sub) => {{
        const s = canvasScreen(512, 300, (c, w, h) => {{ c.clearRect(0, 0, w, h); c.fillStyle = gold; c.font = `700 30px "${{font}}"`; c.textAlign = "left";
          c.fillText(sub.toUpperCase(), 36, 90); c.fillStyle = ivory; c.font = `700 64px "${{font}}"`; c.fillText(title, 36, 180); }});
        s.update(0); return card({{ texture: s.texture, w: 2.4, h: 1.4 }});
      }};
      const cards = [mkCard("Montage", "Vidéo"), mkCard("Contenu", "Réseaux"), mkCard("Stratégie", "Marque")];
      const cardPos = [[-2.6, 1.6, 0.6, 0.25], [2.5, 0.2, 0.9, -0.3], [-2.3, -1.9, 0.4, 0.2]];
      cards.forEach((c) => scene.add(c));

      // --- locaux isométriques
      const bld = isoBuilding({{ floors: 2 }}); bld.scale.setScalar(0.62); scene.add(bld);

      // --- logo final
      const logo = await logoPlane("assets/brand/logo.png", {{ height: 3.2 }}); scene.add(logo);
      const logoOrb = glowOrb({{ size: 1 }}); logoOrb.position.z = -0.5; scene.add(logoOrb);

      const tl = gsap.timeline({{ paused: true }});
      // intro (0–2,2 s) : l'orbe grossit, pulse, puis éclate
      tl.to(st, {{ orbOp: 1, orb: 1.6, duration: 1.2, ease: "power2.out" }}, 0.1);
      tl.to(st, {{ orb: 2.2, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 1.3);
      tl.to(st, {{ orb: 30, orbOp: 0, duration: 0.4, ease: "power3.in" }}, 1.95);
      // téléphone (2,2–7,6 s)
      tl.fromTo(st, {{ py: -7, rotY: -1.3 }}, {{ py: -1.0, rotY: -0.35, duration: 1.0, ease: "expo.out", immediateRender: false }}, 2.2);
      tl.to(st, {{ ui: 1, duration: 3.2, ease: "none" }}, 2.6);
      tl.to(st, {{ rotY: 0.32, duration: 4.2, ease: "sine.inOut" }}, 3.2);
      // cartes (5,2–8,2 s) puis sortie
      tl.to(st, {{ cards: 1, duration: 0.9, ease: "back.out(1.6)" }}, 5.2);
      tl.to(st, {{ cards: 0, px: 0, py: 8, duration: 0.6, ease: "power3.in" }}, 7.6);
      // locaux (8,2–11,8 s)
      tl.fromTo(st, {{ bld: 0 }}, {{ bld: 1, duration: 0.8, ease: "back.out(1.4)", immediateRender: false }}, 8.2);
      tl.fromTo(st, {{ bRot: 0.6 }}, {{ bRot: 1.4, duration: 3.6, ease: "none", immediateRender: false }}, 8.2);
      tl.to(st, {{ bld: 0, duration: 0.5, ease: "power3.in" }}, 11.6);
      // logo (12–15 s)
      tl.fromTo(st, {{ logo: 0 }}, {{ logo: 1, duration: 0.9, ease: "back.out(1.4)", immediateRender: false }}, 12.1);
      // textes DOM (défocalisation)
      const blurIn = (s, t) => tl.fromTo(s, {{ opacity: 0, filter: "blur(18px)", y: 24 }}, {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.5, ease: "power3.out", immediateRender: false }}, t);
      const blurOut = (s, t) => tl.to(s, {{ opacity: 0, filter: "blur(14px)", duration: 0.3 }}, t);
      blurIn("#t1", 2.6); blurOut("#t1", 5.0); blurIn("#t2", 5.3); blurOut("#t2", 7.6); blurIn("#t3", 8.6); blurOut("#t3", 11.5);
      tl.to({{}}, {{ duration: {DUR} }}, 0);

      bindTimeline(tl, "main", stage, (t) => {{
        orb.scale.setScalar(st.orb); orb.material.opacity = st.orbOp;
        ph.visible = t > 2.1 && t < 8.3;
        ph.position.set(st.px, st.py, 0); ph.rotation.set(st.rotX, st.rotY, 0);
        ph.position.y += Math.sin(t * 1.6) * 0.08;                       // flottement
        if (ph.visible) scr.update(t);
        cards.forEach((c, i) => {{ const [x, y, z, r] = cardPos[i]; const k = Math.max(0, Math.min(1.2, st.cards - i * 0.12));
          c.visible = k > 0.01; c.position.set(x * k, y + Math.sin(t * 1.3 + i) * 0.06, z); c.rotation.set(0, r, r * 0.3); c.scale.setScalar(Math.max(0.01, k)); }});
        bld.visible = st.bld > 0.01; bld.scale.setScalar(0.62 * Math.max(0.01, st.bld)); bld.rotation.set(0.62, st.bRot, 0); bld.position.set(0, -0.6, 0);
        bld.userData.band.material.emissiveIntensity = 0.5 + 0.4 * Math.sin(t * 3);
        logo.visible = st.logo > 0.01; logo.scale.setScalar(Math.max(0.01, st.logo)); logo.rotation.y = (1 - st.logo) * 0.8;
        logoOrb.visible = logo.visible; logoOrb.scale.setScalar(8 * st.logo); logoOrb.material.opacity = 0.35 * st.logo;
      }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", OUT)
open(f"{OUT}/meta.json", "w").write('{"id":"demo-motion-3d","name":"demo-motion-3d"}')
shutil.copy(f"{BD}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BD}/fonts", f"{A}/brand/fonts")
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{REPO}/templates/motion-3d/motion3d.js", f"{A}/motion3d.js")
shutil.rmtree(f"{A}/vendor", ignore_errors=True)
os.makedirs(f"{A}/vendor/three", exist_ok=True)
shutil.copy(f"{REPO}/effets/vendor/three/three.module.js", f"{A}/vendor/three/three.module.js")
shutil.copy(f"{REPO}/effets/vendor/three/three.core.js", f"{A}/vendor/three/three.core.js")
shutil.copytree(f"{REPO}/effets/vendor/three/addons", f"{A}/vendor/three/addons")
css = open(f"{BD}/brand.css").read()
open(f"{OUT}/index.html", "w").write(HTML.format(BRAND=BRAND, DUR=DUR, CSS="\n".join("      " + l for l in css.splitlines())))
print("démo motion 3D :", DUR, "s")
