"""Coupe les blancs : détecte les passages sous un seuil (RMS par fenêtres de 20 ms),
garde une marge autour de la parole et assemble les segments (ffmpeg trim/concat).
Écrit cut.mp4 + cuts.json (segments conservés, pour recaler la transcription)."""
import json, subprocess, sys, numpy as np, soundfile as sf

src, wav, out = sys.argv[1:4]
THR_DB, MIN_GAP, PAD = -35.0, 0.15, 0.04

x, sr = sf.read(wav)
h = int(sr * 0.02)
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + h] ** 2)) + 1e-9) for i in range(0, len(x) - h, h)])
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", src]))
gaps, s = [], None
for i, q in enumerate(db < THR_DB):
    if q and s is None: s = i
    if (not q or i == len(db) - 1) and s is not None:
        a, b = s * 0.02, i * 0.02
        if b - a >= MIN_GAP: gaps.append((a, b))
        s = None
keep, t = [], 0.0
for a, b in gaps:
    a2 = a + PAD if a > 0 else a
    b2 = b - PAD
    if a2 > t: keep.append((t, a2))
    t = max(t, b2)
keep.append((t, dur))
keep = [(round(a, 3), round(b, 3)) for a, b in keep if b - a > 0.05]

parts, labels = [], []
for i, (a, b) in enumerate(keep):
    parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                 f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                 f"afade=t=out:st={b - a - 0.012:.3f}:d=0.012[a{i}];")
    labels.append(f"[v{i}][a{i}]")
fc = "".join(parts) + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", out], check=True)
json.dump({"keep": keep}, open(out.rsplit(".", 1)[0] + "_cuts.json", "w"), indent=1)
removed = dur - sum(b - a for a, b in keep)
print(f"{len(keep)} segments, {removed:.2f} s de blancs retirés, durée {dur - removed:.2f} s")
