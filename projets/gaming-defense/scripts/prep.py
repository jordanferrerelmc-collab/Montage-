"""Recadre les séquences de jeu (1920×1080) en vertical plein écran 1080×1920 en suivant le joueur contrôlé
(work/track<i>.json, scripts/track.py), puis assemble les plans calés sur la voix → montage/assets/plans.mp4.

Usage : python3 prep.py            (montage complet)
        python3 prep.py apercu     (planches work/v<i>.jpg pour repérer les moments clés)
"""
import json, os, subprocess, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, CW, FPS = 1920, 1080, 608, 30
FORCE = {}      # pas de cadrage imposé

def path(i):
    """Centre du cadrage (fraction) lissé, échantillonné à 30 i/s sur toute la séquence."""
    tr = json.load(open(f"{ROOT}/work/track{i}.json"))
    t = np.array([o[0] for o in tr]); x = np.array([np.nan if o[1] is None else o[1] for o in tr])
    ok = ~np.isnan(x); x = np.interp(t, t[ok], x[ok])
    x = np.array([np.median(x[max(0, k - 2):k + 3]) for k in range(len(x))])       # retire les sauts isolés
    tt = np.arange(0, t[-1] + 0.2, 1 / FPS); xs = np.interp(tt, t, x)
    for t0, v in FORCE.get(i, []):                                                 # cadrage imposé (ex. le but)
        xs[tt >= t0] = v
    out, cur, vel = [], xs[0], 0.0
    for v in xs:                                                                  # ressort amorti : panoramique fluide
        vel = vel * 0.80 + (v - cur) * 0.035; cur += vel; out.append(cur)
    return np.clip(np.array(out), CW / 2 / W, 1 - CW / 2 / W)

def frames(i, t0, dur):
    """Images recadrées (608×1080 RGB) de la séquence i entre t0 et t0+dur."""
    px = path(i)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", f"{ROOT}/src/clip{i}.mp4", "-vf", f"fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    k = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        c = px[min(len(px) - 1, int(round(t0 * FPS)) + k)]
        x0 = int(round(c * W - CW / 2)); x0 = max(0, min(W - CW, x0))
        yield f[:, x0:x0 + CW]
        k += 1

def encoder(out, extra=()):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{CW}x{H}", "-r", str(FPS), "-i", "-",
                             *extra, "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                             "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)

if len(sys.argv) > 1 and sys.argv[1] == "apercu":
    for i in range(1, 2):
        e = encoder(f"{ROOT}/work/v{i}.mp4")
        for f in frames(i, 0, 99): e.stdin.write(f.tobytes())
        e.stdin.close(); e.wait()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/work/v{i}.mp4", "-vf",
                        "fps=2,scale=150:-2,drawtext=text='%{pts\\:hms}':x=2:y=2:fontsize=13:fontcolor=white:box=1:boxcolor=black,tile=10x2:padding=2",
                        f"{ROOT}/work/v{i}.jpg"])
    sys.exit()

# plans : (séquence, début dans la séquence, durée) dans l'ordre de la voix
PLANS = json.load(open(f"{ROOT}/scripts/plans.json"))
e = encoder(f"{ROOT}/work/plans_video.mp4")
n = 0
for i, t0, d in PLANS:
    want = int(round(d * FPS)); got = 0; last = None
    for f in frames(i, t0, d + 0.2):
        if got >= want: break
        e.stdin.write(f.tobytes()); last = f; got += 1
    while got < want and last is not None:                      # fige la dernière image si la séquence est trop courte
        e.stdin.write(last.tobytes()); got += 1
    n += got
e.stdin.close(); e.wait()
# son du jeu : mêmes plans, bout à bout
parts = "".join(f"[{k}:a]atrim={t0}:{t0 + d},asetpts=PTS-STARTPTS,apad=whole_dur={d},atrim=0:{d}[a{k}];" for k, (i, t0, d) in enumerate(PLANS))
ins = sum((["-i", f"{ROOT}/src/clip{i}.mp4"] for i, _, _ in PLANS), [])
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
                parts + "".join(f"[a{k}]" for k in range(len(PLANS))) + f"concat=n={len(PLANS)}:v=0:a=1[a]", "-map", "[a]", "-ar", "48000", f"{ROOT}/work/plans_audio.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/work/plans_video.mp4", "-i", f"{ROOT}/work/plans_audio.wav", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k", "-shortest", f"{ROOT}/montage/assets/plans.mp4"], check=True)
print(f"plans.mp4 : {n / FPS:.2f} s, {len(PLANS)} plans")
