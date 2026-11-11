# Montage — consignes pour Claude

## Chartes graphiques VERROUILLÉES : deux marques

Chaque montage utilise **exactement une** des deux chartes ci-dessous. Elles ne se mélangent jamais.

| Marque | Dossier | Quand l'utiliser | Couleurs | Police | Format |
|---|---|---|---|---|---|
| **Specimen Agency** | `brand/specimen-agency/` | Par défaut : agence, Instagram, conseils marketing | or, noir profond, ivoire | Helvetica Neue → TeX Gyre Heros (`"Specimen Heros"`) | Reels Instagram, **style éditorial** |
| **Specimen Gaming** | `brand/specimen-gaming/` | Vidéos du **compte TikTok gaming** (jeux vidéo, gameplay, gaming, TikTok gaming) | rouge `#da3d39`, anthracite `#2c2d32`, blanc | Helvetica Neue → TeX Gyre Heros (`"Specimen Heros"`) | TikTok (zones de l'interface évitées), **style gaming premium** |

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
- **Gaming → « gaming premium »** (`templates/reel-gaming/` + bibliothèque d'animations `gaming-fx.js`,
  exemple complet : `projets/demo-style-gaming/scripts/build.py`), d'après la vidéo de référence `references/gaming-style/` :
  - fond sombre en dégradé radial, halo rouge qui respire ; signature « SPECIMEN GAMING » en haut (sans barre de progression, voir règles communes) ;
  - révélation mystère : silhouette « ? » → visuel révélé avec onde de choc (`fx.mysteryReveal`) ;
  - textes en défocalisation (`fx.blurIn` / `fx.blurOut`), classement « N° + nom + sous-titre » ;
  - encadrés de stats et badges qui glissent (`fx.slideBlur`), note « → … », compteur en pastille (`fx.countUp`) ;
  - grille d'appel à l'action 2×2 au début (`fx.ctaGrid`) ; sous-titres mot à mot, blancs, sans contour, mots clés en rouge ;
  - transitions en fondu flouté, pas de flash dur ; bruitages discrets (riser, impact, ding, clic) ; écran de fin avec le logo.
  - Les captures de jeu de l'utilisateur s'intègrent dans la carte centrale (`.cardvis`) ou en plein cadre derrière le halo.
  - Ancien style « dynamique » (flashs, contours épais) : `templates/reel-vertical/`, seulement sur demande.

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
- **Texte toujours centré à l'écran** (demande de l'utilisateur, 09/11/2026) : sous-titres, titres, notes et appels
  à l'action sont centrés horizontalement, dans la colonne `var(--cap-left)` / `var(--cap-width)` de la charte
  (marges égales : 90 px Agency, 110 px Gaming). Jamais de texte aligné ou collé contre un bord : il serait coupé ou
  caché par l'interface (bords arrondis, icônes TikTok / Instagram). Vérifier sur `hyperframes snapshot`.
- **Jamais d'émoji ni d'illustration sur le visage NI sur les sous-titres** (demande de l'utilisateur, 10/11/2026).
  Face caméra : ancrer les zooms au niveau du menton (`transform-origin: 50% 60%`) pour que le visage ne descende pas ;
  placer émojis / illustrations **juste au-dessus des sous-titres** (≈ 1220-1380 px, sous-titres à 1440 px), petits
  (≈ 140 px) avec une onde de choc qui ne déborde pas (`fx.shockwave(..., {to: 1.0})`, anneau de 180 px).
  Vérifier chaque émoji sur `hyperframes snapshot`, y compris pendant les coups de zoom.
- **Pas de barre de progression** (demande de l'utilisateur, 10/11/2026) : ne plus mettre la barre rouge (`.bar`) ni les
  cases de progression (`.tracker`) sous la signature « SPECIMEN GAMING ». La signature seule reste en haut.
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

9. **Toujours terminer la livraison par les descriptions SEO** (demande de l'utilisateur, 10/11/2026), prêtes à copier :
   - **TikTok** : 1re ligne = accroche avec le mot clé principal (ce que les gens tapent dans la recherche), 1 à 2 phrases
     naturelles avec les mots clés secondaires, un appel à l'action (commente / abonne-toi), **4 hashtags maximum**
     (1 large + 2 de niche + 1 de marque ou de format), en français.
   - **YouTube (Shorts)** : un **titre** de moins de 70 caractères (mot clé au début), puis une description de 2 à 4 lignes
     (mot clé dans la 1re phrase, mots clés secondaires, appel à l'action), **4 hashtags maximum**.
   - Pas de faux chiffres ni de promesses trompeuses ; mots clés tirés du sujet réel de la vidéo (jeu, mode, tactique…).
   - Écrire aussi ces textes dans `projets/<nom>/final/description.md`.

Les médias lourds (`src/`, `work/`, `final/`, `renders/`) ne sont pas versionnés.

## Voix clonée de l'utilisateur (montages sans visage)

- Voix de référence : `voix/voix_reference.wav`, échantillon propre de 27 s tiré de `projets/video1`.
  Versionnée dans le dépôt à la demande explicite de l'utilisateur, alors que le dépôt est public
  (risque expliqué le 06/11/2026). Ne l'utiliser que pour ses propres montages.
- Moteur : Chatterbox Multilingual, en local (licence MIT, français). Installation : `npm run voix:install`
  (≈ 3 Go, quelques minutes, à faire au début d'une session qui en a besoin).
- Génération : `npm run voix -- "Texte." -o out/voix.wav` (ou `--fichier texte.txt`, `--expressivite 0.3-0.8`).
  Compter environ 25 s de calcul par phrase sur CPU.
- Toujours relire la sortie avec `hyperframes transcribe` : le modèle peut déformer un mot
  (ex. « vues » → « jus »). Reformuler la phrase et régénérer si besoin.
- Montage sans visage : voix off + style de la marque (cartes, titres, B-roll fournis par l'utilisateur,
  fond de marque), sans la vidéo de la personne.

## Effets et transitions pro (bibliothèque `effets/`)

À utiliser dans chaque montage pour un rendu de qualité. Détail et liste complète : `effets/README.md`.
- **191 éléments HyperFrames** dans `effets/compositions/` : 70 transitions (dont shaders WebGL : cinematic-zoom,
  light-leak, glitch, whip-pan, swirl-vortex, ridged-burn, cross-warp-morph…), effets (grain, vignette, motion blur,
  camera shake, light leaks), 17 styles de sous-titres, bandeaux, titres, logos/CTA. Copier l'élément voulu dans le
  projet, puis remplacer ses couleurs et sa police par les variables de la charte (`npm run brand:check` doit rester vert).
- **Nouvel élément du catalogue** : `cd effets && ../hyperframes/node_modules/.bin/hyperframes add <nom> --no-clipboard`,
  puis `npm run fx:localize` (GSAP local au lieu du CDN).
- **Bruitages** `effets/sfx/` (17), **LUT** `effets/luts/` (6), **grain** `effets/overlays/` (régénérés par `npm run fx:assets`).
- **Sons de réaction** (« woaah », surprise, cris de victoire, foule de stade, huées, rires) : `npm run sfx:reactions`
  télécharge 14 sons Mixkit dans `effets/sfx/reactions/` (non versionnés : la licence Mixkit autorise l'usage dans nos
  vidéos, pas la redistribution des fichiers ; hôtes `mixkit.co` / `assets.mixkit.co` autorisés dans l'environnement
  « Montage »). À relancer au début d'une session qui en a besoin. Usage : **1 à 3 par vidéo, sur les vrais temps forts**
  (but, révélation, chute), volume 0,3 à 0,5 sous la voix, jamais en continu. Pour en ajouter : compléter la liste
  `id nom` du script (id Mixkit visible dans l'URL du son).
- **Étalonnage final** : `npm run grade -- in.mp4 out.mp4 <look> [--grain] [--vignette] [--force 0.8]`.
  Agency : `or-chaud` ou `film-desature`. Gaming : `punchy-gaming` ou `froid-net`.
- **Transitions FFmpeg** entre deux vidéos : `npm run transition -- a.mp4 b.mp4 out.mp4 <type> <durée>`.
- **Remotion** dispose aussi de @remotion/transitions, motion-blur, noise, shapes, paths, lottie et light-leaks.
- Rendu des shaders : WebGL logiciel (pas de GPU), plus lent mais fonctionnel. Les éléments 3D chargent
  Three.js depuis cdn.jsdelivr.net (autorisé dans l'environnement « Montage »).

## Motion design 3D (pubs « 3D + interfaces »)

**EN PAUSE (demande de l'utilisateur, 08/11/2026) : ne pas utiliser ce style dans les montages, sauf nouvelle demande
explicite.** Les outils restent installés pour plus tard.

Pour les vidéos du type `references/motion-3` (téléphone 3D, interfaces animées, objets 3D, halos, logo lumineux) :
bibliothèque `templates/motion-3d/motion3d.js` (voir son README), exemple `projets/demo-motion-3d/`.
- 362 éléments du catalogue dans `effets/compositions/` : maquettes d'interface (chat, notifications, profils, avis,
  navigateur, appareils), scènes 3D, caméras, galeries, fonds lumineux — à adapter aux couleurs de la charte.
- Rendu 3D : toujours piloté par la timeline (`bindTimeline`), écrire aussi `window.__timelines["main"] = tl;`
  dans la page (le contrôle statique le cherche). Bloom : seuil élevé (0,8) pour éviter la surexposition.
- Pas de modèles 3D tiers (licences) : objets procéduraux, ou modèles .glb fournis par l'utilisateur.
- Rendu lent sans GPU : lancer le rendu en arrière-plan.

## Skill « effects » (51 effets face caméra, tiers, MIT)

Installé dans `.claude/skills/effects` (voir `SKILL.md` et `INSTALL-MONTAGE.md`). Commande `/effects <nom>` :
effets qui suivent le visage (mot géant derrière la tête, crochets « locked-on », orbite de reels, spotlight,
tampon, checklist, iMessage, liquid glass, etc.). Mise en route d'une session : `npm run effects:setup` (≈ 2 min).
- **Charte** : ses effets utilisent leurs propres polices (Archivo Black, Anton, Inter…) et couleurs (rouge du
  tampon…), **non conformes** aux chartes Specimen. Dans un montage de marque, ne l'utiliser que si l'utilisateur
  le demande explicitement, et le signaler ; sinon préférer les modèles maison (`reel-editorial`, `reel-gaming`).
- Ses rendus gardent l'audio d'origine et n'ajoutent ni sous-titres ni sons : enchaîner ensuite avec nos
  sous-titres et bruitages si besoin.

## Skill « html-demo » (MengTo/Skills, MIT)

Installé avec `npx skills add MengTo/Skills --skill html-demo` dans `.claude/skills/html-demo` (provenance dans
`skills-lock.json`). Sert à **simuler une application en HTML** (fenêtre façon Mac, curseur scripté, texte tapé,
barre d'étapes), chaque image calculée depuis une seule horloge `View(t)` : démos produit, tutoriels d'interface,
« comme un enregistrement d'écran mais en HTML ».
- Démo : servir la racine du skill (`python3 -m http.server`) puis ouvrir `/demo/index.html`.
- Captures : `node scripts/shoot.mjs <url> <prefix> --at 1,2.5 [--frozen]` (Playwright préinstallé).
- **Pour une vidéo : toujours utiliser la version adaptée `templates/app-demo/`** (skill projet `specimen-app-demo`,
  voir `templates/app-demo/README.md`) : charte de la marque (police, couleurs, logo de fin), kit d'interface `sp-`,
  fenêtre pilotée par la timeline, sous-titre et bruitages par étape. Exemples : `projets/app-demo-agency/`
  (« Du rush au Reel ») et `projets/app-demo-gaming/` (« Ma 4-3-1-2 en 4 étapes »). Le skill d'origine reste intact
  (Geist, hors charte) pour des pages web.

## Skill « steal » (Melvynx/video-agent-skills, installé le 09/11/2026)

Installé avec `npx skills add Melvynx/video-agent-skills --skill steal` dans `.agents/skills/steal`
(lien `.claude/skills/steal`, provenance dans `skills-lock.json`). Sert à **mesurer le style de montage d'un Reel ou
d'un TikTok de référence** (coupes par seconde, rythme, bruitages sur les coupes, niveau de la musique sous la voix,
taille du visage et zooms) au lieu de l'estimer à l'œil. Mise en route d'une session : `npm run steal:setup` (yt-dlp).
Lire aussi `.agents/skills/steal/references/learnings.md` (erreurs déjà rejetées : trop de clics, zooms trop forts…).

Adaptation à ce dépôt (le skill vise le moteur `short-editing` de l'auteur, **non installé ici**) :
- Mesures et notes dans `references/<nom>/` (planches, `cuts.txt`, spectrogramme, `STYLE.md` avec chaque valeur mesurée).
- Application avec **nos** modèles (`reel-editorial`, `reel-gaming`, `app-demo`) : on copie le rythme, la mise en page,
  les zooms et le placement des sons — **jamais les couleurs ni la police** de l'autre créateur, qui restent celles de la
  charte Specimen choisie (`npm run brand:check` doit rester vert). Bruitages pris dans `effets/sfx/`.
- Instagram / TikTok : essayer `yt-dlp` ; s'il est bloqué, demander à l'utilisateur d'envoyer le fichier vidéo.
- Avant de livrer : comparaison image par image original / copie (commande de l'étape 5 du skill).

### Style « Vidéo liquide glass » (mesuré avec steal, 09/11/2026)

Pour **les deux marques**, selon le sujet de la vidéo. Fiche : `references/video-liquide-glass/STYLE.md` ;
modèle : `templates/reel-liquid-glass/` ; exemple : `projets/video1/scripts/build_liquid_glass.py`.
Sous-titres italiques blancs qui entrent / sortent en flou, mot géant en « verre » aux couleurs de la charte derrière la
tête (sujet détouré), poussée lente, transitions en flou plein cadre, impact grave en fin d'accroche, coupes de B-roll
sur le rythme. À utiliser quand l'utilisateur demande ce style (« liquide glass », « liquid glass »).
