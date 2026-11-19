# templates/reel-glass — style « bulles liquid glass » (STYLE PAR DÉFAUT)

Demande de l'utilisateur (19/11/2026) : « Garde ce style pour tous mes montages », après la vidéo
`projets/agency-glass/` (« Ajoute ton lieu »). S'applique aux **deux marques** ; la teinte vient de la charte
(`--glass-tint`, `--glass-tint-soft`, `--glass-cta-ink` dans `brand/<marque>/brand.css` : or pour Agency, rouge pour Gaming).

## Ce qui fait le style
- **Bulles de verre dépoli** (`.glass`) : flou d'arrière-plan 30 px, légère teinte sombre (lisible sur fond clair),
  reflet spéculaire en haut, liseré blanc translucide, ombre douce. Entrée « liquide » : la bulle gonfle et rebondit
  (`elastic.out`), sortie en se rétractant. **Ne jamais mettre de `filter: blur()` sur une bulle** (casse le verre).
- **Trois zones, jamais sur le visage ni sur les sous-titres** :
  - `.topwrap` (≈ 120 px) : accroche en grande bulle `.big` (petite ligne `.eyebrow` + texte, mot clé en couleur d'accent) ;
  - `.midwrap` (≈ 1215 px, entre le menton et les sous-titres) : bulles « notification » `.note` (icône dorée/rouge dans
    un carré sombre + titre + sous-ligne), variante message `.msg`, variante appel à l'action `.gold` (bulle pleine teinte) ;
  - `.capwrap` (≈ 1470 px) : sous-titres mot à mot dans une bulle `.cap`, blancs à contour noir léger, mots clés `.kw`.
  En Gaming, garder la signature « SPECIMEN GAMING » en haut et décaler `.topwrap` sous les onglets TikTok (≈ 260 px).
- **Coupe serrée** de tous les blancs > 0,16 s mesurés sur la voix nettoyée (`projets/agency-glass/scripts/cut.py`),
  coupes masquées par cadrage alterné (1,00 / 1,07) + bref flou « lentille » (4 px, 0,15 s).
- **Zooms aux moments importants** (demande de l'utilisateur, 19/11/2026), sur l'élément `#zoom` (séparé du cadrage
  alterné de `#cam`, ancré au menton) :
  - **coups de zoom** sur chaque mot fort (chiffre, mot clé, chute) : 1,12 à 1,22, puis relâche douce (`power3.out`, 0,75 s) ;
  - **transitions zoom** entre les parties : plongée vers 1,55 avec flou de mouvement (0,24 s), la partie suivante arrive
    zoomée et se pose (0,42 s), whoosh discret ;
  - fenêtres qui ne se chevauchent jamais, départ explicite de chaque tween (rendu déterministe) — voir `punch()` et
    `through()` dans `projets/agency-glass/scripts/build.py`.
- Voix nettoyée (`npm run voix:claire`), -14 LUFS en deux passes, sons discrets (clic `ui` par bulle), écran de fin de la charte.

## Utilisation
Copier `projets/agency-glass/scripts/` (`cut.py`, `build.py`) dans le nouveau projet, adapter les textes et les instants,
`BRAND` selon le sujet. `build.py` injecte `brand.css` puis `glass.css`. Vérifier : `hyperframes check` (0 erreur de
contraste), `npm run brand:check`, `hyperframes snapshot` (rien sur le visage).
