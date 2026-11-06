#!/usr/bin/env bash
# Vérifie que toutes les dépendances système et npm sont présentes.
set -uo pipefail
cd "$(dirname "$0")/.."

fail=0
ok()  { printf '  \033[32m✓\033[0m %-22s %s\n' "$1" "$2"; }
ko()  { printf '  \033[31m✗\033[0m %-22s %s\n' "$1" "$2"; fail=1; }
opt() { printf '  \033[33m•\033[0m %-22s %s\n' "$1" "$2"; }

echo "Montage — diagnostic"

if command -v node >/dev/null; then
  major=$(node -p 'process.versions.node.split(".")[0]')
  if (( major >= 20 )); then ok "Node.js" "$(node -v)"; else ko "Node.js" "$(node -v) (>= 20 requis)"; fi
else ko "Node.js" "introuvable"; fi

command -v npm >/dev/null && ok "npm" "$(npm -v)" || ko "npm" "introuvable"

if command -v ffmpeg >/dev/null; then
  ok "FFmpeg" "$(ffmpeg -version | head -1 | awk '{print $3}')"
  encoders=$(ffmpeg -hide_banner -encoders 2>/dev/null)
  for enc in libx264 libx265 libvpx-vp9 prores_ks aac libopus; do
    grep -q " $enc " <<<"$encoders" && ok "  encodeur $enc" "disponible" || ko "  encodeur $enc" "absent"
  done
  ffmpeg -hide_banner -filters 2>/dev/null | grep -q " drawtext " \
    && ok "  filtre drawtext" "disponible" || opt "  filtre drawtext" "absent (optionnel)"
else ko "FFmpeg" "introuvable (apt install ffmpeg)"; fi

command -v ffprobe >/dev/null && ok "FFprobe" "$(ffprobe -version | head -1 | awk '{print $3}')" || ko "FFprobe" "introuvable"

if [[ -x hyperframes/node_modules/.bin/hyperframes ]]; then
  ok "HyperFrames" "$(node -p 'require("./hyperframes/node_modules/hyperframes/package.json").version')"
else ko "HyperFrames" "non installé (npm install)"; fi

if [[ -x node_modules/.bin/remotion ]]; then
  ok "Remotion" "$(node -p 'require("remotion/package.json").version')"
else ko "Remotion" "non installé (npm install)"; fi

[[ -f node_modules/gsap/package.json ]] && ok "GSAP" "$(node -p 'require("gsap/package.json").version')" || ko "GSAP" "non installé"

browser=$(bash scripts/with-browser.sh bash -c 'echo "${REMOTION_BROWSER_EXECUTABLE:-}"')
if [[ -n "$browser" ]]; then ok "Chrome (Remotion)" "$browser"
else opt "Chrome (Remotion)" "aucun binaire local — Remotion téléchargera le sien"; fi

echo
echo "Diagnostic HyperFrames :"
(cd hyperframes && npx --no-install hyperframes doctor 2>&1 | grep -E '✓|✗' | sed 's/^/  /')

echo
if (( fail )); then echo "❌ Des dépendances obligatoires manquent."; exit 1; fi
echo "✅ Toutes les dépendances obligatoires sont présentes."
