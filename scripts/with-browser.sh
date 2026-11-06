#!/usr/bin/env bash
# Lance une commande en fournissant à Remotion un Chrome Headless Shell local
# quand REMOTION_BROWSER_EXECUTABLE n'est pas déjà défini. Sans binaire local,
# Remotion télécharge le sien (nécessite l'accès réseau à remotion.media).
set -euo pipefail

if [[ -z "${REMOTION_BROWSER_EXECUTABLE:-}" ]]; then
  for candidate in \
    /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell \
    "$HOME"/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell; do
    if [[ -x "$candidate" ]]; then
      export REMOTION_BROWSER_EXECUTABLE="$candidate"
      break
    fi
  done
fi

exec "$@"
