# Motion design 3D — `motion3d.js`

Bibliothèque Three.js pour des pubs verticales « 3D + interfaces » (réf. `references/motion-3`),
rendu déterministe dans HyperFrames (rendu piloté par la timeline GSAP, jamais par une boucle libre).

Exemple complet : `projets/demo-motion-3d/scripts/build.py` (import map, chargement des polices et du logo,
timeline, enregistrement).

| Fonction | Rôle |
|---|---|
| `createStage(canvas, {bloom, threshold, exposure})` | rendu, caméra, éclairage d'environnement (RoomEnvironment), bloom |
| `canvasScreen(w, h, draw)` | texture d'interface dessinée en 2D et redessinée à chaque image (compteurs, grilles, chats…) |
| `phone({screen})` | téléphone 3D (coque arrondie, liseré, écran, encoche) |
| `card({texture})` | carte d'interface flottante avec liseré lumineux |
| `isoBuilding({floors})` | bâtiment isométrique procédural (locaux, boutique, agence) |
| `glowOrb({size})` | halo lumineux additif (intro, points de lumière) |
| `logoPlane(url)` | logo PNG en 3D avec halo (révélation finale) |
| `imageTexture(url)` | capture ou photo de l'utilisateur en texture (écran, cartes) |
| `loadModel(url)` | modèle 3D **fourni par l'utilisateur** (.glb / .gltf) |
| `bindTimeline(tl, id, stage, onFrame)` | branche le rendu sur la timeline et l'enregistre |

Les couleurs viennent des variables de la charte (`brandColor("--accent")`, `getComputedStyle`).
Three.js 0.184 et ses modules (`loaders`, `postprocessing`, `environments`, `geometries`…) sont dans
`effets/vendor/three/` (copiés dans `assets/vendor/three/` du projet). Côté Remotion : `@remotion/three`,
`@react-three/fiber`, `@react-three/drei`.

Aucun modèle 3D tiers n'est fourni : les modèles gratuits vérifiés exigent une attribution (CC-BY) ou ont
une licence incertaine. Les objets sont générés par code ; l'utilisateur peut fournir ses propres .glb.

Rendu : WebGL logiciel (pas de GPU), compter plusieurs minutes pour 15 s en 1080×1920.
