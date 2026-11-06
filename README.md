# Montage

Atelier de création vidéo par le code, prêt à l'emploi :

| Outil | Rôle | Version |
|---|---|---|
| [HyperFrames](https://hyperframes.heygen.com) | Vidéos écrites en HTML/CSS + GSAP, rendues en MP4/WebM/MOV/GIF | 0.9.19 |
| [Remotion](https://www.remotion.dev) | Vidéos écrites en React/TypeScript | 4.0.541 |
| [FFmpeg](https://ffmpeg.org) | Montage, transitions, mixage audio, encodage final | ≥ 6 |
| GSAP | Moteur d'animation des compositions HyperFrames (copie locale, sans CDN) | 3.15.0 |

## Prérequis

- Node.js ≥ 20 et npm
- FFmpeg + FFprobe dans le `PATH` (`apt install ffmpeg` / `brew install ffmpeg`)
- Chrome : HyperFrames et Remotion téléchargent chacun leur Chrome Headless Shell au premier rendu.
  Si le réseau le bloque, `scripts/with-browser.sh` détecte un Chrome Headless Shell Playwright local,
  ou définissez `REMOTION_BROWSER_EXECUTABLE=/chemin/vers/chrome-headless-shell`.

## Installation

```bash
npm install          # installe les deux workspaces (hyperframes/ et remotion/)
npm run doctor       # vérifie Node, FFmpeg (encodeurs), HyperFrames, Remotion, Chrome
npm run verify       # test de bout en bout : check + rendus + montage FFmpeg
```

`npm run verify` doit se terminer par « ✅ Tout fonctionne ».

## Structure

```
hyperframes/          projet HyperFrames (index.html = composition principale)
  assets/vendor/      gsap.min.js embarqué (rendu déterministe, hors-ligne)
  CLAUDE.md, AGENTS.md  règles de composition pour les agents IA
remotion/             projet Remotion (src/Root.tsx enregistre les compositions)
scripts/
  doctor.sh           diagnostic des dépendances
  verify.sh           vérification complète
  montage.sh          exemple de montage FFmpeg (fondu enchaîné + audio -14 LUFS)
  with-browser.sh     fournit un Chrome local à Remotion si besoin
```

## Utilisation

### HyperFrames (HTML → vidéo)

```bash
npm run hf:dev       # studio de prévisualisation dans le navigateur
npm run hf:check     # lint + validation runtime + mise en page + contraste
npm run hf:render    # → hyperframes/renders/main.mp4
cd hyperframes && npx hyperframes render --format webm   # autres formats : mov (ProRes + alpha), gif, png-sequence, hls
cd hyperframes && npx hyperframes snapshot --at 1,3      # captures PNG à des instants précis
```

Règles clés : chaque élément temporisé porte `data-start`/`data-duration` et `class="clip"`,
une timeline GSAP en pause est enregistrée dans `window.__timelines["<id>"]`, et aucune logique
non déterministe (`Math.random()`, `Date.now()`, requêtes réseau). Détails : `hyperframes/CLAUDE.md`
et `npx hyperframes docs <sujet>`.

### Remotion (React → vidéo)

```bash
npm run remotion:dev      # Remotion Studio
npm run remotion:render   # → remotion/out/intro.mp4
```

Ajoutez des compositions dans `remotion/src/Root.tsx`. Les animations se basent sur
`useCurrentFrame()`, `interpolate()` et `spring()`.

### FFmpeg (montage)

```bash
npm run montage                                  # HyperFrames + Remotion → out/montage.mp4 (+ vignette .jpg)
bash scripts/montage.sh a.mp4 b.mp4 sortie.mp4   # avec vos propres clips
```

Le script montre une chaîne type : harmonisation fps/pixels, transition `xfade`, piste audio
avec fondus, normalisation `loudnorm` (EBU R128, -14 LUFS), export H.264/AAC `+faststart`.

## Options facultatives

`npx hyperframes doctor` signale des modules optionnels non installés :

- **whisper.cpp** — transcription / sous-titres automatiques (`hyperframes transcribe`)
- **Kokoro** — synthèse vocale locale : `pip install kokoro-onnx soundfile`
- **MusicGen** — musique générée localement : `pip install transformers torch soundfile numpy`
- **Docker** — rendus HyperFrames reproductibles bit à bit (`--docker`)
