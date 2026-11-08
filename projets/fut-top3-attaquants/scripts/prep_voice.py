"""Prépare la voix off : pauses resserrées, débit accéléré, sections enchaînées, transcription par section.
Sorties : work/voix_off.wav, work/sections.json, work/words.json (mots horodatés sur la piste finale)."""
import json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = f"{ROOT}/work"
H = os.path.join(os.path.dirname(os.path.dirname(ROOT)), "hyperframes/node_modules/.bin/hyperframes")
IDS = ["hook", "n3", "n2", "n1", "outro"]
TEMPO = float(os.environ.get("TEMPO", "1.22"))
GAP = 0.3

def run(*a, **k): subprocess.run(list(a), check=True, **k)
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

os.makedirs(f"{W}/fast", exist_ok=True)
S, t, parts = {}, 0.0, []
for s in IDS:
    out = f"{W}/fast/{s}.wav"
    run("ffmpeg", "-v", "error", "-y", "-i", f"{W}/voix/{s}.wav", "-af",
        f"silenceremove=stop_periods=-1:stop_duration=0.22:stop_threshold=-40dB:detection=rms,atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=7",
        "-ar", "48000", "-ac", "1", out)
    d = dur(out); S[s] = [round(t, 3), round(t + d, 3)]; t += d + GAP; parts.append(out)
inputs, flt = [], []
for i, s in enumerate(IDS):
    inputs += ["-i", parts[i]]; ms = int(S[s][0] * 1000); flt.append(f"[{i}]adelay={ms}|{ms}[a{i}]")
run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
    ";".join(flt) + ";" + "".join(f"[a{i}]" for i in range(len(IDS))) + f"amix=inputs={len(IDS)}:normalize=0[o]",
    "-map", "[o]", "-ar", "48000", "-ac", "1", f"{W}/voix_off.wav")
words = []
for s in IDS:
    d = f"{W}/tr_{s}"; os.makedirs(d, exist_ok=True)
    run("ffmpeg", "-v", "error", "-y", "-i", f"{W}/fast/{s}.wav", "-ar", "16000", "-ac", "1", f"{d}/a.wav")
    if os.path.exists(f"{d}/transcript.json"): os.remove(f"{d}/transcript.json")
    subprocess.run([H, "transcribe", "a.wav", "--model", "small", "--language", "fr", "--no-runtime-install"], cwd=d, capture_output=True)
    for x in json.load(open(f"{d}/transcript.json")):
        words.append({"text": x["text"], "start": round(x["start"] + S[s][0], 3), "end": round(x["end"] + S[s][0], 3), "sec": s})
    print(s, S[s], " ".join(x["text"] for x in words if x["sec"] == s))
json.dump(S, open(f"{W}/sections.json", "w"), indent=1)
json.dump(words, open(f"{W}/words.json", "w"), ensure_ascii=False)
print("durée voix :", round(t - GAP, 2), "s")
