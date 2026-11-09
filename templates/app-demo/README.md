# templates/app-demo — démos d'application aux couleurs Specimen

Adaptation du skill **html-demo** (MengTo/Skills, MIT, `.claude/skills/html-demo`) pour nos vidéos verticales
1080 × 1920 : une fenêtre d'application simulée en HTML (curseur scripté, texte tapé, barre d'étapes),
pilotée image par image par la timeline HyperFrames, aux couleurs de la marque choisie.

| Fichier | Rôle |
|---|---|
| `step-window.js`, `step-window.css` | Moteur d'origine (MIT), **copie adaptée vidéo** : horloge temps réel et transitions CSS retirées |
| `specimen-window.css` | Habillage de la charte (fenêtre, onglets, barre d'étapes, curseur) + **kit d'interface `sp-`** |
| `app-demo.js` | `AppDemo.bind(tl, el, {steps, tabs, label, start})` : la timeline appelle `seek(t)` |
| `template.html` | Vidéo : surtitre + titre, fenêtre, sous-titre par étape, halo, écran de fin de la charte |
| `build_app_demo.py` | `build(...)` : remplit le modèle, place les bruitages, copie charte + ressources |

## Faire une nouvelle démo

1. `projets/<nom>/scripts/steps.js` : `const STEPS = [...]`. Chaque étape :
   `{ id, name, dur, say, clicks, keys, html, draw(t, $) }`
   - `html` : l'écran à 1200 × 750, composé avec le kit `sp-` (`sp-app`, `sp-side`, `sp-main`, `sp-title`, `sp-muted`,
     `sp-btn` / `.ghost`, `sp-card` / `.on`, `sp-row`, `sp-chip` / `.on`, `sp-progress` (`--p`), `sp-toast`, `sp-check`, `sp-spin`).
     Placer les éléments cliqués en absolu (`position:absolute; left; top`) pour connaître leurs coordonnées.
   - `draw(t, $)` : tout ce qui bouge dépend de `t` seul (`ease`, `typed`, `cue`, `held`, `glide`) ;
     renvoyer `{ cursor: glide(t, [[0,0,x,y], [début, fin, x, y], …], [clics]) }`.
   - `say` : sous-titre de l'étape (mots clés dans `<span class='a'>`) ; `clicks` / `keys` : bruitages clic / clavier.
   - Couleurs : **uniquement** `var(--accent)`, `var(--ink)`, `var(--panel)`, `var(--dark)`… (jamais de couleur en dur).
2. `projets/<nom>/scripts/build.py` :
   ```python
   import os, sys
   ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   REPO = os.path.dirname(os.path.dirname(ROOT))
   sys.path.insert(0, f"{REPO}/templates/app-demo")
   from build_app_demo import build
   build(root=ROOT, brand="specimen-agency", steps_js=f"{ROOT}/scripts/steps.js",
         kicker="SPECIMEN AGENCY · PROCESS", title="Du rush<br><span class='a'>au Reel</span>",
         tabs=["Montage", "video1.mp4"], label="Du rush au Reel",
         images={"thumb.jpg": "/chemin/vers/capture.jpg"})   # images → montage/assets/
   ```
3. Dans `projets/<nom>/montage` : `hyperframes check`, `npm run brand:check`, `hyperframes snapshot`,
   `hyperframes render --quality delivery`, loudnorm -14 LUFS, versions HD + légère.

Exemples : `projets/app-demo-agency/` (Du rush au Reel) et `projets/app-demo-gaming/` (Ma 4-3-1-2 en 4 étapes).

Règles : interfaces **originales** (ne pas recopier l'interface d'un jeu ou d'un logiciel tiers), textes de l'écran
≥ 26 px dans la scène (la fenêtre est réduite à 0,75–0,83 dans la vidéo), un message de confirmation tenu ≥ 2 s.
Pour une voix off : caler les `dur` des étapes sur les phrases, puis ajouter l'audio dans `build_app_demo.py`
(`extra_sfx`) ou dans la composition.
