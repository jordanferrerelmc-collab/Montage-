"""Démo d'application aux couleurs Specimen (skill html-demo adapté) : voir templates/app-demo/README.md."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
sys.path.insert(0, f"{REPO}/templates/app-demo")
from build_app_demo import build

build(root=ROOT, brand="specimen-gaming", steps_js=f"{ROOT}/scripts/steps.js",
      kicker="SPECIMEN GAMING · TACTIQUE", title="Ma 4-3-1-2<br><span class='a'>en 4 étapes</span>",
      tabs=["Tactiques", "XI SPM"], label="Tactique 4-3-1-2")
