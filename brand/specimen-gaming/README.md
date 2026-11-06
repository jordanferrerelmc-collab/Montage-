# Charte vidéo — Specimen Gaming (TikTok)

Charte **verrouillée** du compte TikTok gaming. `npm run brand:check` refuse toute couleur non listée
ici et toute police autre que TeX Gyre Heros (Helvetica Neue) dans les vidéos marquées `specimen-gaming`.

## Couleurs (tirées du logo)

| Rôle | Variable | Valeur |
|---|---|---|
| Rouge (accent principal) | `--red` / `--accent` | `#da3d39` |
| Rouge clair (mots clés des sous-titres, plus lisible) | `--red-light` | `#ff5a4e` |
| Rouge foncé (ombres, dégradé) | `--red-dark` | `#a82a27` |
| Anthracite (fond du logo, écran de fin) | `--charcoal` | `#2c2d32` |
| Anthracite profond (cartes) | `--charcoal-deep` / `--panel` | `#1c1d21` / `rgba(28,29,33,.92)` |
| Blanc (sous-titres, manette) | `--ink` | `#ffffff` |
| Argent (éléments secondaires) | `--silver` | `#c9cbd1` |

Interdit : or, jaune, vert, bleu, rose, ou toute autre teinte.

## Typographie (verrouillée, commune aux deux marques)

**Une seule police : Helvetica Neue**, la police du Reel de référence. Elle est payante, on utilise donc son
équivalent libre **TeX Gyre Heros** (licence GUST, usage commercial autorisé). Les fichiers d'origine sont dans
`fonts/` (`texgyreheros-regular.otf`, `texgyreheros-bold.otf`, licence `GUST-FONT-LICENSE.txt`). La police est
déclarée sous le nom `"Specimen Heros"` : le rendu ne dépend ni d'Internet ni des polices installées.

| Usage | Graisse | Style |
|---|---|---|
| Sous-titres | 700 | Casse du discours, lettres resserrées (-0.02em) |
| Grands titres | 700 | Petite ligne en minuscules + très grande ligne en capitales (-0.045em) |
| Étiquettes de cartes | 700 | Capitales espacées |
| Textes courants | 400 | — |

Toute autre `font-family` est refusée par `npm run brand:check`.

## Style gaming

- **Cartes** : fond anthracite, liseré rouge, ombre rouge décalée (8 px), angles peu arrondis.
- **Pastilles numérotées** : carrés rouges inclinés, chiffre blanc.
- **Tampon** : bloc rouge à cadre blanc, incliné.
- **CTA** : bandeau rouge biseauté, texte blanc.
- **Transitions** : flash blanc, flash d'accent rouge.
- **Écran de fin** : fond anthracite, logo horizontal centré, sans slogan.

## Mise en page TikTok

Les sous-titres sont remontés (haut à 1120 px) et décalés vers la gauche (largeur 860 px). Ils évitent
ainsi la colonne d'icônes à droite et la légende en bas. Les illustrations commencent à 230 px, sous les
onglets « Abonnements / Pour toi ».

## Fichiers

- `brand.css` : variables, composants et mise en page, injectés dans chaque composition.
- `brand.json` : palette autorisée, police, règles.
- `fonts/` : Oxanium et sa licence.
- `logo.png` : logo horizontal (fond anthracite). `logo_full.jpg` : visuel d'origine.
