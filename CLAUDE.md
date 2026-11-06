# Montage — consignes pour Claude

## Charte graphique VERROUILLÉE : Specimen Agency

Toutes les vidéos montées dans ce dépôt utilisent la charte **Specimen Agency**, sauf demande
explicite contraire de l'utilisateur pour une vidéo donnée.

- **Source unique** : `brand/specimen-agency/` (`brand.css`, `brand.json`, `logo.png`, `README.md`).
- Les compositions **injectent** `brand.css` (marqueur `{{BRAND_CSS}}` de `templates/reel-vertical/template.html`)
  et utilisent uniquement ses variables (`var(--gold)`, `var(--panel)`…). Dans les SVG :
  `style="fill:var(--gold)"`, jamais une couleur en dur.
- **Interdit** : rouge, vert, rose, bleu ou toute couleur absente de `brand.json`. Les notions
  « négatif / positif » s'expriment avec l'or, le noir et l'ivoire (barré, tampon, contraste), pas avec du rouge ou du vert.
- **Obligatoire** sur chaque vidéo : sous-titres blancs à contour noir avec mots clés en or,
  cartes noires à liseré or, flashs ivoire ou or, écran de fin logo + slogan.
- **Avant de livrer** : `npm run brand:check` doit être vert, en plus de `hyperframes check`.
- Changer la charte = modifier `brand/specimen-agency/` uniquement, puis régénérer les vidéos.

## Monter une nouvelle vidéo (procédure)

Point de départ : `projets/video1/` (pipeline complet et éprouvé).

1. Copier `projets/video1/scripts/` dans `projets/<nom>/scripts/`. La source va dans `projets/<nom>/src/`.
2. `clean_subs.py` : à n'utiliser que si la vidéo a des sous-titres incrustés à effacer.
3. Transcription : `hyperframes transcribe <audio> --model small --language fr`.
4. `cut_silences.py` : couper les blancs, puis recaler les mots sur la nouvelle timeline.
5. `build_composition.py` : adapter les groupes de sous-titres, les sections et les illustrations
   au discours. La charte est lue automatiquement (`BRAND=specimen-agency` par défaut).
6. `hyperframes check`, puis `npm run brand:check`, puis `hyperframes snapshot` pour relire.
7. `hyperframes render --quality delivery`, puis `loudnorm` à -14 LUFS (voir `scripts/montage.sh`).
8. Livrer à l'utilisateur deux fichiers : une version légère (CRF 23, environ 10 Mo) et une version HD.

Les médias lourds (`src/`, `work/`, `final/`, `renders/`) ne sont pas versionnés.
