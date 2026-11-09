# Style : « Vidéo liquide glass »

Copié de https://www.instagram.com/reel/DYmV4ZoxVAl/ (enregistrement d'écran fourni, 12,7 s), mesuré le 09/11/2026.
Modèle : `templates/reel-liquid-glass/`. Test : `projets/video1/scripts/build_liquid_glass.py` → `projets/video1/final/video1-liquid-glass-*.mp4`.
Marques : **Specimen Agency ou Specimen Gaming selon le sujet** (règle de CLAUDE.md). Couleurs et police : celles de la charte, jamais celles de l'original.

## Structure (mesurée)
- 0 → 3,6 s : accroche face caméra, plan large qui se resserre (poussée de caméra continue, visage ~7 → 10 % de la hauteur, ≈ +12 % en 3,5 s).
- 3,6 s : transition en flou plein cadre (défocalisation + flou de mouvement), impact grave, la musique démarre.
- 3,6 → 12,7 s : B-roll (drone FPV) en coupes franches sur le rythme : 10 plans en 9 s (≈ 0,9 s par plan) ;
  les coupes « fouettées » sont des flous de mouvement de 0,1 à 0,2 s.

## Coupes / transitions
- Dans la partie face caméra : pas de coupe visible, une seule transition « lentille » à la fin de l'accroche.
- Copie : transition « lentille » (flou 22 px + légère surexposition, 0,22 s avant → 0,28 s après) à chaque changement de section.
## Cadrage
- Poussée lente continue (+6 % par section dans la copie), cadrages alternés entre sections (1,00 / 1,10).
## Sous-titres
- Italique, blanc, gras, interlettrage serré (≈ -0,045 em), ombre douce, 1 à 3 mots ; chaque mot entre et sort en flou (≈ 0,15-0,2 s).
- Hauteur : petites lignes au-dessus de la tête, mots isolés à hauteur de poitrine.
- Copie : Specimen Heros gras incliné, 78 px, poitrine (1270-1310 px), mots clés à la couleur d'accent.
## Mot géant « verre liquide »
- Un mot clé énorme (≈ 230 px), majuscules inclinées, rempli d'un dégradé coloré semi-opaque, **derrière la tête**
  (sujet détouré par-dessus), encadré d'une petite ligne italique au-dessus et d'une autre décalée en dessous.
- Copie : dégradé de la charte (Agency noir → or foncé → ivoire ; Gaming rouge foncé → rouge → blanc) avec reflet
  qui glisse pendant toute la durée du mot ; entrée floutée + léger zoom arrière.
## Son
- Accroche : voix seule ; montée (riser) de 2,3 à 3,55 s ; **impact grave** + début de musique électronique à 3,6 s.
- Après : coups aigus sur les coupes (4,54 / 5,22 / 5,68 / 6,38 / 8,22 / 8,92 / 10,08 s), coups graves ≈ toutes les 1,4-2 s.
- Niveau global -12 LUFS (on livre à -14).
- Copie : impact-boom sur la fin de l'accroche, whoosh-court discret sur chaque transition, impact-sec sur le logo.
  Riser **non copié** (déjà rejeté une fois, voir `.agents/skills/steal/references/learnings.md`).
## Étalonnage
- Lumineux, saturé, chaud dans les hautes lumières, ciel bleu profond. Copie : `npm run grade -- in out or-chaud --force 0.6`
  (Gaming : `punchy-gaming`).
## Laissé de côté
- Couleurs (orange / violet) et police d'origine : remplacées par la charte.
- B-roll drone : à fournir par l'utilisateur (aucun dans video1) ; le modèle a un emplacement `{{BROLL}}`.
- Musique : aucune piste libre dans le dépôt ; à fournir, calée pour démarrer sur la transition de fin d'accroche.
## Écarts relevés à la comparaison (compare.jpg)
- Sur un mur jaune, le verre doré contraste moins que l'orange / violet de l'original : garder la ligne ivoire du dégradé,
  ou placer le mot sur une zone sombre. En Gaming, le rouge ressort davantage.
