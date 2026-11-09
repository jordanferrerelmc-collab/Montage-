# templates/reel-liquid-glass — style « Vidéo liquide glass »

Mesures et règles : `references/video-liquide-glass/STYLE.md`. Exemple complet : `projets/video1/scripts/build_liquid_glass.py`
(`BRAND=specimen-gaming python3 ...` pour la charte gaming).

Le modèle attend dans `montage-liquid/assets/` : `cut.mp4` (vidéo coupée), `subject.webm` (sujet détouré,
`hyperframes remove-background`), la charte et `effets/sfx/`. Marqueurs : `{{BEHIND}}` (mots en verre, entre la vidéo et le
sujet détouré), `{{BROLL}}` (plans de coupe plein cadre), `{{CAPTIONS}}`, `{{SOFTEN}}` (`block` si la source a des
sous-titres incrustés), `{{ENDCARD}}`, `{{SFX}}`, `{{JS}}`.
