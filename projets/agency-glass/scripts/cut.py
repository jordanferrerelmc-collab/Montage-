"""Coupe serrée : retire tous les blancs de plus de 0,16 s (mesurés sur la voix nettoyée) et la 2e prise
« Et écris ta ville… boutique à Saint-Denis » (18,54-24,2 s dans la source), doublon de la 1re.
Garde 0,07 s avant et après chaque passage parlé. Sortie : montage/assets/cut.mp4 (1080×1920, 30 i/s) + work/segments.json."""
import json, os, subprocess
import numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x, sr = sf.read(f"{ROOT}/work/voix_claire.wav"); hop = int(sr * 0.01)
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
speech = db > -42                                   # voix nettoyée : plancher ≈ -66 dB, voix ≈ -15 dB
EXCLUDE = [(18.50, 24.70)]                          # 2e prise (doublon)
KEEP_RANGE = (0.0, 37.25)
MIN_GAP, PAD = 0.16, 0.07
# passages parlés
runs, on = [], None
for i, s in enumerate(speech):
    t = i * 0.01
    if s and on is None: on = t
    if not s and on is not None: runs.append([on, t]); on = None
if on is not None: runs.append([on, len(speech) * 0.01])
runs = [r for r in runs if r[1] - r[0] >= 0.05]     # retire les clics isolés
# fusionne les passages séparés de moins de MIN_GAP (respirations naturelles entre deux mots)
merged = []
for a, b in runs:
    if merged and a - merged[-1][1] < MIN_GAP: merged[-1][1] = b
    else: merged.append([a, b])
segs = []
for a, b in merged:
    a, b = max(KEEP_RANGE[0], a - PAD), min(KEEP_RANGE[1], b + PAD)
    for ea, eb in EXCLUDE:                              # retire la 2e prise
        if a < eb and b > ea:
            if a < ea: segs.append([a, ea])
            a = max(a, eb)
    if b - a > 0.08: segs.append([round(a, 2), round(b, 2)])
total = sum(b - a for a, b in segs)
print(f"{len(segs)} passages gardés, {total:.2f} s (source 37,6 s)")
json.dump(segs, open(f"{ROOT}/work/segments.json", "w"))
f, ins = "", ""
for n, (a, b) in enumerate(segs):
    f += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v{n}];"
          f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b - a - 0.02:.3f}:d=0.02[a{n}];")
    ins += f"[v{n}][a{n}]"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{ROOT}/src/source.mp4", "-i", f"{ROOT}/work/voix_claire.wav",
                "-filter_complex", f + ins + f"concat=n={len(segs)}:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                f"{ROOT}/montage/assets/cut.mp4"], check=True)
