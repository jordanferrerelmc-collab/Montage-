"""Démo d'application aux couleurs Specimen (skill html-demo adapté) : voir templates/app-demo/README.md."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
sys.path.insert(0, f"{REPO}/templates/app-demo")
from build_app_demo import build

build(root=ROOT, brand="specimen-agency", steps_js=f"{ROOT}/scripts/steps.js",
      kicker="SPECIMEN AGENCY · PROCESS", title="Du rush<br><span class='a'>au Reel</span>",
      tabs=["Montage", "video1.mp4"], label="Du rush au Reel")
