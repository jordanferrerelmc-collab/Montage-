"""Génère la voix off (voix clonée) section par section, en chargeant le modèle une seule fois.
Usage : python gen_voice.py [ids...]   (toutes les sections par défaut)"""
import json, os, re, subprocess, sys, tempfile
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
REF = f"{REPO}/voix/voix_reference.wav"
secs = json.load(open(f"{ROOT}/scripts/sections.json"))
only = set(sys.argv[1:])
import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
for s in secs:
    if only and s["id"] not in only: continue
    parts = [p.strip() for p in re.split(r"(?<=[.!?…])\s+", s["text"]) if p.strip()]
    tmp = tempfile.mkdtemp(); files = []
    for i, p in enumerate(parts):
        seeds = s.get("seeds") or []
        torch.manual_seed(int(seeds[i] if i < len(seeds) and seeds[i] is not None else s.get("seed", 1234)))
        wav = model.generate(p, language_id="fr", audio_prompt_path=REF, exaggeration=0.7, cfg_weight=0.4)
        f = f"{tmp}/{i:02d}.wav"; torchaudio.save(f, wav, model.sr); files.append(f)
        print(s["id"], i, p, flush=True)
    sil = f"{tmp}/sil.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={model.sr}:cl=mono", "-t", "0.12", sil], check=True)
    lst = f"{tmp}/l.txt"
    with open(lst, "w") as fh:
        for i, f in enumerate(files):
            fh.write(f"file '{f}'\n" + (f"file '{sil}'\n" if i < len(files) - 1 else ""))
    out = f"{ROOT}/work/voix/{s['id']}.wav"
    # retire les silences de tête/queue, normalise
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5:LRA=7",
                    "-ar", "48000", "-ac", "1", out], check=True)
    print("OK", out, flush=True)
