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

step "1/6 Diagnostic des dépendances"
bash scripts/doctor.sh

step "2/6 HyperFrames — lint, validation runtime, mise en page"
(cd hyperframes && npx --no-install hyperframes check)

step "3/6 HyperFrames — rendu MP4"
(cd hyperframes && npx --no-install hyperframes render -o renders/main.mp4 --quality draft --quiet >/dev/null)
expect_video hyperframes/renders/main.mp4

step "4/6 Remotion — typecheck"
npm run typecheck -w montage-remotion --silent

step "5/6 Remotion — rendu MP4 + image fixe"
quiet_remotion bash scripts/with-browser.sh npm run render -w montage-remotion --silent >/dev/null
quiet_remotion bash scripts/with-browser.sh npm run still -w montage-remotion --silent >/dev/null
expect_video remotion/out/intro.mp4
[[ -s remotion/out/intro.png ]] && echo "  remotion/out/intro.png ✓"

step "6/6 FFmpeg — montage (fondu enchaîné + audio normalisé)"
bash scripts/montage.sh
expect_video out/montage.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate -of default=nw=1 out/montage.mp4 \
  | tr '\n' ' ' | sed 's/^/  audio → /'; echo

printf '\n\033[32m✅ Tout fonctionne : HyperFrames, Remotion et FFmpeg sont opérationnels.\033[0m\n'
