"""Suit le joueur de l'utilisateur en Clubs (marqueurs jaunes : triangle, étoile, croix) dans les séquences de jeu
2 à 4 → work/track<i>.json : [(t, x_centre en fraction de la largeur ou null, nb de pixels jaunes)]."""
import json, subprocess, os
import numpy as np
from scipy import ndimage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 10, 1920, 1080
for i in (2, 3, 4):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{ROOT}/src/clip{i}.mp4", "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    out, n, last = [], 0, None
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.int16)
        r, g, b = f[..., 0], f[..., 1], f[..., 2]
        m = (r > 215) & (g > 195) & (b < 90)
        m[:90] = False; m[930:] = False                       # hors bandeaux / radar
        lab, k = ndimage.label(m)
        x, best = None, None
        for sl in ndimage.find_objects(lab):
            h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
            size = int(m[sl].sum())
            if not (12 <= size <= 420 and w <= 34 and h <= 34):   # petits marqueurs (pas la cage surlignée)
                continue
            y0, y1, x0, x1 = max(0, sl[0].start - 14), sl[0].stop + 14, max(0, sl[1].start - 14), sl[1].stop + 14
            ring = f[y0:y1, x0:x1].reshape(-1, 3).mean(0)
            if not (ring[1] > ring[0] + 15 and ring[1] > ring[2] + 25):   # entouré de pelouse
                continue
            cx = (sl[1].start + sl[1].stop) / 2 / W
            d = abs(cx - last) if last is not None else 0
            if best is None or d < best[0]: best = (d, cx)
        if best: x = best[1]; last = x
        out.append([n / FPS, x, int(m.sum())]); n += 1
    json.dump(out, open(f"{ROOT}/work/track{i}.json", "w"))
    print(i, n, "images,", sum(o[1] is not None for o in out), "détections ;", " ".join(f"{o[1]:.2f}" if o[1] is not None else "--" for o in out[::5]))
