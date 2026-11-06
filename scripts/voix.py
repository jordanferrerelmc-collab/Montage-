#!/usr/bin/env python3
"""Voix off avec la voix clonée de l'utilisateur (Chatterbox Multilingual, licence MIT, local).

Usage :
  /root/.venvs/voice/bin/python scripts/voix.py "Texte à dire." -o out/voix.wav
  /root/.venvs/voice/bin/python scripts/voix.py --fichier texte.txt -o out/voix.wav [--expressivite 0.5]

La voix de référence est voix/voix_reference.wav (échantillon propre de 20 à 60 s).
Le texte est découpé en phrases, chaque phrase est générée puis assemblée avec de courtes pauses,
et le résultat est normalisé (-16 LUFS) pour le montage.
"""
import argparse, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "voix", "voix_reference.wav")

ap = argparse.ArgumentParser()
ap.add_argument("texte", nargs="?")
ap.add_argument("--fichier")
ap.add_argument("-o", "--sortie", default=os.path.join(ROOT, "out", "voix_off.wav"))
ap.add_argument("--langue", default="fr")
ap.add_argument("--expressivite", type=float, default=0.5, help="0.25 posé … 0.8 très expressif")
ap.add_argument("--pause", type=float, default=0.18, help="pause entre phrases (s)")
ap.add_argument("--reference", default=REF)
a = ap.parse_args()

text = open(a.fichier, encoding="utf-8").read() if a.fichier else a.texte
if not text:
    sys.exit("Donne un texte ou --fichier.")
if not os.path.exists(a.reference):
    sys.exit(f"Voix de référence introuvable : {a.reference}")

# phrases de longueur raisonnable (le modèle est plus stable sous ~250 caractères)
sentences = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", text.strip()) if s.strip()]
chunks = []
for s in sentences:
    while len(s) > 240:
        cut = s.rfind(",", 0, 240)
        cut = cut if cut > 60 else 240
        chunks.append(s[:cut + 1].strip()); s = s[cut + 1:].strip()
    chunks.append(s)

import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

torch.manual_seed(1234)  # rendu reproductible
model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
tmp = tempfile.mkdtemp()
parts = []
for i, c in enumerate(chunks):
    wav = model.generate(c, language_id=a.langue, audio_prompt_path=a.reference,
                         exaggeration=a.expressivite, cfg_weight=0.5)
    p = os.path.join(tmp, f"{i:03d}.wav")
    torchaudio.save(p, wav, model.sr)
    parts.append(p)
    print(f"  [{i + 1}/{len(chunks)}] {c}")

# assemblage + pauses + normalisation
lst = os.path.join(tmp, "list.txt")
sil = os.path.join(tmp, "sil.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={model.sr}:cl=mono",
                "-t", str(a.pause), sil], check=True)
with open(lst, "w") as f:
    for i, p in enumerate(parts):
        f.write(f"file '{p}'\n")
        if i < len(parts) - 1:
            f.write(f"file '{sil}'\n")
os.makedirs(os.path.dirname(os.path.abspath(a.sortie)), exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", "-ac", "1", a.sortie], check=True)
print(f"Voix off : {a.sortie}")
