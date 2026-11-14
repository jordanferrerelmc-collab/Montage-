"""Pack opening FC 27 (n° 2, Origines déchaînées) : recadre l'ouverture du pack (1920×1080) en vertical 1080×1920, un plan toutes les ~1,5 s,
calé sur la voix ; insère 1 s de silence avant la révélation (voix et son du jeu coupés).

Sorties : montage/assets/plans.mp4 (image + son du jeu), montage/assets/voix.wav (voix avec le silence).
"""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1920, 1080, 30
VCUT, GAP = None, 0.0           # pas de silence inséré dans ce montage

# (début dans la source, durée, centre x, largeur du cadrage, centre y, gain du son du jeu)
PLANS = json.load(open(f"{ROOT}/scripts/plans.json"))

def crop(cx, cw, cy):
    ch = round(cw * 1920 / 1080)
    x0 = max(0, min(W - cw, round(cx * W - cw / 2))); y0 = max(0, min(H - ch, round(cy * H - ch / 2)))
    return f"crop={cw}:{ch}:{x0}:{y0},scale=1080:1920:flags=lanczos,setsar=1,fps={FPS}"

os.makedirs(f"{ROOT}/work", exist_ok=True)
parts = []
for k, (t0, d, cx, cw, cy, g) in enumerate(PLANS):
    out = f"{ROOT}/work/p{k:02d}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-i", f"{ROOT}/src/clip1.mp4", "-t", f"{d}",
                    "-vf", crop(cx, cw, cy), "-af", f"volume={g},aresample=48000,apad=whole_dur={d},atrim=0:{d}",
                    "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-frames:v", str(round(d * FPS)),
                    out.replace(".mp4", ".mkv")], check=True)
    parts.append(out.replace(".mp4", ".mkv"))
open(f"{ROOT}/work/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{ROOT}/work/list.txt", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", f"{ROOT}/montage/assets/plans.mp4"], check=True)

# voix (pas de silence inséré)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/src/voix.mp3", "-ar", "48000", "-ac", "1", f"{ROOT}/montage/assets/voix.wav"], check=True) if not GAP else subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{ROOT}/src/voix.mp3", "-filter_complex",
                f"[0:a]aresample=48000,asplit[a][b];[a]atrim=0:{VCUT},afade=t=out:st={VCUT - 0.06}:d=0.06[x];"
                f"[b]atrim={VCUT},asetpts=PTS-STARTPTS[y];anullsrc=r=48000:cl=mono,atrim=0:{GAP}[s];[x][s][y]concat=n=3:v=0:a=1[o]",
                "-map", "[o]", "-ac", "1", f"{ROOT}/montage/assets/voix.wav"], check=True)
tot = sum(p[1] for p in PLANS)
print(f"plans.mp4 : {tot:.2f} s, {len(PLANS)} plans (plus long : {max(p[1] for p in PLANS):.2f} s)")
