# Direction artistique Specimen — DA des montages

> Document de référence, à relire avant chaque montage. Version du 19/11/2026.
> Construit à partir des demandes de l'utilisateur et de ses références :
> la vidéo « motion design clair » (`references/style-motion/STYLE.md`) et trois vidéos Prompt Motion
> (Ondefica, Fitters Bible, Datagran : `references/style-prompt-motion/STYLE.md`).
> Mise en œuvre : `templates/reel-motion/` (`motion.py`, `motion.css`). Exemple complet : `projets/agency-motion/`.
> Les couleurs exactes vivent dans `brand/<marque>/brand.css` : ce document les décrit, il ne les remplace pas.

---

## 1. L'idée en une phrase

**Du motion design net et rythmé, à nos couleurs : une idée par plan, une seule couleur qui désigne ce qui compte,
et un texte qui suit la voix mot à mot.**

Trois principes tirés des références :

1. **Une couleur d'accent, utilisée avec parcimonie** (≈ 10 % de l'image au plus) : or pour Agency, rouge pour Gaming.
   Elle désigne le mot fort, le chiffre, le bouton, l'élément qui change. Tout le reste est neutre.
2. **Une seule idée à l'écran à la fois** : un objet central par phrase (téléphone, lecteur, fenêtre, icône, donnée).
3. **Le rythme fait la qualité** : une scène nouvelle toutes les ~2 s, un élément qui arrive sur chaque mot important,
   des transitions franches, une accélération avant la fin.

---

## 2. Les deux marques

| | **Specimen Agency** | **Specimen Gaming** |
|---|---|---|
| Quand | par défaut : agence, marketing, Instagram | compte TikTok gaming, jeux vidéo |
| Accent | or `#e3b25c` (texte : or foncé `#b8863b` sur clair) | rouge `#da3d39` (rouge clair `#ff5a4e` sur nuit) |
| Neutres | noir profond `#0b0b0d`, ivoire `#f7f1e3`, blanc | anthracite `#1c1d21` / `#2c2d32`, argent `#c9cbd1`, blanc |
| Signature | aucune en haut ; logo en fin | « SPECIMEN GAMING » en haut, sans barre de progression |
| Marges | 90 px sur les côtés | 110 px sur les côtés (icônes TikTok) |

Jamais de mélange : pas de rouge ni de vert dans Agency, pas d'or ni de jaune dans Gaming
(`npm run brand:check`).

---

## 3. Trois fonds = trois « chapitres »

Inspiré d'Ondefica, qui alterne fond sombre, plein accent et clair. On change de fond pour marquer un changement de
partie, pas à chaque plan.

| Fond | Agency | Gaming | Usage |
|---|---|---|---|
| **Clair** (par défaut) | ivoire, haut de l'écran blanc ; soleil rayé or doux | blanc ; soleil rayé rouge doux | explication, démonstration, appel à l'action |
| **Nuit** (`.g-nuit`) | noir profond + grille de points or, halo or | anthracite + grille argent, halo rouge | preuve, données, révélation, ambiance « produit » |
| **Éclat** (`.g-eclat`) | or plein cadre, texte noir | rouge plein cadre, texte blanc | le mot fort en typo géante, 1 à 2 fois par vidéo au plus |

Dans le code : `m.scene("s3", t0, t1, ground="eclat", fill="lines")` ou `ground="nuit", fill="grid", glow=True`.
Tous les éléments (cartes, téléphones, pastilles, texte) changent de couleur seuls grâce aux variables `--mo-*`.

---

## 4. Typographie

Une seule famille : **Helvetica Neue → TeX Gyre Heros** (`var(--font)`), graisses 400 et 700. Aucune autre police.

| Rôle | Taille (1080×1920) | Style |
|---|---|---|
| Typo cinétique (éclat) | 120 à 210 px, calculée selon la longueur | capitales, 700, interlignage 0,92, approche −0,045 em, révélée par masque |
| Phrase du haut | 56 à 62 px | 700, centrée, mots clés en couleur, mot fort en pastille sombre ▸ |
| Grand chiffre | 150 px | 700, couleur d'accent, chiffre qui défile |
| Cartes, étapes | 34 à 38 px | 700 ; sous-ligne 24 px en 400 |
| Étiquette HUD | 28 px (minimum lisible sur téléphone) | capitales très espacées (0,34 em), 700, discrète |

Contraste minimum 3:1 pour les grands textes (`hyperframes check` le vérifie). Sur fond clair, l'or du texte est
l'or foncé.

---

## 5. Mise en page 9:16

```
   0 ┌──────────────────────────────┐
  96 │ ⌜  (coins du HUD)          ⌝ │   Gaming : signature à 120 px
 200 │   La phrase qui s'écrit…     │   Agency 200 px / Gaming 250 px, 1 à 3 lignes
 500 │                              │
     │        OBJET CENTRAL         │   un seul : téléphone, lecteur, fenêtre, icône,
     │                              │   barre de recherche, donnée
1300 │      cartes · étapes · CTA   │
1648 │  01 / 04 · LE CHAPITRE       │   étiquette HUD
1690 │ ⌞ ─ ─ zone interdite ─ ─ ─ ⌟ │   (interface TikTok / Instagram)
1920 └──────────────────────────────┘
```

- Tout le texte est **centré** dans la colonne de la charte, avec une réserve de 50 px pour les zooms.
- Rien à moins de 90 px (Agency) / 110 px (Gaming) des côtés, 90 px du haut, 230 px du bas, à tout moment
  (`npm run marges:check`).
- Rien sur le visage ni sur les sous-titres dans une vidéo face caméra.

---

## 6. Les éléments de la DA

| Élément | Quand | Code |
|---|---|---|
| Phrase mot à mot (défloutage) | toute la vidéo, sur la voix | `m.say()` |
| Typo cinétique géante | 1 à 2 mots forts (titre, chute, promesse) | `m.kin()` sur fond éclat |
| Téléphone / lecteur / fenêtre de montage | l'objet central d'une phrase | `.phone`, `.player`, `.win` |
| Barre de recherche tapée | « recherche… », « tape… » | `.prompt` + `m.type()` |
| Cartes flottantes | réactions, notifications, avantages | `.card` + `m.bob()` |
| Étapes numérotées + coches | méthode, liste, tutoriel | `.step` + `m.tick()` |
| Autocollant rond + onde de choc | souligner un mot (vues, idée, validé) | `.stk` + `m.shock()` |
| Grand chiffre qui défile | **seulement un vrai chiffre** donné par l'utilisateur | `.count` + `m.count()` |
| Grille de points | « un point = un élément » (quantité réelle) | `m.dots()` |
| Barres, anneau | comparaison, proportion réelle | `m.bars()`, `m.ring()` |
| Réseau de nœuds | « tout se connecte », outils reliés | `m.network()` |
| HUD (coins + chapitre) | toute la vidéo, discret | `m.chapter()` |
| Halo de l'accent | derrière l'objet central sur fond nuit | `glow=True` |
| Écran de fin | toujours : logo + slogan de la charte | automatique (`m.write()`) |

Illustrations **maison** : personnage stylisé (`person()`), pictos SVG de la charte. Pas d'interface réelle d'une autre
marque, jamais d'émoji sur un visage ou un sous-titre. **Seule exception : les logos d'outils du skill `dev-icons`**
(Claude, Figma, Notion…), pour désigner l'outil dont parle la vidéo, en couleurs officielles, licence vérifiée
(voir `CLAUDE.md`). TikTok, Instagram, YouTube et ChatGPT n'y sont pas : pas de substitut dessiné.

---

## 7. Mouvement

| Mouvement | Réglage |
|---|---|
| Entrée signature | ressort + défloutage : échelle 0,6 → 1, flou 16 → 0 px, 0,5 s, `back.out(1.7)` |
| Mot de la phrase | flou 10 → 0 px, montée 16 px, 0,3 s, `power2.out`, calé 0,04 s avant le mot prononcé |
| Typo cinétique | lignes qui montent derrière un masque, 0,55 s, `power4.out`, une ligne par mot prononcé |
| Sortie | 0,2 à 0,3 s, échelle 0,9 et flou, `power2.in` : toujours plus rapide que l'entrée |
| Flottement | ± 8 à 10 px, période 1,6 à 1,8 s, `sine.inOut` |
| Caméra | poussée lente 1,00 → 1,04-1,05 par scène ; coup de zoom 1,05-1,06 sur un mot fort (≤ 0,6 s) |
| Chiffres, traits | chiffres qui défilent (`power2.out`), traits qui se dessinent (0,45 s) |

Règles : un coup de zoom ne chevauche jamais une transition. L'image 0 montre déjà l'objet principal (c'est la miniature
sur les réseaux). Chaque texte reste lisible au moins 0,5 s + 0,3 s par mot.

---

## 8. Transitions

| Transition | Quand | Code |
|---|---|---|
| Zoom + flou | entre deux parties, sur le même fond | `m.through(t)` |
| Balayage d'accent (bandes diagonales) | pour entrer ou sortir d'un fond éclat, ou d'un chapitre important | `m.wipe(t)` |
| Changement de fond | début d'un chapitre (clair → nuit → clair) | `ground=` sur la scène |
| Rafale finale (option) | avant le logo, sur une vidéo musicale : 4 à 6 plans de 0,2 à 0,3 s | scènes courtes enchaînées |

Pas de flash blanc dur, pas de tremblement.

---

## 9. Rythme

- Une **scène toutes les ~2 à 2,5 s**, à chaque phrase de la voix.
- Un **élément nouveau toutes les 0,4 à 1 s** dans une scène, toujours calé sur un mot.
- Vidéo **sans voix** (musique) : coupes sur le temps, accélération en rafale avant la fin, comme Fitters Bible.
- Structure type : **accroche** (objet visible dès l'image 0) → **pourquoi** → **méthode** (étapes, éclat) →
  **preuve** (nuit, données vraies) → **à toi** (action) → **logo**. Étiquettes HUD « 01 / 04 · … ».

---

## 10. Son

- Voix au premier plan, nettoyée (`npm run voix:claire` si face caméra), vidéo finale à **-14 LUFS** en deux passes.
- Petits sons d'interface sur les apparitions **importantes** seulement, volume 0,12 à 0,2 : `ui` (apparition),
  `clic-focus` (pastille), `validation` (1re coche d'une liste), `clavier-apple` (frappe), `whoosh-court`
  (transition, balayage).
- Réactions de foule (sons validés) : 1 à 3 par vidéo, sur un vrai temps fort.
- Nouveau son : sources autorisées (Openverse, Kenney CC0, Mixkit), choisi avec `earshot`.

---

## 11. Honnêteté

Aucun chiffre, avis, statistique ou résultat inventé. Un compteur, une barre, un anneau ou une grille de points ne montre
qu'une valeur **fournie par l'utilisateur** ; sinon on illustre sans chiffre (jauges sans valeur, cartes génériques).

---

## 12. Avant de livrer

1. `hyperframes check` : 0 erreur, contraste OK.
2. `npm run brand:check` : charte respectée.
3. `npm run marges:check -- projets/<nom>/montage/index.html` : aucun texte près des bords.
4. `hyperframes snapshot` sur chaque scène : rien ne se chevauche, la phrase ne touche pas l'objet central.
5. Rendu `--quality delivery`, son à -14 LUFS, versions HD + légère, descriptions SEO TikTok + YouTube (4 hashtags max).

---

## 13. Ce qui reste valable des styles précédents

- **Face caméra** : bulles « liquid glass » + zooms (`templates/reel-glass/`), sauf demande contraire ; les éléments de
  cette DA (HUD, éclat, typo cinétique) peuvent s'y ajouter entre deux plans.
- Les anciens styles (éditorial, gaming premium, liquid glass « mot derrière la tête », 3D) : seulement sur demande.
