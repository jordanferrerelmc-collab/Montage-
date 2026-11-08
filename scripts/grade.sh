#!/usr/bin/env bash
# Applique un filtre couleur (LUT) à une vidéo, avec option grain de film et vignette.
# Usage : scripts/grade.sh entree.mp4 sortie.mp4 <look> [--grain] [--vignette] [--force 0.8]
#   looks : cinema-teal-orange, or-chaud, froid-net, punchy-gaming, film-desature, noir-et-blanc
set -euo pipefail
cd "$(dirname "$0")/.."
IN=$1; OUT=$2; LOOK=$3; shift 3
GRAIN=0; VIG=0; FORCE=1.0
while [ $# -gt 0 ]; do case $1 in --grain) GRAIN=1;; --vignette) VIG=1;; --force) FORCE=$2; shift;; esac; shift; done
LUT=effets/luts/$LOOK.cube
[ -f "$LUT" ] || { echo "Look inconnu : $LOOK ($(ls effets/luts | sed 's/.cube//' | tr '\n' ' '))"; exit 1; }
VF="split[o][g];[g]lut3d=file=$LUT[l];[o][l]blend=all_expr='A*(1-$FORCE)+B*$FORCE'"
[ $VIG = 1 ] && VF="$VF,vignette=PI/5"
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$IN"); H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$IN")
if [ $GRAIN = 1 ]; then
  [ -f effets/overlays/grain-vertical.mp4 ] || bash scripts/make-fx-assets.sh >/dev/null
  G=effets/overlays/grain-$([ "$H" -gt "$W" ] && echo vertical || echo horizontal).mp4
  ffmpeg -v error -y -i "$IN" -stream_loop -1 -i "$G" -filter_complex "[0:v]$VF[c];[1:v]scale=$W:$H,format=yuv420p[n];[c][n]blend=all_mode=overlay:all_opacity=0.12:shortest=1,format=yuv420p[v]" \
    -map "[v]" -map 0:a? -c:v libx264 -crf 18 -preset medium -c:a copy -shortest -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -i "$IN" -vf "$VF,format=yuv420p" -c:v libx264 -crf 18 -preset medium -c:a copy -movflags +faststart "$OUT"
fi
echo "✓ $OUT ($LOOK)"
