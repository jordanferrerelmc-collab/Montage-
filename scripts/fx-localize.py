#!/usr/bin/env python3
"""Fait pointer les éléments du catalogue (effets/compositions) vers la copie locale de GSAP
(effets/vendor/gsap) au lieu de cdn.jsdelivr.net. À relancer après chaque `hyperframes add`."""
import glob, os, re
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "effets")
n = 0
for f in glob.glob(f"{ROOT}/compositions/**/*.html", recursive=True):
    s = open(f, encoding="utf-8").read()
    rel = os.path.relpath(f"{ROOT}/vendor/gsap", os.path.dirname(f))
    s2 = re.sub(r"https://cdn\.jsdelivr\.net/npm/gsap@[\d.]+/dist/", rel + "/", s)
    if s2 != s:
        open(f, "w", encoding="utf-8").write(s2); n += 1
print(f"{n} fichier(s) basculé(s) sur GSAP local")
