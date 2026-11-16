#!/usr/bin/env bash
# Voix claire : réduction de bruit (RNNoise, modèle « bd » de GregorR/rnnoise-models, cloné dans /opt/rnnoise-models),
# puis égalisation voix, dé-esseur, compression douce, limiteur et niveau homogène (-16 LUFS, la vidéo finale sort à -14).
# Usage : clean_voice.sh entrée(vidéo ou audio) sortie.wav
set -e
M=/opt/rnnoise-models/beguiling-drafter-2018-08-30/bd.rnnn
[ -f "$M" ] || git clone -q --depth 1 https://github.com/GregorR/rnnoise-models.git /opt/rnnoise-models
CHAIN="highpass=f=85,arnndn=m=$M:mix=0.92,equalizer=f=240:t=q:w=1.1:g=-2.5,equalizer=f=3400:t=q:w=1.2:g=3,highshelf=f=9000:g=2,deesser=i=0.35,acompressor=threshold=-21dB:ratio=3:attack=8:release=140:makeup=4dB,alimiter=limit=0.89"
# loudnorm en deux passes (mesure, puis correction linéaire)
J=$(ffmpeg -nostdin -v info -i "$1" -vn -ac 1 -ar 48000 -af "$CHAIN,loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
v() { echo "$J" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -nostdin -v error -y -i "$1" -vn -ac 1 -ar 48000 -af "$CHAIN,loudnorm=I=-16:TP=-1.5:LRA=7:measured_I=$(v input_i):measured_TP=$(v input_tp):measured_LRA=$(v input_lra):measured_thresh=$(v input_thresh):offset=$(v target_offset):linear=true" "$2"
