"""Héros FC 27 : resserre les blancs de la voix (début rapide) → montage/assets/voix.wav + work/timemap.json.
Chaque silence (> 0,3 s sous -40 dB) est ramené à KEEP secondes ; les mots sont recalés par build.py."""
import json, os, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = 0.16
log = subprocess.run(["ffmpeg", "-i", f"{ROOT}/src/voix.mp3", "-af", "silencedetect=n=-40dB:d=0.3", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
cuts = [(a + KEEP / 2, b - KEEP / 2) for a, b in zip(st, en) if a > 0.05 and b - a > KEEP]   # segments retirés
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{ROOT}/src/voix.mp3"],
                           capture_output=True, text=True).stdout)
keep, t = [], 0.0
for a, b in cuts:
    keep.append((t, a)); t = b
keep.append((t, dur))
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b - a - 0.012:.3f}:d=0.012[s{k}];"
            for k, (a, b) in enumerate(keep))
f += "".join(f"[s{k}]" for k in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[o]"
os.makedirs(f"{ROOT}/work", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/src/voix.mp3", "-filter_complex", f, "-map", "[o]", "-ar", "48000", "-ac", "1",
                f"{ROOT}/montage/assets/voix.wav"], check=True)
json.dump(cuts, open(f"{ROOT}/work/timemap.json", "w"))
print(f"voix : {dur:.2f} s → {dur - sum(b - a for a, b in cuts):.2f} s ({len(cuts)} blancs resserrés)")

# cartes : découpées dans src/cartes.jpg (visuel fourni, non versionné) → montage/assets/cartes/<nom>.jpg
from PIL import Image, ImageFilter
CARTES = {"silva": (170, 48, 357, 288), "rossi": (368, 48, 555, 288), "kerimoglu": (566, 50, 748, 292), "carrick": (763, 50, 946, 292),
          "nasri": (960, 50, 1144, 292), "toure": (170, 298, 354, 542), "hyypia": (368, 298, 552, 542), "vandervaart": (566, 298, 750, 542),
          "defoe": (763, 298, 947, 542), "jota": (960, 298, 1144, 542), "baines": (368, 550, 552, 792), "pedersen": (566, 550, 750, 792),
          "sturridge": (763, 550, 947, 792)}
im = Image.open(f"{ROOT}/src/cartes.jpg").convert("RGB")
os.makedirs(f"{ROOT}/montage/assets/cartes", exist_ok=True)
for k, box in CARTES.items():
    c = im.crop(box)
    c.resize((c.width * 3, c.height * 3), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2)).save(
        f"{ROOT}/montage/assets/cartes/{k}.jpg", quality=93)
print(f"{len(CARTES)} cartes découpées")
