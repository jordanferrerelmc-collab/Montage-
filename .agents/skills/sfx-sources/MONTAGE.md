# Adaptation Montage

- Source : https://github.com/sxhzju/sfx (commit fb4ae3c, MIT). Copie dans `.agents/skills/sfx-sources`, lien `.claude/skills/sfx-sources`.
- Patch local (`scripts/sfx.py`, fonction `kenney`) : Kenney ne publie plus le lien .zip dans la page ; on demande le
  lien signé `https://kenney.nl/download-link/<id>` (en-tête Referer de la page du pack), comme le bouton
  « Continue without donating ».
- Sons téléchargés : `effets/sfx/sources/` (non versionné). Commande : `npm run sfx -- <commande>`.
- État au 19/11/2026 : Mixkit OK, Kenney OK, Freesound 403 (refus du site), Pixabay non autorisé (contournement Cloudflare).
