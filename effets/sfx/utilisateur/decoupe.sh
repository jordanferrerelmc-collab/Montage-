#!/usr/bin/env bash
# Découpe la vidéo de sons envoyée par l'utilisateur le 16/11/2026 (TikTok « Effets sonores premium », @yass.views)
# en 8 effets nommés d'après l'étiquette affichée. Usage : decoupe.sh <vidéo source>
# Les fichiers ne sont pas versionnés (droits inconnus : sons d'un pack tiers) ; redéposer la vidéo dans work/source.mp4.
set -e
cd "$(dirname "$0")"
SRC="${1:-work/source.mp4}"
while read -r nom debut fin; do
  [ -z "$nom" ] && continue
  d=$(python3 -c "print(round($fin-$debut,3))")
  ffmpeg -nostdin -v error -y -ss $debut -t $d -i "$SRC" -vn -ac 1 -ar 48000 \
    -af "afade=t=in:d=0.004,afade=t=out:st=$(python3 -c "print(round($d-0.03,3))"):d=0.03,loudnorm=I=-18:TP=-2:LRA=11" "$nom.wav"
  echo "✓ $nom ($d s)"
done <<'LIST'
clavier-apple 0.00 0.53
tic-flutter 0.53 1.23
chargement-donnees 1.23 2.24
ui 2.24 2.73
montee-impact 2.73 3.40
impact-grave 3.40 4.77
clic-focus 4.77 5.17
montee-shepard 5.17 7.36
LIST
