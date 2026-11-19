# Modèle « motion design clair » (`templates/reel-motion/`)

Style demandé par l'utilisateur le 19/11/2026 : « Animations, motion design mais sous mes couleurs ».
Fiche mesurée : `references/style-motion/STYLE.md`. Exemple complet : `projets/agency-motion/scripts/build.py`
(« Sous-titres = vues », voix off). Marche avec les deux marques : `BRAND=specimen-gaming python3 scripts/build.py`.

## Ce qui fait le style

1. **Fond clair de la charte** (ivoire / blanc Agency, blanc Gaming), haut de l'écran en blanc pour le contraste,
   soleil rayé doux et points qui dérivent aux couleurs de la charte (`--mo-deco`).
2. **La phrase en haut**, centrée, qui s'écrit mot à mot au rythme de la voix (défloutage) : mots clés en
   `--mo-kw` (or foncé / rouge), le mot fort dans une **pastille sombre** (`"pill"`). Elle remplace les sous-titres
   dans ce style.
3. **Un objet central par phrase** : téléphone (`.phone`, `.phone.sm`), lecteur (`.player`), fenêtre de montage
   (`.win` avec pistes et tête de lecture), icône d'app (`.app`), barre de recherche tapée (`.prompt` + `m.type()`).
   Dans un cadre paysage, `person(wide=True)` garde le personnage entier.
4. **Éléments qui arrivent sur les mots** : autocollants ronds (`.stk`) avec onde de choc (`.ring` + `m.shock()`),
   cartes flottantes (`.card` + `m.bob()`), pastilles numérotées (`.num`), étapes cochées (`.step` + `.tick`),
   compteur (`.count` + `m.count()`, **seulement avec un vrai chiffre**), jauges (`.meter`).
5. **Caméra** : poussée lente par scène (`m.push`), transition zoom + flou à chaque partie (`m.through`), coups de zoom
   sur les mots forts (`m.punch`), jamais en même temps qu'une transition (sinon HyperFrames signale `gsap_tween_tail`).
6. **Son** : voix au premier plan, petits sons d'interface sur les apparitions importantes seulement (`ui`, `clic-focus`
   pour les pastilles, `validation` pour la 1re coche d'une liste, `clavier-apple` pour la frappe, `whoosh-court` sur
   les transitions), volumes 0,12 à 0,2.

## Utilisation

```python
sys.path.insert(0, f"{REPO}/templates/reel-motion"); from motion import Motion, ICONS as I, person
m = Motion(REPO, ROOT, BRAND)
m.scene("s1", 0.0, 1.5); m.push(0.0, 1.5)
m.say("t1", [(0.06, "Trois", "kw"), (0.25, "mots", "kw"), (1.15, "vues.", "pill")], end=1.5)
m.add(f'<div class="slot" style="top:470px;height:900px"><div class="phone" id="ph"><div class="island"></div><div class="scr">{person()}</div></div></div>')
m.tw("#ph", "{scale: 0.94}", "{scale: 1}", 0.0, 0.8)   # visible dès l'image 0 (miniature)
m.through(1.5)
m.write(MAIN, "assets/voix.wav", VOICE_DUR)
```

Placement : `.slot` (boîte pleine largeur, centre son contenu) ou `.abs` (position libre) ; GSAP anime l'élément
intérieur. La phrase a une réserve intérieure de 50 px pour ne jamais toucher les marges pendant les zooms.

## Avant de livrer

`hyperframes check` (0 erreur, contraste ≥ 3:1), `npm run brand:check`, `npm run marges:check -- <index.html>`,
`hyperframes snapshot` sur chaque scène (une phrase de 4 lignes ne doit pas toucher l'objet central : réduire `size=`
de `m.say()` ou descendre l'objet).
