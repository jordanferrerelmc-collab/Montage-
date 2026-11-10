#!/bin/bash
# Découpe la capture (1920×1080) en plans verticaux 1080×1920 plein écran, calés sur la voix.
# plan : début_source durée centre_x_départ centre_x_arrivée (fraction de la largeur)
set -e
cd "$(dirname "$0")/.."
mkdir -p work/seg
i=0; list=work/seg/list.txt; : > $list
while read s d c0 c1; do
  [ -z "$s" ] && continue
  x="max(0,min(3414-1080,(${c0}+(${c1}-${c0})*t/${d})*3414-540))"
  ffmpeg -nostdin -v error -y -ss $s -t $d -i src/ecran.mov -filter_complex \
    "[0:v]fps=30,scale=3414:1920:flags=lanczos,crop=1080:1920:'$x':0,setsar=1[v];[0:a]aresample=48000[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k work/seg/s$i.mp4
  echo "file 's$i.mp4'" >> $list; i=$((i+1))
done <<PLANS
1.00 2.05 0.50 0.50
3.60 2.35 0.33 0.52
8.50 1.00 0.14 0.50
11.50 1.70 0.8383 0.8383
13.90 1.40 0.22 0.47
15.40 1.95 0.36 0.44
PLANS
ffmpeg -v error -y -f concat -safe 0 -i $list -c copy montage/assets/plans.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 montage/assets/plans.mp4
