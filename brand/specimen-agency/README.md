# Charte vidéo — Specimen Agency

> « Votre image. Notre expertise. »

Cette charte est **verrouillée** : toutes les vidéos du dépôt l'utilisent. `npm run brand:check`
refuse toute couleur qui n'est pas listée ici.

## Couleurs

| Rôle | Variable | Valeur |
|---|---|---|
| Or (accent principal, mots clés) | `--gold` | `#e3b25c` |
| Or clair (accent secondaire) | `--gold-light` | `#f2d58e` |
| Or profond | `--gold-deep` | `#b8863b` |
| Dégradé or (CTA, écran de fin) | `--gold-grad` | `#f0cd7c → #e1b667 → #c79c4d → #bd8e3e` |
| Noir profond (cartes, pastilles) | `--black` / `--panel` | `#0b0b0d` / `rgba(11,11,13,.9)` |
| Ivoire (textes des cartes, bulles) | `--ivory` | `#f7f1e3` |
| Blanc (sous-titres) | `--ink` | `#ffffff` |
| Flash de transition | `--flash` | `#fff8e8` |
| Neutres (éléments « avant », inactifs) | `--taupe`, `--stone`, `--dark` | `#8a8378`, `#a59d90`, `#4a4540` |

Interdit : rouge, vert, rose, bleu, ou toute autre teinte.

## Typographie

Montserrat (repli : Inter). Sous-titres en 900 et en capitales. Titres de cartes en 800.
Textes de marque (slogan, kicker) en capitales avec lettres espacées (0.16 à 0.22em).

## Composants

- **Sous-titres** : blancs, contour noir de 14 px, ombre portée. Mot clé en `.hl` (or), mot clé secondaire en `.hl-soft` (or clair).
- **Cartes** `.panel` : fond noir translucide, liseré or de 4 px, coins arrondis de 44 px.
- **Pastilles** `.num-badge` : cercle noir, anneau or, chiffre or.
- **Tampon** `.stamp` : fond noir, cadre et texte or, incliné de -10°.
- **CTA** `.cta` : pilule en dégradé or, texte noir.
- **Transitions** : flash ivoire (`#flash`) et flash d'accent or (`#accentflash`).
- **Écran de fin** : fond dégradé or, logo rond (`logo.png`, 700 px) et slogan sur deux lignes.

## Fichiers

- `brand.css` : variables et composants, injectés dans chaque composition.
- `brand.json` : palette autorisée (utilisée par le vérificateur), slogan, règles d'usage.
- `logo.png` : logo rond détouré. `logo_full.jpg` : visuel d'origine.
