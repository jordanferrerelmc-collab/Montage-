---
name: specimen-app-demo
description: Démo d'application animée en HTML pour une vidéo Specimen (Agency ou Gaming) — fenêtre façon logiciel, curseur scripté, texte tapé, barre d'étapes, aux couleurs et à la police de la marque. Utiliser pour un tutoriel d'interface, une démo produit, un « process » en étapes, une tactique / un réglage de jeu montré écran par écran, ou « comme un enregistrement d'écran mais en HTML » dans un Reel ou un TikTok.
---

# Démo d'application Specimen

Version maison du skill `html-demo` (MengTo, MIT) pour nos vidéos 1080 × 1920. Tout est dans
`templates/app-demo/` — lire son `README.md` avant de commencer.

1. Choisir la marque (CLAUDE.md) : gaming / TikTok gaming → `specimen-gaming`, sinon `specimen-agency`.
2. Copier un exemple : `projets/app-demo-agency/scripts/` ou `projets/app-demo-gaming/scripts/` vers `projets/<nom>/scripts/`.
3. Réécrire `steps.js` (3 à 5 étapes de 3,5 à 5 s) avec le contenu de l'utilisateur : ses textes, ses captures
   (passées par `images=`), ses chiffres. Interface originale, couleurs par variables uniquement.
4. Adapter `build.py` (marque, surtitre, titre, onglets), puis `python3 scripts/build.py`.
5. `hyperframes check` (0 erreur), `npm run brand:check`, `hyperframes snapshot` et relire la planche
   (curseur bien sur les boutons, rien de coupé), puis rendu, loudnorm -14 LUFS, versions HD + légère.
