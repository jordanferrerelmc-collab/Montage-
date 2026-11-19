# Références « Prompt Motion » — fiche mesurée (19/11/2026)

Trois vidéos envoyées par l'utilisateur (« J'aime bien ça… Inspire-t'en, intègre ça dans ma DA ») :

| Vidéo | Auteur | Format | Durée | Sujet |
|---|---|---|---|---|
| Ondefica app motion reel | @jesscaroline7 (HyperFrames) | 1080×1920, 60 i/s | 59,6 s | appli de lieux, données de la communauté |
| Fitters Bible app promo | @Adamdesgns | 1920×1080, 60 i/s | 15,1 s | appli métier, « showreel » |
| Datagran ChatGPT ads explainer | @charlesmendez | 1920×1080, 30 i/s | 57,0 s | produit SaaS, parcours en étapes |

Fichiers dans `work/` (non versionnés : les vidéos appartiennent à leurs auteurs). On en retient **des principes**,
jamais le contenu, les logos, les couleurs ou les interfaces.

## Mesures (ffmpeg)

| Mesure | Ondefica | Fitters Bible | Datagran |
|---|---|---|---|
| Part de l'image presque noire | 47 % (+ 19 % de scènes blanches) | 78 % | 90 % |
| Part de la couleur d'accent | 12 % (orange) | ≈ 1 à 3 % (bleu, + or sur un passage) | ≈ 2 % (vert) |
| Coupes franches (seuil 0,18) | 8 en 60 s : surtout des transitions animées | 24 en 15 s, **qui accélèrent** : 1 toutes les 2 s, puis toutes les 0,2 s entre 10,5 et 13 s, juste avant le logo | 0 : un seul « monde » continu, les panneaux glissent |
| Scène / idée nouvelle | toutes les ~2 s | toutes les ~1 s | toutes les ~3,5 s (16 étapes) |
| Volume | -15,9 LUFS | -7,1 LUFS (musique très forte) | -14,3 LUFS |
| Voix | aucune : musique + design sonore | aucune | aucune |

## Ce qu'elles ont en commun (le « sens » retenu)

1. **Fond sombre + UNE couleur d'accent**, utilisée avec parcimonie (≤ 12 % de l'image) : elle désigne ce qui compte
   (le chiffre, le bouton, le mot). Ondefica alterne trois fonds : sombre, **plein accent** (orange plein cadre) et
   clair (blanc cassé), ce qui crée des « chapitres ».
2. **Typo cinétique géante** : 2 à 4 mots en capitales très grasses qui remplissent le cadre (« MEASURE TWICE. CUT ONCE. »,
   « ONE HAND. », « Launch. Grow. »), révélés par masque ou par lettres qui défilent, puis une petite ligne fine dessous.
   Contraste fort entre très gros / très petit.
3. **Habillage façon interface technique (HUD)** : coins de cadre, petites étiquettes en capitales très espacées en haut
   et en bas (nom du projet, chapitre « 04 / 08 », minutage), grille de points ou de lignes très discrète.
4. **La donnée devient image** : grands chiffres qui défilent (« 1.534 », « 5,820 »), grilles de points (un point par
   élément), anneaux de progression, barres, podium, courbe, réseau de nœuds reliés par des traits qui se dessinent.
5. **L'interface du produit est la vedette** : téléphones et panneaux sombres, éléments d'interface qui s'allument dans
   la couleur d'accent, texte tapé, bulles de conversation, curseur.
6. **Lumière** : halo radial de la couleur d'accent derrière l'objet, étincelles, particules, champ d'étoiles avant le logo.
7. **Rythme musical** : coupes et apparitions sur le temps ; accélération en rafale avant la fin ; fin = logo + slogan
   + petites pastilles.
8. **Mouvements** : sorties rapides, entrées avec léger dépassement, chiffres qui « roulent », balayages diagonaux de la
   couleur d'accent (Fitters Bible), caméra qui glisse dans un même univers (Datagran).

## Intégration dans la DA Specimen

Voir `DA.md` (racine du dépôt) : ces principes sont ajoutés au style « motion design clair » sous forme de **fonds
« nuit » et « éclat »**, de **typo cinétique**, de **HUD**, de **visualisations de données** et du **balayage d'accent**
(`templates/reel-motion/`). Les couleurs restent celles de la charte Specimen (noir + or / anthracite + rouge).
