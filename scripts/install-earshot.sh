#!/usr/bin/env bash
# Installe earshot (Leonxlnx/earshot, MIT) : « des oreilles » pour juger un son (rank, find, describe, realness,
# timeline…). Programme + modèles hors du dépôt, dans /opt/earshot-src (à relancer dans une nouvelle session, ≈ 5 min).
# Les skills (.agents/skills/earshot et real-sound) sont déjà dans le dépôt ; ce script installe le moteur.
set -e
D=/opt/earshot-src; mkdir -p $D; cd $D
[ -d repo ] || git clone -q --depth 1 https://github.com/Leonxlnx/earshot.git repo
[ -x .venv/bin/python ] || uv venv -q -p 3.12 .venv
# --no-sources : le dépôt pointe PyTorch vers download.pytorch.org (bloqué ici) ; on prend la version de PyPI
uv pip install -q --no-sources -p .venv/bin/python -e "repo[mcp]"
HF_HUB_DISABLE_XET=1 .venv/bin/python -m earshot doctor --fetch   # sans Xet : cas-server.xethub.hf.co est bloqué
