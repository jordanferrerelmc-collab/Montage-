#!/usr/bin/env bash
# Installe le clonage de voix local (Chatterbox Multilingual, licence MIT) dans /root/.venvs/voice
# et télécharge le modèle (≈ 3 Go au total). Nécessite l'accès à pypi.org et huggingface.co.
set -euo pipefail
V=${VOICE_VENV:-/root/.venvs/voice}
[ -x "$V/bin/python" ] || uv venv -q -p 3.11 "$V"
VIRTUAL_ENV="$V" uv pip install -q chatterbox-tts "setuptools<81"
HF_HUB_DISABLE_XET=1 "$V/bin/python" -c "from chatterbox.mtl_tts import ChatterboxMultilingualTTS as M; M.from_pretrained(device='cpu'); print('✅ Modèle de voix prêt')"
