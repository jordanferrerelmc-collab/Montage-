#!/usr/bin/env bash
# Vérification de bout en bout : diagnostic, validation, rendus et montage.
set -euo pipefail
cd "$(dirname "$0")/.."

# Remotion signale à tort une mémoire cgroup « différente » dans les conteneurs : bruit inoffensif.
quiet_remotion() { "$@" 2> >(grep -vE 'memory amounts|Memory reported|--memory flag|lower amount of memory' >&2); }
step() { printf '\n\033[1m▶ %s\033[0m\n' "$1"; }
probe() {
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=codec_name,width,height,r_frame_rate -show_entries format=duration \
    -of default=nw=1 "$1" | tr '\n' ' '; echo
}
expect_video() {
  local f=$1
  [[ -s "$f" ]] || { echo "✗ $f absent"; exit 1; }
  local info; info=$(probe "$f")
  echo "  $f → $info"
  grep -q "width=1920" <<<"$info" && grep -q "height=1080" <<<"$info" \
    || { echo "✗ résolution inattendue pour $f"; exit 1; }
}

step "1/8 Diagnostic des dépendances"
bash scripts/doctor.sh

step "2/8 HyperFrames — lint, validation runtime, mise en page"
(cd hyperframes && npx --no-install hyperframes check)

step "3/8 HyperFrames — rendu MP4"
(cd hyperframes && npx --no-install hyperframes render -o renders/main.mp4 --quality draft --quiet >/dev/null)
expect_video hyperframes/renders/main.mp4

step "4/8 Remotion — typecheck"
npm run typecheck -w montage-remotion --silent

step "5/8 Remotion — rendu MP4 + image fixe"
quiet_remotion bash scripts/with-browser.sh npm run render -w montage-remotion --silent >/dev/null
quiet_remotion bash scripts/with-browser.sh npm run still -w montage-remotion --silent >/dev/null
expect_video remotion/out/intro.mp4
[[ -s remotion/out/intro.png ]] && echo "  remotion/out/intro.png ✓"

step "6/8 FFmpeg — montage (fondu enchaîné + audio normalisé)"
bash scripts/montage.sh
expect_video out/montage.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate -of default=nw=1 out/montage.mp4 \
  | tr '\n' ' ' | sed 's/^/  audio → /'; echo

step "7/8 Voix (Kokoro) → sous-titres (whisper.cpp)"
HF=$PWD/hyperframes/node_modules/.bin/hyperframes
if command -v whisper-cli >/dev/null && python3 -c 'import kokoro_onnx' 2>/dev/null; then
  mkdir -p out/voix
  "$HF" tts "Bonjour et bienvenue dans l'atelier de montage." --voice ff_siwis -o out/voix/voix.wav >/dev/null
  (cd out/voix && "$HF" transcribe voix.wav --model small --language fr --no-runtime-install \
     --to srt -o voix.srt >/dev/null 2>&1)
  [[ -s out/voix/voix.srt ]] || { echo "✗ transcription échouée"; exit 1; }
  echo "  out/voix/voix.wav → out/voix/voix.srt :"
  sed 's/^/    /' out/voix/voix.srt
else
  echo "  ⏭  ignoré : whisper.cpp ou Kokoro absent (npm run install:ai)"
fi

step "8/8 Charte graphique verrouillée (Specimen Agency)"
python3 scripts/check-brand.py

printf '\n\033[32m✅ Tout fonctionne : HyperFrames, Remotion et FFmpeg sont opérationnels.\033[0m\n'
