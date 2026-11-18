#!/usr/bin/env bash
# Copie la charte choisie (BRAND=specimen-agency | specimen-gaming) dans remotion/public/brand/
# pour que les compositions Remotion utilisent la même source unique que HyperFrames.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRAND="${BRAND:-specimen-agency}"
SRC="$ROOT/brand/$BRAND"
DST="$ROOT/remotion/public/brand"
[ -f "$SRC/brand.json" ] || { echo "Marque inconnue : $BRAND (dossiers : $(ls "$ROOT/brand"))" >&2; exit 1; }
rm -rf "$DST"; mkdir -p "$DST/fonts"
cp "$SRC/brand.json" "$SRC/logo.png" "$DST/"
cp "$SRC"/fonts/*.otf "$DST/fonts/"
python3 - "$DST/brand.json" "$BRAND" <<'PY'
import json, sys
p, b = sys.argv[1], sys.argv[2]
d = json.load(open(p)); d["id"] = b
json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
PY
echo "Charte $BRAND copiée dans remotion/public/brand/"
