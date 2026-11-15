#!/usr/bin/env python3
"""Fabrique un Reel « conseil » de 20 s (Specimen Agency, sans visage) à partir d'une fiche JSON.

  /root/.venvs/voice/bin/python projets/reels-quotidiens/scripts/make_reel.py projets/reels-quotidiens/specs/<id>.json

Étapes : voix clonée phrase par phrase (relue par transcription, régénérée si un mot est déformé) → calage des mots →
composition HyperFrames (templates/reel-conseil) → contrôles (hyperframes check + charte) → rendu → -14 LUFS →
file/<id>.mp4 (léger, publié sur Instagram) et final/<id>-hd.mp4.
Options : --sans-rendu (s'arrête après la composition), --voix-seulement.
"""
import difflib, hashlib, html, json, os, re, shutil, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = "specimen-agency"
BRAND_DIR = f"{REPO}/brand/{BRAND}"
TPL = f"{REPO}/templates/reel-conseil"
H = f"{REPO}/hyperframes/node_modules/.bin/hyperframes"
REF = f"{REPO}/voix/voix_reference.wav"
GAP = 0.14          # pause entre deux phrases (s)
LEAD = 0.15         # silence avant la première phrase
CIBLE_VOIX = 17.3   # durée maximale de la voix : au-delà, le débit est accéléré (jusqu'à 15 %)
END = 2.2           # écran de fin (logo)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = {a for a in sys.argv[1:] if a.startswith("--")}
spec = json.load(open(args[0], encoding="utf-8"))
ID = spec["id"]
plans = spec["plans"]
W = f"{ROOT}/work/{ID}"
os.makedirs(f"{W}/voix", exist_ok=True)
brand = json.load(open(f"{BRAND_DIR}/brand.json"))

def run(*a, **k): return subprocess.run(list(a), check=True, **k)
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
def norm(s):
    s = unicodedata.normalize("NFD", s.lower().replace("œ", "oe"))
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))
def mots(t): return [w for w in t.split() if norm(w)]

# ------------------------------------------------------------------ 1. voix (une phrase = un plan)
def transcrire(wav, d):
    os.makedirs(d, exist_ok=True)
    run("ffmpeg", "-v", "error", "-y", "-i", wav, "-ar", "16000", "-ac", "1", f"{d}/a.wav")
    if os.path.exists(f"{d}/transcript.json"): os.remove(f"{d}/transcript.json")
    subprocess.run([H, "transcribe", "a.wav", "--model", "small", "--language", "fr", "--no-runtime-install"], cwd=d, capture_output=True)
    return [x for x in json.load(open(f"{d}/transcript.json")) if norm(x["text"])]

def score(texte, heard):
    a, b = [norm(w) for w in mots(texte)], [norm(x["text"]) for x in heard]
    return difflib.SequenceMatcher(None, "".join(a), "".join(b), autojunk=False).ratio()

model = None
def generer(texte, seed, out):
    global model
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    import torch, torchaudio
    if model is None:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    torch.manual_seed(seed)
    wav = model.generate(texte, language_id="fr", audio_prompt_path=REF, exaggeration=0.65, cfg_weight=0.4)
    brut = out + ".brut.wav"
    torchaudio.save(brut, wav, model.sr)
    run("ffmpeg", "-v", "error", "-y", "-i", brut, "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
        "silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-40dB:detection=rms,loudnorm=I=-16:TP=-1.5:LRA=7",
        "-ar", "48000", "-ac", "1", out)
    os.remove(brut)

rapport = []
for i, p in enumerate(plans):
    key = hashlib.md5(p["voix"].encode()).hexdigest()[:8]
    wav, meta = f"{W}/voix/{i:02d}-{key}.wav", f"{W}/voix/{i:02d}-{key}.json"
    if not os.path.exists(meta):
        best = None
        for essai in range(5):
            seed = int(p.get("seed", 1234)) + 7 * essai
            tmp = f"{W}/voix/{i:02d}-essai.wav"
            generer(p["voix"], seed, tmp)
            heard = transcrire(tmp, f"{W}/tr")
            sc, d = score(p["voix"], heard), dur(tmp)
            # une phrase trop longue pour son nombre de mots = bafouillage ou bruit ajouté par le modèle
            lent = d > 0.62 * len(mots(p["voix"])) + 0.9
            print(f"  plan {i} essai {essai} (seed {seed}) : {sc:.2f} {d:.2f}s{' LENT' if lent else ''} « {' '.join(x['text'] for x in heard)} »", flush=True)
            note = sc - (0.3 if lent else 0)
            if best is None or note > best[0]:
                best = (note, seed, heard, sc, d); shutil.copy(tmp, wav)
            if sc >= 0.92 and not lent: break
        json.dump({"seed": best[1], "score": best[3], "dur": best[4], "heard": best[2]}, open(meta, "w"), ensure_ascii=False)
    m = json.load(open(meta, encoding="utf-8"))
    p["_wav"], p["_heard"], p["_score"] = wav, m["heard"], m["score"]
    rapport.append((i, m["score"], p["voix"], " ".join(x["text"] for x in m["heard"])))

brute = sum(dur(p["_wav"]) for p in plans) + GAP * (len(plans) - 1)
TEMPO = min(1.15, max(1.0, brute / CIBLE_VOIX))
t = LEAD
inputs, flt = [], []
for i, p in enumerate(plans):
    f = f"{W}/voix/{i:02d}-tempo.wav"
    run("ffmpeg", "-v", "error", "-y", "-i", p["_wav"], "-af", f"atempo={TEMPO:.4f}", "-ar", "48000", "-ac", "1", f)
    d = dur(f)
    p["t0"], p["t1"] = round(t, 3), round(t + d, 3)
    inputs += ["-i", f]; ms = int(t * 1000); flt.append(f"[{i}]adelay={ms}|{ms}[a{i}]")
    t += d + GAP
run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
    ";".join(flt) + ";" + "".join(f"[a{i}]" for i in range(len(plans))) + f"amix=inputs={len(plans)}:normalize=0[o]",
    "-map", "[o]", "-ar", "48000", "-ac", "1", f"{W}/voix_off.wav")
VOICE_END = plans[-1]["t1"]
MAIN = round(VOICE_END + 0.9, 2)
DUR = round(MAIN + END, 2)
print(f"voix : {brute:.1f} s brute, débit ×{TEMPO:.2f}, fin de voix {VOICE_END:.1f} s, durée totale {DUR} s")
faibles = [r for r in rapport if r[1] < 0.85]
for r in faibles: print(f"  ATTENTION plan {r[0]} ({r[1]:.2f}) : « {r[2]} » entendu « {r[3]} »")
if "--voix-seulement" in flags: sys.exit(0)

# ------------------------------------------------------------------ 2. mots horodatés (texte exact du script)
def caler(p):
    toks = [{"text": w} for w in mots(p["voix"])]
    heard = [{"text": x["text"], "start": p["t0"] + x["start"] / TEMPO, "end": p["t0"] + x["end"] / TEMPO} for x in p["_heard"]]
    a, b = [norm(x["text"]) for x in toks], [norm(x["text"]) for x in heard]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): toks[i1 + k]["start"], toks[i1 + k]["end"] = heard[j1 + k]["start"], heard[j1 + k]["end"]
        elif tag == "replace" and j2 > j1:
            a0, a1, n = heard[j1]["start"], heard[j2 - 1]["end"], i2 - i1
            for k in range(n): toks[i1 + k]["start"], toks[i1 + k]["end"] = a0 + (a1 - a0) * k / n, a0 + (a1 - a0) * (k + 1) / n
    # mots non entendus : répartis entre leurs voisins ; tout reste dans le plan
    for i, x in enumerate(toks):
        if "start" not in x:
            prev = toks[i - 1]["end"] if i else p["t0"]
            nxt = next((toks[k]["start"] for k in range(i + 1, len(toks)) if "start" in toks[k]), p["t1"])
            n = 1 + sum(1 for k in range(i + 1, len(toks)) if "start" not in toks[k] and all("start" not in toks[q] for q in range(i, k)))
            x["start"], x["end"] = prev, prev + (nxt - prev) / n
    for x in toks:
        x["start"] = min(max(x["start"], p["t0"]), p["t1"] - 0.05); x["end"] = min(max(x["end"], x["start"] + 0.05), p["t1"])
    return toks

for p in plans: p["mots"] = caler(p)

# ------------------------------------------------------------------ 3. composition
scenes, caps, js, audio = [], [], [], []
def sfx(name, t, vol): audio.append((name, max(0.0, t), vol))
def e(s): return html.escape(s)
GOLD, WHITE = brand["colors"]["gold"], brand["colors"]["white"]
ICON = {
    "sub": '<svg viewBox="0 0 24 24"><path d="M11 4h2v7h7v2h-7v7h-2v-7H4v-2h7z" style="fill:var(--black)"/></svg>',
    "save": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--accent)"/></svg>',
}
def taille(lignes, maxi=230, mini=96):
    n = max(len(l) for l in lignes)
    return int(max(mini, min(maxi, 900 / (0.6 * n))))

js.append(f"  tl.fromTo('#stage', {{scale: 1}}, {{scale: 1.05, duration: {MAIN:.2f}, ease: 'none'}}, 0);")
js.append(f"  tl.fromTo('#halo', {{opacity: 0.22, scale: 0.94}}, {{opacity: 0.4, scale: 1.08, duration: 2.2, ease: 'sine.inOut', yoyo: true, repeat: {int(DUR / 2.2) + 1}}}, 0);")
js.append(f"  tl.fromTo('#o1', {{rotation: 0}}, {{rotation: 40, duration: {DUR}, ease: 'none'}}, 0);")
js.append(f"  tl.fromTo('#sig', {{opacity: 0, y: -16}}, {{opacity: 1, y: 0, duration: 0.5, ease: 'power2.out'}}, 0.1);")

for i, p in enumerate(plans):
    v = p["visuel"]; kind = v["type"]
    t0 = 0.0 if i == 0 else p["t0"] - 0.08
    t1 = (plans[i + 1]["t0"] - 0.08) if i + 1 < len(plans) else MAIN
    sid, inner, anim = f"s{i}", "", []
    def at(k, n):          # instants répartis dans le plan pour les éléments qui entrent un par un
        return p["t0"] + (p["t1"] - p["t0"]) * k / max(n, 1) * 0.8
    if kind == "titre":
        lignes = v["grand"].split("|")
        if v.get("petit"): inner += f'<div class="small" id="{sid}a">{e(v["petit"])}</div>'
        inner += f'<div class="huge" id="{sid}b" style="font-size:{taille(lignes)}px">{"<br/>".join(e(l) for l in lignes)}</div>'
        if v.get("petit"): anim.append(f"  tl.fromTo('#{sid}a', {{opacity: 0, y: 24, filter: 'blur(10px)'}}, {{opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.35, ease: 'power2.out'}}, {t0 + 0.05:.2f});")
        tb = t0 + (0.22 if v.get("petit") else 0.05)
        anim.append(f"  tl.fromTo('#{sid}b', {{opacity: 0, scale: 1.18, filter: 'blur(18px)'}}, {{opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.45, ease: 'power3.out'}}, {tb:.2f});")
        anim.append(f"  tl.fromTo('#{sid}b', {{color: '{GOLD}'}}, {{color: '{WHITE}', duration: 0.6, ease: 'power1.inOut', immediateRender: false}}, {min(tb + 0.9, t1 - 0.7):.2f});")
    elif kind == "carte":
        inner = (f'<div class="card{" light" if v.get("clair") else ""}" id="{sid}a"><div class="label">{e(v["label"])}</div>'
                 f'<div class="text">{"<br/>".join(e(l) for l in v["texte"].split("|"))}</div></div>')
        anim.append(f"  tl.fromTo('#{sid}a', {{opacity: 0, y: 70, rotation: -4, scale: 0.92}}, {{opacity: 1, y: 0, rotation: 0, scale: 1, duration: 0.5, ease: 'back.out(1.5)'}}, {t0 + 0.05:.2f});")
    elif kind == "duo":
        inner = '<div class="duo">'
        for k, c in enumerate(v["cartes"]):
            inner += (f'<div class="card{" light" if c.get("clair") else ""}" id="{sid}c{k}"><div class="label">{e(c["label"])}</div>'
                      f'<div class="text">{"<br/>".join(e(l) for l in c["texte"].split("|"))}</div></div>')
            tk = t0 + 0.05 if k == 0 else at(k, len(v["cartes"]))
            anim.append(f"  tl.fromTo('#{sid}c{k}', {{opacity: 0, x: {-90 if k % 2 == 0 else 90}, rotation: {-5 if k % 2 == 0 else 5}}}, {{opacity: 1, x: 0, rotation: 0, duration: 0.45, ease: 'back.out(1.4)'}}, {tk:.2f});")
            if k: sfx("pop", tk, 0.2)
        inner += "</div>"
    elif kind == "etapes":
        inner = '<div class="steps">'
        for k, s in enumerate(v["etapes"]):
            inner += f'<div class="step" id="{sid}e{k}"><b>{k + 1}</b><span>{e(s)}</span></div>'
            tk = t0 + 0.05 if k == 0 else at(k, len(v["etapes"]))
            anim.append(f"  tl.fromTo('#{sid}e{k}', {{opacity: 0, y: 40, scale: 0.94}}, {{opacity: 1, y: 0, scale: 1, duration: 0.4, ease: 'back.out(1.6)'}}, {tk:.2f});")
            sfx("clic", tk, 0.3)
        inner += "</div>"
    elif kind == "cta":
        inner = (f'<div class="ctas"><div class="pill" id="{sid}a">{ICON["sub"]}{e(v.get("abonne", "Abonne-toi"))}</div>'
                 f'<div class="pill ghost" id="{sid}b">{ICON["save"]}{e(v.get("enregistre", "Enregistre ce Reel"))}</div></div>')
        tb = next((x["start"] for x in p["mots"] if norm(x["text"]).startswith("enregistre")), at(1, 2))
        anim.append(f"  tl.fromTo('#{sid}a', {{opacity: 0, scale: 0.7}}, {{opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)'}}, {t0 + 0.05:.2f});")
        anim.append(f"  tl.fromTo('#{sid}b', {{opacity: 0, scale: 0.7}}, {{opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)'}}, {tb - 0.05:.2f});")
        anim.append(f"  tl.to('#{sid}a', {{scale: 1.06, duration: 0.3, yoyo: true, repeat: 1, ease: 'sine.inOut'}}, {tb + 0.5:.2f});")
        sfx("pop", t0 + 0.05, 0.25); sfx("pop", tb - 0.05, 0.25)
    else:
        raise SystemExit(f"type de visuel inconnu : {kind}")
    scenes.append(f'<div class="scene clip" id="{sid}" data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" data-track-index="{2 + i % 2}">{inner}</div>')
    js += anim
    if i + 1 < len(plans):   # sortie en flou + halo doux + micro-saut du plan suivant
        js.append(f"  tl.to('#{sid}', {{opacity: 0, filter: 'blur(14px)', scale: 0.97, duration: 0.18, ease: 'power1.in'}}, {t1 - 0.18:.2f});")
        js.append(f"  tl.fromTo('#bloom', {{opacity: 0}}, {{opacity: 0.16, duration: 0.12, yoyo: true, repeat: 1, ease: 'sine.inOut', immediateRender: false}}, {t1 - 0.1:.2f});")
        sfx("whoosh-court", t1 - 0.12, 0.14)
    if i == 0: sfx("impact-sec", 0.05, 0.3)
    if p.get("fort"): sfx("ding", p["t0"], 0.18)

    # sous-titres : 1 à 3 mots, mots clés en or (pas sur le plan CTA, déjà écrit en grand)
    if kind == "cta": continue
    cles = {norm(c) for c in p.get("cles", [])}
    groups, cur = [], []
    for k, x in enumerate(p["mots"]):
        cur.append(k)
        if re.search(r"[.!?,:;…]$", x["text"]) or len(cur) >= 3 or sum(len(p["mots"][q]["text"]) for q in cur) > 12:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    # un mot de liaison seul (« ? », « : ») rejoint le groupe précédent
    for gi, g in enumerate(groups):
        st = max(0.0, p["mots"][g[0]]["start"] - 0.04)
        en = (p["mots"][groups[gi + 1][0]]["start"] - 0.04) if gi + 1 < len(groups) else min(p["t1"] + 0.1, t1)
        if en - st < 0.12: en = st + 0.12
        parts = []
        for q in g:
            w = re.sub(r"[.,:;…]+$", "", p["mots"][q]["text"])
            parts.append(f"<span class='k'>{e(w)}</span>" if norm(w) in cles else f"<span>{e(w)}</span>")
        cid = f"c{i}_{gi}"
        caps.append(f'<div class="cap clip" id="{cid}" data-start="{st:.2f}" data-duration="{en - st:.2f}" data-track-index="5">{"".join(parts)}</div>')
        js.append(f"  tl.fromTo('#{cid}', {{opacity: 0, y: 14, scale: 0.96}}, {{opacity: 1, y: 0, scale: 1, duration: 0.14, ease: 'power2.out'}}, {st:.2f});")

# écran de fin : logo + slogan (charte)
tag = brand["tagline"].replace(". ", ".<br/>", 1)
endcard = (f'<div class="clip" id="endcard" data-start="{MAIN}" data-duration="{END}" data-track-index="6">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{e(brand["name"])}"/><div id="tagline">{tag}</div></div>')
js.append(f"  tl.fromTo('#bloom', {{opacity: 0}}, {{opacity: 0.5, duration: 0.2, yoyo: true, repeat: 1, ease: 'sine.inOut', immediateRender: false}}, {MAIN - 0.2:.2f});")
js.append(f"  tl.fromTo('#endcard', {{opacity: 0}}, {{opacity: 1, duration: 0.25, ease: 'power1.out'}}, {MAIN:.2f});")
js.append(f"  tl.fromTo('#logo', {{scale: 0.82, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.6, ease: 'back.out(1.6)'}}, {MAIN + 0.05:.2f});")
js.append(f"  tl.fromTo('#tagline', {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.5, ease: 'power2.out'}}, {MAIN + 0.4:.2f});")
sfx("impact-sec", MAIN, 0.3)

OUT = f"{ROOT}/montage"
A = f"{OUT}/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{REPO}/projets/fut-4312/montage/hyperframes.json", OUT)
open(f"{OUT}/meta.json", "w").write(json.dumps({"id": "reel-conseil", "name": "reel-conseil"}))
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True); shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.rmtree(f"{A}/sfx", ignore_errors=True); shutil.copytree(f"{REPO}/effets/sfx", f"{A}/sfx", ignore=shutil.ignore_patterns("openverse", "reactions"))
shutil.copy(f"{REPO}/effets/vendor/gsap/gsap.min.js", f"{A}/gsap.min.js")
shutil.copy(f"{W}/voix_off.wav", f"{A}/voix_off.wav")

aud = [f'<audio id="voice" class="clip" src="assets/voix_off.wav" data-start="0" data-duration="{VOICE_END + 0.2:.2f}" data-volume="1" data-track-index="0"></audio>']
tracks = {}
for n, (name, ts, vol) in enumerate(audio):
    d = round(min(dur(f"{A}/sfx/{name}.wav"), DUR - ts), 2)
    tr = 8
    while any(not (ts >= e2 or ts + d <= s2) for s2, e2 in tracks.get(tr, [])): tr += 1
    tracks.setdefault(tr, []).append((ts, ts + d))
    aud.append(f'<audio id="a{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{ts:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

css = open(f"{BRAND_DIR}/brand.css").read()
page = (open(f"{TPL}/template.html").read()
        .replace("{{BRAND_CSS}}", "\n".join("      " + l for l in css.splitlines()))
        .replace("{{BRAND}}", BRAND).replace("{{DUR}}", str(DUR)).replace("{{SIGNATURE}}", brand["name"].upper())
        .replace("{{SCENES}}", "\n        ".join(scenes)).replace("{{CAPTIONS}}", "\n      ".join(caps))
        .replace("{{ENDCARD}}", endcard).replace("{{AUDIO}}", "\n    ".join(aud)).replace("{{JS}}", "\n".join(js)))
open(f"{OUT}/index.html", "w", encoding="utf-8").write(page)
json.dump({"id": ID, "dur": DUR, "main": MAIN, "tempo": TEMPO, "plans": [{"t0": p["t0"], "t1": p["t1"], "score": p["_score"]} for p in plans]},
          open(f"{W}/timing.json", "w"), indent=1)
print(f"composition : {OUT}/index.html ({DUR} s)")
if "--sans-rendu" in flags: sys.exit(0)

# ------------------------------------------------------------------ 4. contrôles, rendu, -14 LUFS, fichiers
run(H, "check", cwd=OUT)
run("python3", f"{REPO}/scripts/check-brand.py", f"{OUT}/index.html")
os.makedirs(f"{OUT}/renders", exist_ok=True)
brut = f"{OUT}/renders/{ID}.mp4"
run(H, "render", "--quality", "delivery", "-o", brut, cwd=OUT)
os.makedirs(f"{ROOT}/file", exist_ok=True); os.makedirs(f"{ROOT}/final", exist_ok=True)
AF = "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000"
run("ffmpeg", "-v", "error", "-y", "-i", brut, "-af", AF, "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{ROOT}/final/{ID}-hd.mp4")
run("ffmpeg", "-v", "error", "-y", "-i", brut, "-af", AF, "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-profile:v", "high",
    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", f"{ROOT}/file/{ID}.mp4")
json.dump({"id": ID, "titre": spec["titre"], "legende": spec["legende"], "duree": DUR,
           "script": [p["voix"] for p in plans]}, open(f"{ROOT}/file/{ID}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK {ROOT}/file/{ID}.mp4 ({os.path.getsize(f'{ROOT}/file/{ID}.mp4') / 1e6:.1f} Mo, {DUR} s)")
