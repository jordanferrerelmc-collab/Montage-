#!/usr/bin/env bash
# Coupe la source : garde les phrases utiles, retire la 2e prise (« Et écris ta ville… boutique à Saint-Denis »,
# 18,54-24,2 s, doublon de la 1re) et les blancs. Voix nettoyée (work/voix_claire.wav) en piste son. 1080×1920, 30 i/s.
set -e
cd "$(dirname "$0")/.."
SEGS="0.05:11.38 11.38:18.62 24.68:29.28 29.98:37.25"
f=""; n=0; ins=""
for s in $SEGS; do a=${s%:*}; b=${s#*:}
  f="$f[0:v]trim=$a:$b,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v$n];[1:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=$(python3 -c "print(round($b-$a-0.03,3))"):d=0.03[a$n];"
  ins="$ins[v$n][a$n]"; n=$((n+1)); done
ffmpeg -nostdin -v error -y -i src/source.mp4 -i work/voix_claire.wav -filter_complex "$f${ins}concat=n=$n:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 montage/assets/cut.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 montage/assets/cut.mp4
