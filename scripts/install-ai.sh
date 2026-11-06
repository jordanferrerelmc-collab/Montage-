#!/usr/bin/env bash
# Installe les modules IA locaux utilisés par HyperFrames :
#   - Kokoro (synthèse vocale)       : paquets Python + modèle ONNX + voix (GitHub)
#   - whisper.cpp (transcription)    : compilé depuis les sources (cmake + compilateur C/C++)
#   - modèle Whisper ggml            : téléchargé depuis Hugging Face
# Idempotent : ce qui est déjà présent est conservé.
#
# Variables : WHISPER_VERSION (v1.9.5), WHISPER_MODEL (small), PREFIX (/usr/local)
set -euo pipefail

WHISPER_VERSION=${WHISPER_VERSION:-v1.9.5}
WHISPER_MODEL=${WHISPER_MODEL:-small}
PREFIX=${PREFIX:-/usr/local}
CACHE=${HYPERFRAMES_CACHE_DIR:-$HOME/.cache/hyperframes}
SUDO=""; [[ $(id -u) -ne 0 && ! -w "$PREFIX/bin" ]] && SUDO="sudo"

echo "▶ Kokoro (TTS)"
python3 -m pip install -q kokoro-onnx soundfile
K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
mkdir -p "$CACHE/tts/models" "$CACHE/tts/voices"
[[ -s "$CACHE/tts/models/kokoro-v1.0.onnx" ]] || curl -fL --retry 3 -o "$CACHE/tts/models/kokoro-v1.0.onnx" "$K/kokoro-v1.0.onnx"
[[ -s "$CACHE/tts/voices/voices-v1.0.bin" ]] || curl -fL --retry 3 -o "$CACHE/tts/voices/voices-v1.0.bin" "$K/voices-v1.0.bin"

echo "▶ whisper.cpp $WHISPER_VERSION"
if command -v whisper-cli >/dev/null; then
  echo "  déjà installé : $(command -v whisper-cli)"
else
  for tool in git cmake c++; do
    command -v "$tool" >/dev/null || { echo "✗ $tool requis pour compiler whisper.cpp"; exit 1; }
  done
  SRC=$(mktemp -d)
  trap 'rm -rf "$SRC"' EXIT
  git -c advice.detachedHead=false clone -q --depth 1 --branch "$WHISPER_VERSION" https://github.com/ggml-org/whisper.cpp.git "$SRC"
  cmake -S "$SRC" -B "$SRC/build" -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DWHISPER_BUILD_TESTS=OFF >/dev/null
  cmake --build "$SRC/build" --config Release -j"$(nproc 2>/dev/null || echo 4)" >/dev/null
  $SUDO cmake --install "$SRC/build" --prefix "$PREFIX" >/dev/null
  echo "  installé : $PREFIX/bin/whisper-cli"
fi

echo "▶ Modèle Whisper ggml-$WHISPER_MODEL"
W="$CACHE/whisper/models"
mkdir -p "$W"
if [[ ! -s "$W/ggml-$WHISPER_MODEL.bin" ]]; then
  curl -fL --retry 3 -o "$W/ggml-$WHISPER_MODEL.bin.part" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$WHISPER_MODEL.bin" \
    && mv "$W/ggml-$WHISPER_MODEL.bin.part" "$W/ggml-$WHISPER_MODEL.bin" \
    || { rm -f "$W/ggml-$WHISPER_MODEL.bin.part"; echo "✗ téléchargement impossible (huggingface.co accessible ?)"; exit 1; }
fi
echo "  $W/ggml-$WHISPER_MODEL.bin"

echo "✅ Modules IA installés."
