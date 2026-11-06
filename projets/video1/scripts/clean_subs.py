"""Efface les sous-titres blancs incrustés (inpainting OpenCV), image par image.
Usage : python3 clean_subs.py entree.mp4 sortie.mp4 [--preview t1,t2,...]"""
import subprocess, sys, numpy as np, cv2

W, H, FPS = 1080, 1920, 30
Y0, Y1 = 1000, 1650          # bande verticale où apparaissent les anciens sous-titres

def text_mask(band):
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    v, s = hsv[..., 2], hsv[..., 1]
    h_ = hsv[..., 0]
    white = (v > 185) & (s < 35)
    pale_yellow = (v > 200) & (s < 120) & (h_ >= 18) & (h_ <= 40)   # mots surlignés
    m = (white | pale_yellow).astype(np.uint8) * 255
    # ne garder que les lettres : composantes de hauteur homogène alignées sur une même ligne
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    comps = [(i, st[i]) for i in range(1, n)
             if 10 <= st[i][3] <= 90 and st[i][4] >= 15 and st[i][2] <= 120]
    keep = np.zeros_like(m)
    for i, (x, y, w, h, a) in comps:
        cy = y + h / 2
        mates = [j for j, (x2, y2, w2, h2, a2) in comps
                 if j != i and abs((y2 + h2 / 2) - cy) < 0.35 * h and 0.6 < h2 / h < 1.6 and abs(x2 - x) < 260]
        if len(mates) >= 2 or (len(mates) >= 1 and h >= 22) or (h >= 40 and 0.3 < w / h < 1.2 and a > 300):
            keep[lab == i] = 255
    keep = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27)))
    return keep

_prev = [None]
def clean(frame):
    band = frame[Y0:Y1]
    cur = text_mask(band)
    m = cur if _prev[0] is None else cv2.bitwise_or(cur, _prev[0])
    _prev[0] = cur
    if m.any():
        frame[Y0:Y1] = cv2.inpaint(band, m, 7, cv2.INPAINT_TELEA)
    return frame, m

def main():
    src, dst = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == "--preview":
        for t in sys.argv[4].split(","):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", src, "-frames:v", "1",
                                  "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
            f = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
            before = f.copy()
            after, m = clean(f)
            vis = np.hstack([before, after])
            cv2.imwrite(f"{dst}_{t}.jpg", cv2.resize(vis, (W, H // 2)))
        return
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS}", "-f", "rawvideo",
                            "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a",
                            "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", dst], stdin=subprocess.PIPE)
    n = 0
    while True:
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:
            break
        f, _ = clean(np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy())
        enc.stdin.write(f.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"{n} images traitées")

main()
