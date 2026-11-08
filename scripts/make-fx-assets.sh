#!/usr/bin/env bash
# Génère la banque d'effets maison (aucun téléchargement, libre de droits) :
#   effets/sfx/       bruitages de montage (whoosh, riser, impact, glitch, shutter…)
#   effets/luts/      filtres couleur .cube (étalonnage) + scripts/grade.sh pour les appliquer
#   effets/overlays/  grain de film en boucle (à superposer en mode « overlay »)
set -euo pipefail
cd "$(dirname "$0")/.."
S=effets/sfx; L=effets/luts; O=effets/overlays
mkdir -p "$S" "$L" "$O"
f() { ffmpeg -v error -y "$@"; }

# ---------------------------------------------------------------- bruitages (48 kHz)
f -f lavfi -i "anoisesrc=d=0.6:c=pink:a=0.9" -af "highpass=f=250,lowpass=f=7000,afade=t=in:d=0.35:curve=exp,afade=t=out:st=0.35:d=0.25,volume=0.9" -ar 48000 $S/whoosh-court.wav
f -f lavfi -i "anoisesrc=d=1.1:c=pink:a=0.9" -af "bandpass=f=900:width_type=o:w=2.5,afade=t=in:d=0.7:curve=exp,afade=t=out:st=0.7:d=0.4,aecho=0.6:0.5:40:0.25,volume=1.4" -ar 48000 $S/whoosh-long.wav
f -f lavfi -i "anoisesrc=d=0.5:c=white:a=0.8" -af "highpass=f=1200,afade=t=in:d=0.05,afade=t=out:st=0.05:d=0.45:curve=exp,areverse,volume=0.8" -ar 48000 $S/swoosh-inverse.wav
f -f lavfi -i "aevalsrc='0.35*sin(2*PI*(120+900*t*t/4)*t)+0.25*(random(0)-0.5)*t/2':s=48000:d=2" -af "afade=t=in:d=1.6:curve=exp,highpass=f=80,volume=1.2" $S/riser.wav
f -f lavfi -i "aevalsrc='0.4*sin(2*PI*(900-800*t)*t)*exp(-t*1.5)+0.2*(random(0)-0.5)*exp(-t*3)':s=48000:d=1.2" -af "lowpass=f=4000,volume=1.1" $S/downlifter.wav
f -f lavfi -i "aevalsrc='0.95*sin(2*PI*(70-35*t)*t)*exp(-t*5)+0.4*(random(0)-0.5)*exp(-t*30)':s=48000:d=0.9" -af "lowpass=f=3000,alimiter=limit=0.95" $S/impact-boom.wav
f -f lavfi -i "aevalsrc='0.8*sin(2*PI*(180-120*t)*t)*exp(-t*14)+0.5*(random(0)-0.5)*exp(-t*25)':s=48000:d=0.35" -af "highpass=f=60,alimiter=limit=0.95" $S/impact-sec.wav
f -f lavfi -i "aevalsrc='0.5*(gt(sin(2*PI*90*t)\,0)*2-1)*(lt(mod(t\,0.06)\,0.03))+0.3*(random(0)-0.5)':s=48000:d=0.45" -af "acrusher=bits=4:samples=12,highpass=f=300,afade=t=out:st=0.3:d=0.15,volume=0.6" $S/glitch.wav
f -f lavfi -i "aevalsrc='0.9*(random(0)-0.5)*(exp(-t*90)+exp(-(t-0.07)*90)*gte(t\,0.07))':s=48000:d=0.2" -af "bandpass=f=3000:w=2000,volume=1.6" $S/shutter.wav
f -f lavfi -i "aevalsrc='0.9*sin(2*PI*(900-700*t/0.09)*t)*exp(-t*35)':s=48000:d=0.12" $S/pop.wav
f -f lavfi -i "aevalsrc='0.8*sin(2*PI*2200*t)*exp(-t*90)':s=48000:d=0.05" $S/clic.wav
f -f lavfi -i "aevalsrc='0.35*(sin(2*PI*1318*t)+0.6*sin(2*PI*1975*t))*exp(-t*6)':s=48000:d=0.7" $S/ding.wav
f -f lavfi -i "aevalsrc='0.4*(sin(2*PI*660*t)*lt(t\,0.09)+sin(2*PI*990*t)*gte(t\,0.09))*exp(-t*5)':s=48000:d=0.45" $S/validation.wav
f -f lavfi -i "aevalsrc='0.5*sin(2*PI*180*t)*exp(-t*10)+0.5*sin(2*PI*140*t)*exp(-t*10)':s=48000:d=0.45" $S/buzzer.wav
f -f lavfi -i "aevalsrc='0.6*(random(0)-0.5)*exp(-t*60)+0.3*sin(2*PI*1800*t)*exp(-t*80)':s=48000:d=0.08" -af "highpass=f=800" $S/frappe-clavier.wav
f -f lavfi -i "aevalsrc='0.5*sin(2*PI*(400+1600*t)*t)*exp(-t*4)':s=48000:d=0.5" -af "afade=t=out:st=0.3:d=0.2" $S/montee-ui.wav
f -f lavfi -i "anoisesrc=d=0.5:c=brown:a=1" -af "lowpass=f=2500,highpass=f=60,afade=t=out:st=0:d=0.5:curve=exp,volume=2.2,alimiter=limit=0.95" -ar 48000 $S/tir.wav
echo "✓ $(ls $S | wc -l) bruitages dans $S"

# ---------------------------------------------------------------- LUT .cube (33³)
python3 - "$L" <<'PY'
import sys, math
out = sys.argv[1]; N = 33
def clamp(x): return max(0.0, min(1.0, x))
def lum(r, g, b): return 0.2126*r + 0.7152*g + 0.0722*b
def scurve(x, k): return clamp(0.5 + (x - 0.5) * k / (1 + abs(x - 0.5) * (k - 1) * 2)) if k != 1 else x
def sat(r, g, b, s):
    y = lum(r, g, b); return tuple(clamp(y + (c - y) * s) for c in (r, g, b))
LOOKS = {
  # nom : (contraste, saturation, ombres RGB, hautes lumières RGB, description)
  "cinema-teal-orange": (1.25, 1.10, (-0.02, 0.03, 0.06), (0.06, 0.02, -0.05), "Look cinéma : ombres bleu-vert, peaux orangées"),
  "or-chaud":           (1.15, 1.05, (0.02, 0.0, -0.03), (0.07, 0.04, -0.04), "Chaud et doré (Specimen Agency)"),
  "froid-net":          (1.15, 0.95, (-0.02, 0.0, 0.05), (-0.02, 0.01, 0.04), "Froid et propre (tech, gaming)"),
  "punchy-gaming":      (1.35, 1.30, (0.0, -0.01, 0.03), (0.03, 0.0, -0.02), "Très contrasté et saturé (gaming)"),
  "film-desature":      (1.10, 0.70, (0.01, 0.01, 0.0), (0.03, 0.02, -0.01), "Film argentique doux, couleurs passées"),
  "noir-et-blanc":      (1.30, 0.0, (0, 0, 0), (0, 0, 0), "Noir et blanc contrasté"),
}
for name, (k, s, sh, hi, desc) in LOOKS.items():
    lines = [f'TITLE "{name}"', f"# {desc}", f"LUT_3D_SIZE {N}"]
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):
                r, g, b = ri/(N-1), gi/(N-1), bi/(N-1)
                y = lum(r, g, b)
                w_sh, w_hi = (1 - y) ** 2, y ** 2
                r, g, b = (clamp(c + w_sh * a + w_hi * h) for c, a, h in zip((r, g, b), sh, hi))
                r, g, b = (scurve(c, k) for c in (r, g, b))
                r, g, b = sat(r, g, b, s)
                lines.append(f"{r:.5f} {g:.5f} {b:.5f}")
    open(f"{out}/{name}.cube", "w").write("\n".join(lines) + "\n")
print(f"✓ {len(LOOKS)} LUT dans {out}")
PY

# ---------------------------------------------------------------- grain de film (boucle 2 s basse déf., agrandi à l'usage ; non versionné)
f -f lavfi -i "color=c=0x808080:s=540x960:d=2:r=30" -vf "noise=alls=30:allf=t+u,format=gray,eq=contrast=1.2" -c:v libx264 -crf 30 -pix_fmt yuv420p $O/grain-vertical.mp4
f -f lavfi -i "color=c=0x808080:s=960x540:d=2:r=30" -vf "noise=alls=30:allf=t+u,format=gray,eq=contrast=1.2" -c:v libx264 -crf 30 -pix_fmt yuv420p $O/grain-horizontal.mp4
echo "✓ grain de film dans $O"
