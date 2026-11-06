# Charte vidéo — Specimen Gaming (TikTok)

Charte **verrouillée** du compte TikTok gaming. `npm run brand:check` refuse toute couleur non listée
ici et toute police autre qu'Oxanium dans les vidéos marquées `specimen-gaming`.

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

## Typographie (verrouillée)

**Une seule police : Oxanium**, au lettrage carré proche de celui du logo. Le fichier est embarqué dans
`fonts/Oxanium-Variable.woff2` (graisses 200 à 800, licence SIL OFL : voir `fonts/OFL.txt`) et déclaré sous le nom
`"Specimen Oxanium"`.

| Usage | Graisse | Style |
|---|---|---|
| Sous-titres | 800 | Capitales, contour noir |
| Titres des cartes | 800 | Capitales |
| Petits titres (kicker) | 700 | Capitales, lettres espacées 0.14em |
| Bulles de dialogue | 600 | Casse normale |

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
