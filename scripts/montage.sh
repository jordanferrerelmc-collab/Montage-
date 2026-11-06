#!/usr/bin/env bash
# Exemple de montage FFmpeg : enchaîne le rendu HyperFrames et le rendu Remotion
# avec un fondu enchaîné, ajoute une piste audio générée, normalise le volume
# (EBU R128, -14 LUFS) et exporte un MP4 H.264/AAC prêt pour le web + une vignette.
#
# Usage : scripts/montage.sh [clipA.mp4] [clipB.mp4] [sortie.mp4]
set -euo pipefail
cd "$(dirname "$0")/.."

A=${1:-hyperframes/renders/main.mp4}
B=${2:-remotion/out/intro.mp4}
OUT=${3:-out/montage.mp4}
FADE=1   # durée du fondu enchaîné (s)

for f in "$A" "$B"; do
  [[ -f "$f" ]] || { echo "Fichier introuvable : $f (lancez d'abord les rendus)"; exit 1; }
done
mkdir -p "$(dirname "$OUT")"

dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
DA=$(dur "$A"); DB=$(dur "$B")
OFFSET=$(awk -v a="$DA" -v f="$FADE" 'BEGIN{printf "%.3f", a-f}')
TOTAL=$(awk -v a="$DA" -v b="$DB" -v f="$FADE" 'BEGIN{printf "%.3f", a+b-f}')
FADE_OUT_START=$(awk -v t="$TOTAL" 'BEGIN{printf "%.3f", t-1}')

ffmpeg -hide_banner -loglevel error -y \
  -i "$A" -i "$B" \
  -f lavfi -i "aevalsrc='0.15*sin(2*PI*220*t)+0.10*sin(2*PI*330*t)+0.08*sin(2*PI*440*t)':s=48000:d=${TOTAL}" \
  -filter_complex "\
    [0:v]fps=30,format=yuv420p,setsar=1[va]; \
    [1:v]fps=30,format=yuv420p,setsar=1[vb]; \
    [va][vb]xfade=transition=fade:duration=${FADE}:offset=${OFFSET},format=yuv420p[v]; \
    [2:a]afade=t=in:d=1,afade=t=out:st=${FADE_OUT_START}:d=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart -shortest \
  "$OUT"

ffmpeg -hide_banner -loglevel error -y -ss 2 -i "$OUT" -frames:v 1 -q:v 2 "${OUT%.*}.jpg"

echo "Montage : $OUT ($(dur "$OUT") s) — vignette : ${OUT%.*}.jpg"
