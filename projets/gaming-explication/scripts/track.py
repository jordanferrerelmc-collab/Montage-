"""Suit le joueur contrôlé (triangle rose au-dessus de sa tête) dans chaque séquence → work/track<i>.json.
Sert au recadrage vertical plein écran : [(t, x_centre en fraction de la largeur)], lissé."""
import json, subprocess, sys, os
import numpy as np
from scipy import ndimage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 10, 1920, 1080
for i in range(1, 5):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{ROOT}/src/clip{i}.mp4", "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    out, n, last = [], 0, None
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.int16)
        r, g, b = f[..., 0], f[..., 1], f[..., 2]
        m = (r > 190) & (g < 90) & (b > 90) & (b < 190) & (r - b > 40)
        m[:60] = False; m[940:] = False          # hors bandeaux / radar
        lab, k = ndimage.label(m)
        x, best = None, None
        for sl in ndimage.find_objects(lab):
            h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
            size = int(m[sl].sum())
            if 14 <= size <= 70 and 5 <= w <= 16 and 4 <= h <= 14:      # le triangle : petit et compact
                y0, y1, x0, x1 = max(0, sl[0].start - 14), sl[0].stop + 14, max(0, sl[1].start - 14), sl[1].stop + 14
                ring = f[y0:y1, x0:x1].reshape(-1, 3).mean(0)
                if not (ring[1] > ring[0] + 25 and ring[1] > ring[2] + 25):   # doit être entouré de pelouse (pas la tribune)
                    continue
                cx = (sl[1].start + sl[1].stop) / 2 / W
                d = abs(cx - last) if last is not None else 0
                if best is None or d < best[0]:
                    best = (d, cx)
        if best: x = best[1]; last = x
        xs = np.zeros(int(m.sum()))
        out.append([n / FPS, x, int(len(xs))]); n += 1
    json.dump(out, open(f"{ROOT}/work/track{i}.json", "w"))
    found = [o for o in out if o[1] is not None]
    print(i, n, "images,", len(found), "détections ;", " ".join(f"{o[1]:.2f}" if o[1] is not None else "--" for o in out[::5]))
