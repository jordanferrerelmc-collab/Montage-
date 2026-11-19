# Style « motion design clair » — fiche mesurée (19/11/2026)

Référence envoyée par l'utilisateur : « Le style que je veux pour mes montages. Animations, motion design mais sous mes
couleurs ». Vidéo de 27,7 s, horizontale (écran filmé), voix off seule ; fichier non versionné (`work/`).
Mesures faites avec ffmpeg (planche 1 image/s, séquences à 5 images/s, spectrogramme) et la transcription HyperFrames.

## Mesures

| Élément | Valeur mesurée | Application chez nous |
|---|---|---|
| Débit de la voix | 3,1 mots/s (89 mots en 28,5 s) | phrases courtes, rythme serré |
| Changement de scène | 12 idées visuelles en 27 s → **une scène toutes les ~2,3 s**, à chaque phrase | `m.scene()` + `m.through()` à chaque phrase |
| Coupes franches | aucune (détection de scène à 0,25 : 0) : tout est animé en continu | jamais de coupe sèche |
| Ajouts dans une scène | un nouvel élément toutes les 0,4 à 1 s, calé sur le mot prononcé | `m.pop(sel, W[i])` |
| Texte | phrase complète **en haut**, centrée, gris très foncé, mot à mot avec défloutage ; 1 à 2 mots clés en couleur ; le mot fort dans une **pastille sombre** avec un petit triangle | `m.say()` (kinds `kw` / `pill`) |
| Objet central | un seul à la fois : téléphone, lecteur vidéo, fenêtre de montage, icône d'app, barre de recherche, cartes | classes `.phone`, `.player`, `.win`, `.app`, `.prompt` |
| Entrées | ressort + défloutage (≈ 0,5 s, léger dépassement), sorties floutées | `m.pop()` / `m.out()` |
| Éléments secondaires | pastilles numérotées 1, 2… puis coches ; cartes de notification flottantes ; compteur qui défile ; badge d'heure ; onde de choc autour des icônes | `.num`, `m.tick()`, `.card` + `m.bob()`, `m.count()`, `m.shock()` |
| Décor | fond clair + décor illustré lié au sujet, très doux, qui reste en place | fond de la charte + soleil rayé aux couleurs de la charte (`#deco`) |
| Son | voix au premier plan, pas de musique marquée ; petits « pop / clic » sur les apparitions (traits verticaux du spectrogramme) | `ui`, `clic-focus`, `validation`, `whoosh-court`, volume 0,12 à 0,2 |

## Ce qu'on ne copie pas

- Les couleurs (rose / pêche / violet) et le décor du sujet de la référence (palmiers, coucher de soleil de jeu) : on
  utilise les couleurs `--mo-*` de la charte Specimen choisie et un décor maison.
- Les logos et interfaces réels (TikTok, YouTube, bande-annonce, application « MotionLab ») : illustrations maison seulement.
- Les chiffres : un compteur n'affiche qu'un **vrai** chiffre donné par l'utilisateur (`m.count()`).

## Adaptation 9:16 (Reels / TikTok)

Phrase en haut (Agency 200 px, Gaming 250 px sous la signature), objet central entre ~500 et 1300 px, liste / cartes
entre 1250 et 1650 px, rien sous 1690 px ni à moins de 90 px (Agency) / 110 px (Gaming) des côtés
(`npm run marges:check`). Modèle : `templates/reel-motion/`, exemple : `projets/agency-motion/`.
