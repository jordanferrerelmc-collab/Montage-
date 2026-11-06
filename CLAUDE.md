# Montage — consignes pour Claude

## Chartes graphiques VERROUILLÉES : deux marques

Chaque montage utilise **exactement une** des deux chartes ci-dessous. Elles ne se mélangent jamais.

| Marque | Dossier | Quand l'utiliser | Couleurs | Police | Format |
|---|---|---|---|---|---|
| **Specimen Agency** | `brand/specimen-agency/` | Par défaut : agence, Instagram, conseils marketing | or, noir profond, ivoire | Helvetica Neue → TeX Gyre Heros (`"Specimen Heros"`) | Reels Instagram, **style éditorial** |
| **Specimen Gaming** | `brand/specimen-gaming/` | Vidéos du **compte TikTok gaming** (jeux vidéo, gameplay, gaming, TikTok gaming) | rouge `#da3d39`, anthracite `#2c2d32`, blanc | Helvetica Neue → TeX Gyre Heros (`"Specimen Heros"`) | TikTok (zones de l'interface évitées), **style dynamique** |

**Choix de la marque.** Si l'utilisateur parle de gaming, du compte gaming ou de TikTok gaming, ou si la vidéo
porte sur le jeu vidéo, utiliser `specimen-gaming`. Sinon, utiliser `specimen-agency`. En cas de doute réel,
poser la question avant de monter. La marque se choisit avec `BRAND=<marque>` au moment de la génération ;
elle est inscrite dans la composition (`<meta name="brand">`) et le vérificateur s'en sert.

**Styles de montage verrouillés** (`montage_style` dans `brand.json`) :
- **Agency → éditorial** (`templates/reel-editorial/`, exemple : `projets/video1/scripts/build_editorial.py`),
  d'après le Reel de référence `references/reel-style/` :
  - sous-titres mot à mot (1 à 3 mots), blancs, TeX Gyre Heros gras, sans contour, ombre douce, à hauteur de poitrine ;
  - grands titres (petite ligne + très grande ligne en capitales) **derrière la tête** : le sujet est détouré avec
    `hyperframes remove-background` (`assets/subject.webm`, superposé au-dessus des titres). Ils passent de l'or au blanc ;
  - cartes flottantes arrondies (noir ou ivoire, liseré or) qui entrent en éventail ; carte de stats (anneau), pastilles d'étape ;
  - transitions en halo lumineux doux (`#bloom`), zooms lents, micro-sauts discrets sur les coupes ; pas de flash dur ni de tremblement ;
  - CTA en pilule dorée, écran de fin avec le logo.
- **Gaming → dynamique** (`templates/reel-vertical/`, exemple : `projets/video1/scripts/build_composition.py`) :
  flashs et zooms rapides, sous-titres à contour épais, bruitages.

Règles communes :
- **Source unique** : `brand/<marque>/` (`brand.css`, `brand.json`, `logo.png`, `fonts/`, `README.md`).
- Les compositions **injectent** `brand.css` (marqueur `{{BRAND_CSS}}` de `templates/reel-vertical/template.html`)
  et n'utilisent que ses variables (`var(--accent)`, `var(--panel)`, `var(--font)`…). Dans les SVG,
  écrire `style="fill:var(--accent)"`, jamais une couleur en dur. Les alias `--gold`, `--ivory`… existent
  dans les deux chartes pour que les modèles fonctionnent avec l'une comme avec l'autre.
- **Police unique, la même pour les deux marques** : Helvetica Neue, remplacée par son équivalent libre
  TeX Gyre Heros (licence GUST, fichiers d'origine non modifiés dans `brand/<marque>/fonts/`), famille
  `"Specimen Heros"`, exposée par `var(--font)`. Graisses disponibles : 400 et 700. Aucune autre `font-family`
  (ni Arial, ni Inter, ni Google Fonts).
- **Interdit** : toute couleur absente du `brand.json` de la marque. Pas de rouge ni de vert dans Agency ;
  pas d'or ni de jaune dans Gaming.
- **Obligatoire** sur chaque vidéo : sous-titres blancs à contour noir avec mots clés à la couleur
  d'accent de la marque, cartes de la marque, flashs de la marque, écran de fin avec le logo de la marque.
- La bande floutée `#shade` ne sert qu'à masquer des sous-titres déjà incrustés dans la source :
  la retirer si la vidéo source n'en a pas.
- **Avant de livrer** : `npm run brand:check` (couleurs + police, selon la marque) doit être vert, en plus de `hyperframes check`.
- Changer une charte = modifier uniquement `brand/<marque>/`, puis régénérer les vidéos.

## Monter une nouvelle vidéo (procédure)

Point de départ : `projets/video1/` (pipeline complet et éprouvé).

1. Copier `projets/video1/scripts/` dans `projets/<nom>/scripts/`. La source va dans `projets/<nom>/src/`.
2. `clean_subs.py` : à n'utiliser que si la vidéo a des sous-titres incrustés à effacer.
3. Transcription : `hyperframes transcribe <audio> --model small --language fr`.
4. `cut_silences.py` : couper les blancs, puis recaler les mots sur la nouvelle timeline.
5. `build_composition.py` : adapter les groupes de sous-titres, les sections et les illustrations
   au discours. La charte (couleurs, police, logo) est lue et copiée automatiquement dans
   `montage/assets/brand/`. Lancer avec `BRAND=specimen-gaming` pour le compte gaming
   (`specimen-agency` par défaut).
6. `hyperframes check`, puis `npm run brand:check`, puis `hyperframes snapshot` pour relire.
7. `hyperframes render --quality delivery`, puis `loudnorm` à -14 LUFS (voir `scripts/montage.sh`).
8. Livrer à l'utilisateur deux fichiers : une version légère (CRF 23, environ 10 Mo) et une version HD.

Les médias lourds (`src/`, `work/`, `final/`, `renders/`) ne sont pas versionnés.
