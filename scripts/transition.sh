#!/usr/bin/env bash
# Enchaîne deux vidéos avec une transition FFmpeg (xfade), image ET son (fondu audio).
# Usage : scripts/transition.sh a.mp4 b.mp4 sortie.mp4 [type=fade] [durée=0.5]
# Types utiles : fade fadewhite fadeblack dissolve pixelize radial circleopen circleclose zoomin
#   slideleft slideright slideup slidedown smoothleft smoothright smoothup smoothdown wipeleft wiperight
#   wipetl wipebr hblur distance squeezeh squeezev diagtl diagbr hlslice hrslice vuslice vdslice
#   rectcrop circlecrop coverleft coverright revealleft revealright (liste complète : ffmpeg -h filter=xfade)
set -euo pipefail
A=$1; B=$2; OUT=$3; T=${4:-fade}; D=${5:-0.5}
dur() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }
OFF=$(awk -v a="$(dur "$A")" -v d="$D" 'BEGIN{printf "%.3f", a-d}')
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$A"); H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$A")
HAS_A=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$A" | head -1)
HAS_B=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$B" | head -1)
FV="[0:v]fps=30,format=yuv420p,setsar=1[a];[1:v]fps=30,scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,format=yuv420p,setsar=1[b];[a][b]xfade=transition=$T:duration=$D:offset=$OFF[v]"
if [ -n "$HAS_A" ] && [ -n "$HAS_B" ]; then
  ffmpeg -v error -y -i "$A" -i "$B" -filter_complex "$FV;[0:a][1:a]acrossfade=d=$D[au]" -map "[v]" -map "[au]" -c:v libx264 -crf 18 -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -i "$A" -i "$B" -filter_complex "$FV" -map "[v]" -c:v libx264 -crf 18 -movflags +faststart "$OUT"
fi
echo "✓ $OUT ($T, ${D}s)"
