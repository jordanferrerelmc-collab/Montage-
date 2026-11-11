#!/usr/bin/env bash
# Télécharge les sons de réaction (« woaah », foule, rires…) depuis Mixkit dans effets/sfx/reactions/.
# Licence Mixkit (gratuite) : utilisation libre dans nos vidéos, mais PAS de redistribution des fichiers seuls
# → ces sons ne sont pas versionnés (dépôt public) ; relancer `npm run sfx:reactions` dans une nouvelle session.
# Réseau : mixkit.co et assets.mixkit.co doivent être autorisés (environnement « Montage »).
set -e
cd "$(dirname "$0")/.."
OUT=effets/sfx/reactions; mkdir -p "$OUT"
while read -r id name; do
  [ -z "$id" ] && continue
  [ -s "$OUT/$name.wav" ] && continue
  tmp=$(mktemp --suffix=.wav)
  curl -fsSL --retry 3 -o "$tmp" "https://assets.mixkit.co/active_storage/sfx/$id/$id.wav" \
    || curl -fsSL --retry 3 -o "$tmp" "https://assets.mixkit.co/active_storage/sfx/$id/$id-preview.mp3"
  # mono 48 kHz, 8 s max, volume homogène, petit fondu de sortie
  ffmpeg -nostdin -v error -y -i "$tmp" -t 8 -ac 1 -ar 48000 -af "silenceremove=start_periods=1:start_threshold=-45dB,loudnorm=I=-16:TP=-1.5,afade=t=out:st=7.6:d=0.4" "$OUT/$name.wav"
  rm -f "$tmp"; echo "✓ $name ($id)"
done <<'LIST'
966 surprise-homme
964 surprise-femme
967 surprise-cartoon
2010 cri-victoire-homme
2011 cri-victoire-homme-2
2012 yes-victoire-groupe
462 foule-victoire-enorme
459 foule-acclame-court
975 foule-joie
2110 foule-stade-cris
3022 foule-stade-joie
463 foule-huees
424 foule-rires
411 rire-homme
LIST
ls "$OUT" | wc -l
