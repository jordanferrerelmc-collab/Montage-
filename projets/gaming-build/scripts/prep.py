"""Assemble les plans verticaux 1080×1920 calés sur la voix → montage/assets/plans.mp4 (vidéo) + son du jeu.

Deux types de plans (scripts/plans.json) :
  ["g", séquence, début, durée]                 jeu : recadrage plein écran qui suit le joueur (work/track<i>.json)
  ["m", zone, début, durée_source, durée]       menu : zone utile agrandie (1000 px de large, liseré de la charte)
                                                sur le même écran flouté ; écran fixe étiré si la source est courte
"""
import json, os, subprocess, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, CW, FPS = 1920, 1080, 608, 30
# zones utiles des menus dans la source : x, y, largeur, hauteur
ROI = {"carte": (80, 370, 780, 530), "stat": (1290, 190, 536, 310), "style": (1250, 190, 574, 450), "corps": (96, 300, 574, 400)}
RED = "0xda3d39"

def path(i):
    tr = json.load(open(f"{ROOT}/work/track{i}.json"))
    t = np.array([o[0] for o in tr]); x = np.array([np.nan if o[1] is None else o[1] for o in tr])
    ok = ~np.isnan(x); x = np.interp(t, t[ok], x[ok])
    x = np.array([np.median(x[max(0, k - 2):k + 3]) for k in range(len(x))])
    tt = np.arange(0, t[-1] + 0.2, 1 / FPS); xs = np.interp(tt, t, x)
    out, cur, vel = [], xs[0], 0.0
    for v in xs:
        vel = vel * 0.80 + (v - cur) * 0.035; cur += vel; out.append(cur)
    return np.clip(np.array(out), CW / 2 / W, 1 - CW / 2 / W)

def game(i, t0, d, out):
    px = path(i); want = int(round(d * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-i", f"{ROOT}/src/clip{i}.mp4", "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    e = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{CW}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    got, last = 0, None
    while got < want:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            if last is None: break
            e.stdin.write(last); got += 1; continue           # fige la dernière image si la séquence est trop courte
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        c = px[min(len(px) - 1, int(round(t0 * FPS)) + got)]
        x0 = max(0, min(W - CW, int(round(c * W - CW / 2))))
        last = f[:, x0:x0 + CW].tobytes(); e.stdin.write(last); got += 1
    p.kill(); e.stdin.close(); e.wait()

def menu(roi, t0, sd, d, out):
    x, y, w, h = ROI[roi]
    fh = int(round(1000 * h / w / 2) * 2)                       # hauteur du panneau à 1000 px de large
    bx = max(0, min(W - CW, x + w // 2 - CW // 2))              # fond : même écran, recadré autour de la zone, flouté
    fc = (f"[0:v]setpts=PTS*{d / sd:.5f},fps={FPS},split[a][b];"
          f"[a]crop={CW}:{H}:{bx}:0,scale=1080:1920,boxblur=24:2,eq=brightness=-0.22:saturation=0.8[bg];"
          f"[b]crop={w}:{h}:{x}:{y},scale=1000:{fh}:flags=lanczos,pad=1012:{fh + 12}:6:6:color={RED}[fg];"
          f"[bg][fg]overlay=34:{900 - (fh + 12) // 2}[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{sd}", "-i", f"{ROOT}/src/clip1.mp4", "-filter_complex", fc, "-map", "[v]",
                    "-frames:v", str(int(round(d * FPS))), "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", out], check=True)

PLANS = json.load(open(f"{ROOT}/scripts/plans.json"))
os.makedirs(f"{ROOT}/work/seg", exist_ok=True)
lst, aud_in, aud_f, total = [], [], [], 0.0
for k, pl in enumerate(PLANS):
    out = f"{ROOT}/work/seg/s{k:02d}.mp4"
    if pl[0] == "g":
        _, i, t0, d = pl; game(i, t0, d, out)
        aud_in += ["-i", f"{ROOT}/src/clip{i}.mp4"]
        aud_f.append(f"[{k}:a]atrim={t0}:{t0 + d},asetpts=PTS-STARTPTS,apad=whole_dur={d},atrim=0:{d}[a{k}]")
    else:
        _, roi, t0, sd, d = pl; menu(roi, t0, sd, d, out)
        aud_in += ["-f", "lavfi", "-t", f"{d}", "-i", "anullsrc=r=48000:cl=stereo"]     # menus : pas de son du jeu
        aud_f.append(f"[{k}:a]atrim=0:{d},asetpts=PTS-STARTPTS[a{k}]")
    lst.append(f"file 's{k:02d}.mp4'"); total += pl[-1]
open(f"{ROOT}/work/seg/list.txt", "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{ROOT}/work/seg/list.txt", "-c", "copy", f"{ROOT}/work/plans_video.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *aud_in, "-filter_complex", ";".join(aud_f) + ";" + "".join(f"[a{k}]" for k in range(len(PLANS)))
                + f"concat=n={len(PLANS)}:v=0:a=1,aresample=48000[a]", "-map", "[a]", f"{ROOT}/work/plans_audio.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/work/plans_video.mp4", "-i", f"{ROOT}/work/plans_audio.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                f"{ROOT}/montage/assets/plans.mp4"], check=True)
print(f"plans.mp4 : {total:.2f} s prévues, {len(PLANS)} plans")
