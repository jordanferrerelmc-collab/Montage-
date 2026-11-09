# Installation dans le dépôt Montage

Skill tiers « claude-video-effects » (Vibha Ramprakash, licence MIT), copié depuis
github.com/Vibha-Ramprakash/claude-video-effects (commit 93140a9). Chargé automatiquement par Claude Code
dans ce projet (`.claude/skills/effects`).

Mise en route dans une nouvelle session (≈ 2 min) :

```bash
apt-get install -y libegl1 libgles2          # requis par MediaPipe dans le conteneur
cd .claude/skills/effects && uv venv -q -p 3.12 .venv && uv pip install -q -p .venv/bin/python -r requirements.txt
bash scripts/setup.sh                        # doit afficher READY
```

(`npm run effects:setup` fait tout cela.) L'erreur « ImageSegmenter.__del__ … NoneType » affichée en fin de rendu
est un message de fermeture de MediaPipe, sans conséquence.
