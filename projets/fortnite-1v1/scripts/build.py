"""Vidéo « sans visage » Specimen Gaming : 3 astuces pour gagner ses 1v1 sur Fortnite.

Entrées : work/voix_off.wav (voix clonée, sections assemblées), work/words.json (mots horodatés),
work/sections.json (début/fin de chaque section). Sortie : montage/index.html (HyperFrames).
Illustrations : maquettes et schémas génériques (aucun visuel ni logo du jeu).
"""
import html, json, os, re, shutil, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
BRAND = os.environ.get("BRAND", "specimen-gaming")
BRAND_DIR = f"{REPO}/brand/{BRAND}"
brand = json.load(open(f"{BRAND_DIR}/brand.json"))
heard = json.load(open(f"{ROOT}/work/words.json"))      # mots horodatés (transcription, parfois fautive)
S = json.load(open(f"{ROOT}/work/sections.json"))       # {id: [start, end]}
script = json.load(open(f"{ROOT}/scripts/sections.json"))
VOICE_END = S["outro"][1]
END_LEN = 2.4
DUR = round(VOICE_END + 0.35 + END_LEN, 2)

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9']", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))

def align():
    """Texte exact du script, horodaté grâce à la transcription (alignement mot à mot)."""
    import difflib
    toks = []
    for s in script:
        for w in s["text"].split():
            toks.append({"text": w, "sec": s["id"]})
    a = [norm(t["text"]) for t in toks]
    b = [norm(h["text"]) for h in heard]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                toks[i1 + k]["start"], toks[i1 + k]["end"] = heard[j1 + k]["start"], heard[j1 + k]["end"]
        elif tag == "replace" and j2 > j1:   # répartit l'intervalle entendu sur les mots du script
            t0, t1 = heard[j1]["start"], heard[j2 - 1]["end"]
            n = i2 - i1
            for k in range(n):
                toks[i1 + k]["start"] = t0 + (t1 - t0) * k / n
                toks[i1 + k]["end"] = t0 + (t1 - t0) * (k + 1) / n
    # mots non retrouvés : interpolation entre voisins, bornée par la section
    for i, t in enumerate(toks):
        if "start" not in t:
            prev = next((toks[k]["end"] for k in range(i - 1, -1, -1) if "end" in toks[k]), S[t["sec"]][0])
            nxt = next((toks[k]["start"] for k in range(i + 1, len(toks)) if "start" in toks[k]), S[t["sec"]][1])
            t["start"], t["end"] = prev, max(prev + 0.05, min(nxt, prev + 0.3))
    # « un contre un » s'affiche « 1v1 »
    out, i = [], 0
    while i < len(toks):
        if [norm(x["text"]) for x in toks[i:i + 3]] == ["un", "contre", "un"]:
            out.append({**toks[i], "text": "1v1", "end": toks[i + 2]["end"]}); i += 3
        else:
            out.append(toks[i]); i += 1
    return out

words = align()

def T(word, after=0.0, default=None):
    """Début du premier mot commençant par `word` après `after` (s)."""
    w = norm(word)
    for x in words:
        n = norm(x["text"])
        if x["start"] >= after - 0.05 and (n.startswith(w) or n.split("'")[-1].startswith(w)):
            return x["start"]
    if default is None:
        raise SystemExit(f"mot introuvable : {word} après {after}")
    return default

js, scenes, audio = [], [], []
def sfx(name, t, vol=0.4, dur=0.5):
    audio.append((name, t, vol, dur))

# ------------------------------------------------------------------ fond animé
js.append(f'  tl.fromTo("#grid", {{y: 0}}, {{y: 600, duration: {DUR}, ease: "none"}}, 0);')
js.append(f'  tl.fromTo("#glow", {{scale: 0.9, opacity: 0.25}}, {{scale: 1.15, opacity: 0.4, duration: {DUR / 2:.2f}, yoyo: true, repeat: 1, ease: "sine.inOut"}}, 0);')
js.append(f'  tl.fromTo("#progress", {{scaleX: 0}}, {{scaleX: 1, duration: {VOICE_END:.2f}, ease: "none"}}, 0);')
streaks = []
for k, (y, w, d, delay) in enumerate([(180, 260, 1.6, 0.0), (520, 180, 1.3, 0.7), (900, 320, 1.9, 0.3),
                                      (1300, 220, 1.5, 1.1), (1650, 280, 1.7, 0.5), (760, 140, 1.2, 1.4)]):
    streaks.append(f'<div class="streak" id="sk{k}" style="top:{y}px; width:{w}px; left:-{w}px"></div>')
    reps = int((DUR - delay) / d)
    js.append(f'  tl.fromTo("#sk{k}", {{x: 0}}, {{x: {1080 + w}, duration: {d}, ease: "none", repeat: {reps}}}, {delay});')

# ------------------------------------------------------------------ scènes
def scene(sid, start, end, inner, big=False):
    scenes.append(f'<div class="scene clip" id="{sid}" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="2">{inner}</div>')
    if start > 0.05:
        js.append(f'  tl.fromTo("#flash", {{opacity: {0.9 if big else 0.7}}}, {{opacity: 0, duration: 0.2, ease: "power2.out", immediateRender: false}}, {start:.3f});')
        js.append(f'  tl.fromTo("#stage", {{scale: {1.16 if big else 1.1}, rotation: {-1.5 if len(scenes) % 2 else 1.5}}}, {{scale: 1, rotation: 0, duration: 0.32, ease: "expo.out", immediateRender: false}}, {start:.3f});')
        sfx("whoosh", start - 0.15, 0.35 if big else 0.25, 0.45)
        if big:
            js.append(f'  tl.fromTo("#accentflash", {{opacity: 0.5}}, {{opacity: 0, duration: 0.35, immediateRender: false}}, {start:.3f});')
            sfx("impact", start, 0.4, 0.45)

def pop(sel, t, **kw):
    fr = kw.get("fr", "scale: 0.3, opacity: 0")
    js.append(f'  tl.from("{sel}", {{{fr}, duration: {kw.get("d", 0.3)}, ease: "{kw.get("ease", "back.out(2.2)")}"}}, {t:.3f});')
    if kw.get("snd", True):
        sfx(kw.get("name", "pop"), t, kw.get("vol", 0.3), 0.15)

def badge(n, title):
    return (f'<div class="center" style="top:420px; display:flex; flex-direction:column; align-items:center; gap:46px">'
            f'<div class="num-badge" style="width:240px; height:240px; font-size:170px">{n}</div>'
            f'<div class="h1 stroke" style="font-size:104px; width:1000px">{title}</div></div>')

PLAYER = lambda col, sid: (f'<svg id="{sid}" viewBox="0 0 100 140" style="width:200px"><circle cx="50" cy="32" r="26" style="fill:{col}"/>'
                           f'<path d="M12 140 Q12 70 50 70 Q88 70 88 140 Z" style="fill:{col}"/></svg>')

h0, h1 = S["hook"]
t_visee = T("visee", h0)
t_voici = T("voici", h0)
t_3e = T("troisieme", t_voici)
scene("s-hook1", h0, t_voici - 0.05,
      '<div class="center" style="top:330px; display:flex; align-items:center; gap:40px">'
      + PLAYER("var(--ink)", "p-me") + '<div class="h1 acc stroke" id="vs" style="font-size:150px">1V1</div>' + PLAYER("var(--red)", "p-foe") + '</div>'
      '<div class="center" id="reticle" style="top:700px; display:flex; align-items:center; gap:30px">'
      '<svg viewBox="0 0 100 100" style="width:190px"><circle cx="50" cy="50" r="34" fill="none" style="stroke:var(--ink)" stroke-width="6"/>'
      '<path d="M50 4v24M50 72v24M4 50h24M72 50h24" style="stroke:var(--ink)" stroke-width="6"/>'
      '<path id="slash" d="M14 86L86 14" style="stroke:var(--red)" stroke-width="10" stroke-linecap="round"/></svg>'
      '<div class="h2 stroke" style="text-align:left">PAS TA<br/><span class="acc">VISÉE ?</span></div></div>')
pop("#p-me", h0, fr="x: -500, opacity: 0", ease="expo.out", d=0.35, name="whoosh", vol=0.3)
pop("#p-foe", h0 + 0.1, fr="x: 500, opacity: 0", ease="expo.out", d=0.35, snd=False)
pop("#vs", h0 + 0.35, fr="scale: 3, opacity: 0", ease="power4.in", d=0.2, name="impact", vol=0.4)
pop("#reticle", t_visee - 0.1, fr="scale: 0.4, opacity: 0, rotation: -90")
pop("#slash", T("probleme", t_visee) - 0.05, fr="scale: 0, transformOrigin: '50% 50%'", ease="back.out(3)", name="buzz", vol=0.3)

tiles = "".join(f'<div class="panel" id="tile{i}" style="width:250px; height:250px; justify-content:center; padding:0">'
                f'<div class="h1" style="font-size:150px">{i}</div></div>' for i in (1, 2, 3))
scene("s-hook2", t_voici - 0.05, h1 + 0.1,
      '<div class="center" style="top:300px"><div class="h1 stroke" id="h3a"><span class="acc">3</span> ASTUCES</div></div>'
      f'<div class="center" style="top:600px; display:flex; gap:40px">{tiles}</div>'
      '<div class="center" id="forgot" style="top:800px; white-space:nowrap"><span class="tag">La plus oubliée</span></div>')
pop("#h3a", t_voici, fr="y: -120, opacity: 0", ease="back.out(1.8)")
for i in (1, 2, 3):
    pop(f"#tile{i}", T("astuces", t_voici) + 0.12 * (i - 1), fr="y: 200, opacity: 0, rotation: 12")
js.append(f'  tl.to("#tile3", {{scale: 1.18, rotation: -4, duration: 0.25, ease: "back.out(3)"}}, {t_3e:.3f});')
js.append(f'  tl.to("#tile3", {{scale: 1.1, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut"}}, {t_3e + 0.3:.3f});')
pop("#forgot", T("oublient", t_3e) - 0.1, fr="scale: 2, opacity: 0", ease="power3.in", name="impact", vol=0.3)

# ---- conseil 1
c0, c1e = S["c1"]
t_va = T("va", c0); t_audio = T("audio", t_va); t_active = T("active", t_audio); t_pourras = T("pourras", t_active)
t_pas = T("pas", t_pourras); t_antic = T("anticiper", t_pas)
scene("s-c1a", c0, t_va - 0.05, badge(1, 'VISUALISATION<br/><span class="acc">DES BRUITAGES</span>'), big=True)
pop("#s-c1a .num-badge", c0 + 0.05, fr="scale: 0, rotation: -40", ease="back.out(2.5)")
tabs = "".join(f'<div class="tab" id="tab-{n}" style="padding:16px 26px; font-weight:700; font-size:38px; letter-spacing:0.06em; '
               f'color:var(--silver); border-bottom:6px solid transparent">{n}</div>' for n in ("VIDÉO", "AUDIO", "JEU", "COMMANDES"))
scene("s-c1b", t_va - 0.05, t_pourras - 0.05,
      '<div class="center" id="crumb" style="top:40px; white-space:nowrap"><span class="tag" style="font-size:36px">Paramètres › Audio › Bruitages</span></div>')
pop("#crumb", t_va - 0.05, fr="y: -80, opacity: 0", ease="back.out(2)", snd=False)
sfx("click", t_audio, 0.5, 0.1)
sfx("click", t_active, 0.5, 0.1); sfx("check", t_active + 0.05, 0.3, 0.4)

STEP = '<svg viewBox="0 0 40 60" style="width:56px"><ellipse cx="20" cy="20" rx="14" ry="18" style="fill:var(--ink)"/><ellipse cx="20" cy="49" rx="10" ry="10" style="fill:var(--ink)"/></svg>'
scene("s-c1c", t_pourras - 0.05, c1e + 0.1,
      '<div style="position:absolute; left:660px; top:0px; transform:scale(0.52); transform-origin:0 0"><div id="radar" style="position:relative; width:720px; height:720px; border-radius:50%; background:var(--panel); border:6px solid var(--red)">'
      '<svg viewBox="0 0 200 200" style="position:absolute; inset:0; width:720px">'
      '<circle cx="100" cy="100" r="92" fill="none" style="stroke:var(--silver)" stroke-width="2" opacity="0.5"/>'
      '<circle cx="100" cy="100" r="60" fill="none" style="stroke:var(--silver)" stroke-width="2" opacity="0.35"/>'
      '<path id="arc" d="M100 8 A92 92 0 0 1 179 53" fill="none" style="stroke:var(--red)" stroke-width="12" stroke-linecap="round"/>'
      '<circle cx="100" cy="100" r="9" style="fill:var(--ink)"/></svg>'
      f'<div id="st1" style="position:absolute; left:470px; top:120px; transform:rotate(30deg)">{STEP}</div>'
      f'<div id="st2" style="position:absolute; left:540px; top:200px; transform:rotate(40deg)">{STEP}</div>'
      f'<div id="st3" style="position:absolute; left:595px; top:290px; transform:rotate(55deg)">{STEP}</div></div></div>'
      '<div class="center" id="antic" style="top:820px; white-space:nowrap"><span class="tag" style="font-size:46px">Anticipe l\'ennemi</span></div>')
pop("#radar", t_pourras - 0.05, fr="scale: 0.5, opacity: 0", ease="expo.out", d=0.4, snd=False)
for k in (1, 2, 3):
    tt = t_pas + 0.22 * (k - 1)
    pop(f"#st{k}", tt, fr="scale: 0, opacity: 0", ease="back.out(3)", name="step", vol=0.5)
js.append(f'  tl.fromTo("#arc", {{opacity: 0.2}}, {{opacity: 1, duration: 0.18, yoyo: true, repeat: 5, immediateRender: false}}, {t_pas:.3f});')
pop("#antic", t_antic - 0.05, fr="y: 80, opacity: 0", ease="back.out(2)")

# ---- conseil 2
c2s, c2e = S["c2"]
t_sur = T("sur", c2s); t_droite = T("droite", t_sur); t_alors = T("alors", t_droite)
t_sortir = T("sortir", t_alors); t_tirer = T("tirer", t_sortir); t_couvert = T("couvert", t_tirer); t_evite = T("evite", t_couvert)
scene("s-c2a", c2s, t_sur - 0.05, badge(2, 'UTILISE<br/><span class="acc">LES ANGLES</span>'), big=True)
pop("#s-c2a .num-badge", c2s + 0.05, fr="scale: 0, rotation: -40", ease="back.out(2.5)")
scene("s-c2b", t_sur - 0.05, t_alors - 0.05,
      '<div class="panel" style="position:absolute; left:560px; top:0px; width:480px; padding:16px"><div style="width:760px; transform:scale(0.58); transform-origin:0 0; height:370px">'
      '<svg viewBox="0 0 200 160" style="width:760px">'
      '<path id="cone" d="M118 112 L60 10 L196 10 Z" style="fill:var(--red)" opacity="0.28"/>'
      '<path d="M118 112 L60 10 M118 112 L196 10" style="stroke:var(--red)" stroke-width="2" stroke-dasharray="5 4"/>'
      '<circle cx="100" cy="120" r="14" style="fill:var(--ink)"/>'
      '<g id="cam"><rect x="108" y="132" width="26" height="18" rx="3" style="fill:var(--red)"/><path d="M134 136 l10 -5 v20 l-10 -5z" style="fill:var(--red)"/></g>'
      '<path d="M100 120 L121 141" style="stroke:var(--silver)" stroke-width="2" stroke-dasharray="3 3"/></svg></div></div>'
      '<div class="center" style="top:770px; width:1000px"><div class="h2 stroke" style="font-size:62px">CAMÉRA DÉCALÉE <span class="acc">À DROITE →</span></div></div>')
pop("#s-c2b svg", t_sur - 0.05, fr="scale: 0.6, opacity: 0", ease="expo.out", d=0.4, snd=False)
pop("#cam", T("camera", t_sur) - 0.05, fr="x: -60, opacity: 0", ease="back.out(2)")
js.append(f'  tl.from("#cone", {{opacity: 0, duration: 0.3}}, {t_droite - 0.1:.3f});')

labels = "".join(f'<span class="tag" id="lb{i}" style="background:var(--dark); font-size:40px">{t}</span>'
                 for i, t in enumerate(["SORS", "TIRE", "COUVRE-TOI"]))
scene("s-c2c", t_alors - 0.05, t_evite - 0.05,
      f'<div class="center" style="top:60px; display:flex; gap:22px">{labels}</div>')
js.append(f'  tl.to("#lb0", {{backgroundColor: "var(--red)", duration: 0.1}}, {t_sortir:.3f});')
js.append(f'  tl.to("#lb1", {{backgroundColor: "var(--red)", duration: 0.1}}, {t_tirer:.3f});')
sfx("shot", t_tirer, 0.5, 0.5)
js.append(f'  tl.to("#lb2", {{backgroundColor: "var(--red)", duration: 0.1}}, {t_couvert - 0.1:.3f});')

scene("s-c2d", t_evite - 0.05, c2e + 0.1,
      '<div class="center" style="top:300px; width:820px; height:420px">'
      '<svg viewBox="0 0 200 100" style="width:820px">'
      '<circle cx="24" cy="50" r="12" style="fill:var(--ink)"/><circle cx="176" cy="50" r="12" style="fill:var(--red)"/>'
      '<path d="M44 50 H150 M136 38 L152 50 L136 62" fill="none" style="stroke:var(--ink)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
      '<path id="bigx" d="M80 18 L120 82 M120 18 L80 82" style="stroke:var(--red)" stroke-width="12" stroke-linecap="round"/></svg></div>'
      '<div class="center" style="top:640px; width:1000px"><div class="h1 stroke" style="font-size:110px">NE FONCE <span class="acc">PAS !</span></div></div>')
pop("#s-c2d svg", t_evite - 0.05, fr="x: -300, opacity: 0", ease="expo.out", d=0.3, snd=False)
pop("#bigx", T("foncer", t_evite) - 0.05, fr="scale: 3, opacity: 0, transformOrigin: '50% 50%'", ease="power4.in", d=0.2, name="buzz", vol=0.35)

# ---- conseil 3
c3s, c3e = S["c3"]
t_mets = T("mets", c3s); t_pompe = T("pompe", t_mets); t_protege = T("protege", t_pompe); t_change = T("change", t_protege)
t_attaque = T("attaque", t_change); t_bon = T("bon", t_attaque); t_prendre = T("prendre", t_bon)
scene("s-c3a", c3s, t_mets - 0.05, badge(3, 'NE FORCE PAS<br/><span class="acc">LE KILL</span>'), big=True)
pop("#s-c3a .num-badge", c3s + 0.05, fr="scale: 0, rotation: -40", ease="back.out(2.5)")
steps = ["GROS TIR<br/>AU POMPE", "PROTÈGE-<br/>TOI", "CHANGE<br/>D'ANGLE", "ATTAQUE<br/>À NOUVEAU"]
grid = "".join(f'<div class="panel" id="cy{i}" style="width:240px; height:170px; justify-content:center; padding:10px; box-shadow:none">'
               f'<div style="font-weight:700; font-size:22px; color:var(--ink); letter-spacing:0.1em">ÉTAPE {i + 1}</div>'
               f'<div class="h2" style="font-size:34px">{s}</div></div>' for i, s in enumerate(steps))
scene("s-c3b", t_mets - 0.05, t_bon - 0.05,
      f'<div class="center" style="top:110px; display:flex; gap:16px">{grid}</div>')
for i, t in enumerate([t_mets, t_protege, t_change, t_attaque]):
    pop(f"#cy{i}", t - 0.08, fr="scale: 0.5, opacity: 0", ease="back.out(2)")
    js.append(f'  tl.to("#cy{i}", {{backgroundColor: "var(--red)", borderColor: "var(--ink)", duration: 0.12}}, {t - 0.02 if i else t_pompe:.3f});')
sfx("shot", t_pompe, 0.55, 0.5)

bar = lambda bid, label, col: (f'<div style="display:flex; flex-direction:column; gap:14px; width:860px">'
                               f'<div style="font-weight:700; font-size:40px; letter-spacing:0.08em">{label}</div>'
                               f'<div style="height:64px; background:var(--dark); border:4px solid var(--silver); border-radius:10px; overflow:hidden">'
                               f'<div id="{bid}" style="height:100%; width:100%; background:{col}; transform-origin:0 50%"></div></div></div>')
scene("s-c3c", t_bon - 0.05, c3e + 0.1,
      '<div class="center" style="top:430px; display:flex; flex-direction:column; gap:50px">'
      + bar("hp-foe", "ADVERSAIRE", "var(--red)") + bar("hp-me", "TOI", "var(--ink)") + '</div>'
      '<div class="center" id="nodmg" style="top:720px; white-space:nowrap"><span class="tag" style="font-size:36px">Dégâts reçus : 0</span></div>')
pop("#s-c3c .center", t_bon - 0.05, fr="y: 200, opacity: 0", ease="expo.out", d=0.4, snd=False)
js.append(f'  tl.to("#hp-foe", {{scaleX: 0.35, duration: 0.5, ease: "power3.out"}}, {T("degats", t_bon):.3f});')
sfx("impact", T("degats", t_bon), 0.35, 0.45)
js.append(f'  tl.fromTo("#hp-me", {{scaleX: 1}}, {{scaleX: 1.0, duration: 0.01, immediateRender: false}}, {t_bon:.3f});')
pop("#nodmg", t_prendre - 0.15, fr="scale: 2, opacity: 0", ease="power3.in", name="check", vol=0.35)

# ---- outro
o0, o1 = S["outro"]
t_dis = T("dis", o0); t_constr = T("construction", t_dis); t_zero = T("zero", t_constr); t_abonne = T("abonne", t_zero)
items = ["Bruitages visuels", "Joue l'angle droit", "Ne force pas le kill"]
check = '<svg viewBox="0 0 40 40" style="width:70px"><rect x="2" y="2" width="36" height="36" rx="6" style="fill:var(--red)"/><path d="M10 21l7 7 14-15" fill="none" style="stroke:var(--ink)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
lst = "".join(f'<div id="ck{i}" style="display:flex; align-items:center; gap:30px; font-weight:700; font-size:58px; text-transform:uppercase">{check}{t}</div>'
              for i, t in enumerate(items))
scene("s-o1", o0, t_dis - 0.05,
      f'<div class="center panel" style="top:470px; width:900px; align-items:flex-start; gap:36px; padding:50px">{lst}</div>', big=True)
for i in range(3):
    pop(f"#ck{i}", o0 + 0.2 + 0.35 * i, fr="x: -200, opacity: 0", ease="back.out(2)", name="check", vol=0.3)
opt = lambda oid, t: (f'<div class="panel" id="{oid}" style="width:440px; height:230px; justify-content:center; padding:20px">'
                      f'<div class="h2" style="font-size:50px">{t}</div></div>')
scene("s-o2", t_dis - 0.05, t_abonne - 0.05,
      '<div class="center" style="top:300px"><div class="h2 stroke" style="font-size:84px">TU JOUES EN…</div></div>'
      f'<div class="center" style="top:560px; display:flex; gap:40px">{opt("op1", "CONSTRUC-<br/>TION")}{opt("op2", "ZÉRO<br/>CONSTRUCTION")}</div>'
      '<div class="center" id="cmt" style="top:790px; white-space:nowrap"><span class="tag" style="font-size:40px">Réponds en commentaire ↓</span></div>')
pop("#s-o2 .h2", t_dis - 0.05, fr="y: -100, opacity: 0", ease="back.out(2)", snd=False)
pop("#op1", t_constr - 0.1, fr="x: -400, opacity: 0", ease="expo.out")
pop("#op2", t_zero - 0.1, fr="x: 400, opacity: 0", ease="expo.out")
pop("#cmt", t_zero + 0.6, fr="y: 60, opacity: 0", ease="back.out(2)")
scene("s-o3", t_abonne - 0.05, VOICE_END + 0.35,
      '<div class="center" style="top:470px; display:flex; flex-direction:column; align-items:center; gap:50px">'
      '<div class="cta" id="sub" style="font-size:76px; padding:40px 80px; white-space:nowrap">+ ABONNE-TOI</div>'
      '<div class="h2" style="font-size:64px; letter-spacing:0.04em">SPECIMEN <span class="acc">GAMING</span></div></div>', big=True)
pop("#sub", t_abonne, fr="scale: 0.3, opacity: 0", ease="back.out(2.5)")
js.append(f'  tl.to("#sub", {{scale: 0.92, duration: 0.1, yoyo: true, repeat: 1}}, {t_abonne + 0.9:.3f});')
sfx("click", t_abonne + 0.9, 0.5, 0.1)

# ------------------------------------------------------------------ sous-titres (mots, style dynamique)
KEY = {"1", "un", "fortnite", "visee", "3", "trois", "troisieme", "bruitages", "pas", "anticiper", "angles", "droite", "mur",
       "couvert", "foncer", "pompe", "protege", "angle", "degats", "prendre", "commentaire", "construction", "abonnetoi", "abonne", "specimen", "gaming"}
KEY -= {"pas", "un"}
fixes = {"1": "1V1"}
groups, cur = [], []
for i, x in enumerate(words):
    cur.append(i)
    end_punct = re.search(r"[.!?,:]$", x["text"])
    nxt_gap = (words[i + 1]["start"] - x["end"]) if i + 1 < len(words) else 9
    if end_punct or len(cur) >= 3 or nxt_gap > 0.35 or sum(len(words[k]["text"]) for k in cur) > 16:
        groups.append(cur); cur = []
if cur: groups.append(cur)
caps = []
for gi, g in enumerate(groups):
    st = max(0.0, words[g[0]]["start"] - 0.04)
    en = (words[groups[gi + 1][0]]["start"] - 0.04) if gi + 1 < len(groups) else VOICE_END + 0.3
    spans = []
    for k in g:
        t = re.sub(r"[.,!?:;]+$", "", words[k]["text"]).upper()
        cls = "w hl" if norm(words[k]["text"]) in KEY else "w"
        spans.append(f'<span class="{cls}" id="w{k}">{html.escape(t)}</span>')
    caps.append(f'<div class="cap clip" id="g{gi}" data-start="{st:.3f}" data-duration="{en - st:.3f}" data-track-index="4">{" ".join(spans)}</div>')
    js.append(f'  tl.from("#g{gi}", {{scale: 0.7, y: 24, duration: 0.16, ease: "back.out(2.5)"}}, {st:.3f});')
    for k in g:
        js.append(f'  tl.fromTo("#w{k}", {{y: -14}}, {{y: 0, duration: 0.18, ease: "back.out(3)"}}, {max(st, words[k]["start"] - 0.03):.3f});')

# ------------------------------------------------------------------ écran de fin
endcard = (f'<div class="clip" id="endcard" data-start="{VOICE_END + 0.35:.3f}" data-duration="{END_LEN:.2f}" data-track-index="5">'
           f'<img id="logo" src="assets/brand/logo.png" alt="{html.escape(brand["name"])}"/></div>')
js.append(f'  tl.fromTo("#flash", {{opacity: 0.9}}, {{opacity: 0, duration: 0.3, immediateRender: false}}, {VOICE_END + 0.35:.3f});')
js.append(f'  tl.from("#logo", {{scale: 0.6, opacity: 0, duration: 0.5, ease: "back.out(1.8)"}}, {VOICE_END + 0.4:.3f});')
sfx("impact", VOICE_END + 0.35, 0.45, 0.45)

# ------------------------------------------------------------------ images du jeu (captures de l'utilisateur)
# (début, fin, clip, entrée source, sortie source, mode, voile sombre)
# mode « full » : plein écran vertical recadré sur le personnage ; « card » : capture entière en carte sur fond flouté
SRC = f"{ROOT}/src"
BROLL = [   # un clip par partie, lu en continu (choix de l'utilisateur)
    (h0, c0, "clip2.mp4", 0.0, 5.85, "full", 0.0),
    (c0, c2s, "clip1.mp4", 0.0, 8.85, "menu", 0.0),
    (c2s, c3s, "clip3.mov", 0.0, 10.45, "full", 0.0),
    (c3s, c3e + 0.1, "clip4.mov", 0.0, 9.4, "full", 0.0),
]
# voile sombre scène par scène (lisibilité des textes), 0 = images du jeu pleinement visibles
DIM = [(h0, 0.45), (t_voici - 0.05, 0.55), (c0, 0.6), (t_va - 0.05, 0.0), (t_pourras - 0.05, 0.3),
       (c2s, 0.6), (t_sur - 0.05, 0.25), (t_alors - 0.05, 0.08), (t_evite - 0.05, 0.45),
       (c3s, 0.6), (t_mets - 0.05, 0.08), (t_bon - 0.05, 0.5), (c3e + 0.1, 0.0)]
FOCUS = {"clip2.mp4": 0.42, "clip3.mov": 0.44, "clip4.mov": 0.44}  # position horizontale du personnage

def build_broll():
    import hashlib, subprocess, tempfile
    key = hashlib.md5(json.dumps([[round(x, 3) if isinstance(x, float) else x for x in b] for b in BROLL]).encode()).hexdigest()[:10]
    out = f"{ROOT}/work/broll_{key}.mp4"
    if os.path.exists(out):
        return out
    tmp = tempfile.mkdtemp(dir=f"{ROOT}/work")
    parts = []
    for n, (a, b, clip, si, so, mode, _) in enumerate(BROLL):
        need = b - a
        speed = (so - si) / need                       # > 1 : accéléré, < 1 : ralenti
        speed = min(max(speed, 0.55), 1.8)
        used = need * speed
        if mode == "menu":
            vf = (f"split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.25[bg];"
                  f"[b]crop=1180:760:0:120,scale=1040:-2,pad=iw+12:ih+12:6:6:color=0xda3d39[fg];[bg][fg]overlay=(W-w)/2:330")
        else:
            fx = FOCUS.get(clip, 0.45)
            vf = f"scale=-2:1920,crop=1080:1920:'max(0,min(iw-1080,iw*{fx}-540))':0"
        f = f"{tmp}/{n:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{si}", "-t", f"{used:.3f}", "-i", f"{SRC}/{clip}",
                        "-filter_complex", f"[0:v]setpts=PTS/{speed:.4f},fps=30,{vf},format=yuv420p,tpad=stop_mode=clone:stop_duration=2[v]",
                        "-map", "[v]", "-t", f"{need:.3f}", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast", f], check=True)
        parts.append(f)
    with open(f"{tmp}/list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-r", "30", "-an", out], check=True)
    return out

broll_file = build_broll()
BROLL_LEN = BROLL[-1][1]
for (a, dim) in DIM:
    js.append(f'  tl.set("#dim", {{opacity: {dim}}}, {max(0, a):.3f});')

# ------------------------------------------------------------------ audio
aud = [f'<audio id="voice" class="clip" src="assets/voix_off.wav" data-start="0" data-duration="{VOICE_END + 0.2:.3f}" data-volume="1" data-track-index="0"></audio>']
tracks = {}
for n, (name, t, vol, d) in enumerate(audio):
    t = max(0.0, t)
    tr = 6
    while any(not (t >= e or t + d <= s0) for s0, e in tracks.get(tr, [])):
        tr += 1
    tracks.setdefault(tr, []).append((t, t + d))
    aud.append(f'<audio id="sfx{n}" class="clip" src="assets/sfx/{name}.wav" data-start="{t:.3f}" data-duration="{d}" data-volume="{vol}" data-track-index="{tr}"></audio>')

tpl = open(f"{REPO}/templates/reel-faceless/template.html").read()
brand_css = open(f"{BRAND_DIR}/brand.css").read()
A = f"{ROOT}/montage/assets"
os.makedirs(f"{A}/brand", exist_ok=True)
shutil.copy(f"{BRAND_DIR}/{brand['logo']}", f"{A}/brand/logo.png")
shutil.rmtree(f"{A}/brand/fonts", ignore_errors=True)
shutil.copytree(f"{BRAND_DIR}/fonts", f"{A}/brand/fonts")
shutil.copy(f"{ROOT}/work/voix_off.wav", f"{A}/voix_off.wav")
shutil.copy(broll_file, f"{A}/broll.mp4")
out = (tpl.replace("{{BRAND_CSS}}", "\n".join("      " + l for l in brand_css.splitlines()))
          .replace("{{BRAND}}", BRAND).replace("{{DUR}}", f"{DUR}")
          .replace("{{STREAKS}}", "\n      ".join(streaks))
          .replace("{{BACKDROP}}", f'<video id="broll" class="clip" src="assets/broll.mp4" data-start="0" data-duration="{BROLL_LEN:.3f}" muted data-track-index="1"></video><div id="dim"></div>')
          .replace("{{SCENES}}", "\n        ".join(scenes))
          .replace("{{CAPTIONS}}", "\n      ".join(caps))
          .replace("{{ENDCARD}}", endcard)
          .replace("{{AUDIO}}", "\n    ".join(aud))
          .replace("{{JS}}", "\n".join(js)))
open(f"{ROOT}/montage/index.html", "w").write(out)
print(f"index.html ({BRAND}, sans visage) : {DUR} s, {len(scenes)} scènes, {len(caps)} sous-titres, {len(aud)} pistes audio")
