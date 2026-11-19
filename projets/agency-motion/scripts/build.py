"""« Sous-titres = vues » en style « motion design clair » (templates/reel-motion) — démo Specimen Agency.

Même voix off que projets/agency-soustitres (ElevenLabs, fournie par l'utilisateur). Une phrase qui s'écrit mot à mot en
haut, un objet central par phrase, cartes et coches, transitions zoom entre les parties, coups de zoom sur les mots forts.
Aucun chiffre inventé, aucun logo ni interface d'application réelle (illustrations maison).
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
sys.path.insert(0, f"{REPO}/templates/reel-motion")
from motion import Motion, ICONS as I, person

BRAND = os.environ.get("BRAND", "specimen-agency")
SRC = f"{REPO}/projets/agency-soustitres"
words = json.load(open(f"{SRC}/work/transcript.json"))
W = [w["start"] for w in words]
VOICE_DUR, MAIN = 18.76, 19.0
B = [0.0, 1.50, 4.72, 6.06, 9.86, 14.70, MAIN]           # scènes
m = Motion(REPO, ROOT, BRAND)
os.makedirs(f"{ROOT}/montage/assets", exist_ok=True)
shutil.copy(f"{SRC}/montage/assets/voix.wav", f"{ROOT}/montage/assets/voix.wav")

def say(sid, idx, kinds, end, **kw):
    m.say(sid, [(W[i], words[i]["text"], kinds.get(i, "")) for i in idx], end, **kw)

def card(cid, icon, title, sub=None):
    return (f'<div class="card" id="{cid}"><span class="ic">{I[icon]}</span><span>{title}'
            + (f"<small>{sub}</small>" if sub else "") + "</span></div>")

# ---------------------------------------------------------------- 1. « Trois mots pour booster vos vues. »
m.scene("s1", B[0], B[1]); m.push(B[0], B[1])
say("t1", range(0, 6), {0: "kw", 1: "kw", 5: "pill"}, B[1])
m.add(f'<div class="slot" style="top:470px;height:900px"><div class="phone" id="ph1"><div class="island"></div><div class="scr">{person()}</div></div></div>')
m.add(f'<div class="abs" style="left:770px;top:600px"><div class="stk" id="k1">{I["up"]}</div><i class="ring" id="r1"></i></div>')
m.add(f'<div class="abs" style="left:160px;top:960px"><div class="stk" id="k2">{I["eye"]}</div><i class="ring" id="r2"></i></div>')
m.tw("#ph1", "{scale: 0.94, y: 20}", "{scale: 1, y: 0}", 0.0, 0.8)     # visible dès l'image 0 (miniature des réseaux)
m.pop("#k1", W[3] - 0.04, sound="ui", vol=0.14); m.shock("#r1", W[3])
m.pop("#k2", W[5] - 0.04); m.shock("#r2", W[5])
m.bob("#k1", W[3] + 0.5, B[1], 8); m.bob("#k2", W[5] + 0.5, B[1], 8)
m.through(B[1])

# ---------------------------------------------------------------- 2. « Les sous-titres retiennent l'attention et boostent l'engagement. »
m.scene("s2", B[1], B[2]); m.push(B[1], B[2])
say("t2", range(6, 13), {7: "kw", 9: "kw", 12: "pill"}, B[2])
m.add('<div class="slot" style="top:560px;height:500px"><div class="player" id="pl">' + person(wide=True) +
      '<div class="incap" style="bottom:86px"><span style="font-size:58px" id="ic1">retiennent</span></div>'
      '<div class="incap" style="bottom:86px"><span style="font-size:58px" id="ic2"><b>l\'attention</b></span></div>'
      '<div class="bar"><i id="plb"></i></div></div></div>')
m.pop("#pl", B[1], 0.6)
m.grow("#plb", B[1], B[2] - B[1], "scaleX")
m.pop("#ic1", W[8] - 0.04, 0.35, 0.7, 10, sound="ui", vol=0.12); m.out("#ic1", W[9] - 0.08, 0.1)
m.pop("#ic2", W[9] - 0.04, 0.35, 0.7, 10)
CARDS = [("ca", "eye", "Attention", 150, 1130, W[9]), ("cb", "heart", "J'aime", 610, 1220, W[11]),
         ("cc", "bubble", "Commentaire", 150, 1360, W[12]), ("cd", "share", "Partage", 620, 1470, W[12] + 0.22)]
for cid, ic, tt, x, y, t in CARDS:
    m.add(f'<div class="abs" style="left:{x}px;top:{y}px">{card(cid, ic, tt)}</div>')
    m.pop(f"#{cid}", t, sound="ui" if cid in ("ca", "cc") else None, vol=0.12)
    m.bob(f"#{cid}", t + 0.55, B[2], 9, 1.6 + 0.2 * len(tt) % 3)
m.punch(W[11], 1.05, 0.35)
m.wipe(B[2])

# ---------------------------------------------------------------- 3. « Étape par étape. » — fond ÉCLAT (or plein cadre), typo cinétique
m.scene("s3", B[2], B[3], ground="eclat", fill="lines"); m.push(B[2], B[3], 1.0, 1.03)
m.kin("k3", [("Étape", False), ("par", False), ("étape.", True)], W[13] - 0.15, B[3], top=560, stagger=[W[13] - 0.15, W[14] - 0.15, W[15] - 0.15])
m.add('<div class="slot" style="top:1270px;height:160px"><div style="display:flex;gap:44px">'
      + "".join(f'<div class="num" id="n{k}">{k + 1}</div>' for k in range(3)) + "</div></div>")
for k, t in enumerate((W[13], W[14], W[15])):
    m.pop(f"#n{k}", t + 0.1, 0.45, 0.4, 20, sound="ui" if k == 0 else None, vol=0.15)
m.wipe(B[3])

# ---------------------------------------------------------------- 4. « Un texte court, synchronisé, des overlays qui apparaissent au bon moment. »
m.scene("s4", B[3], B[4]); m.push(B[3], B[4])
say("t4", range(16, 27), {17: "kw", 18: "kw", 19: "kw", 21: "kw", 26: "pill"}, B[4])
pv = (person(wide=True) + '<div class="incap" style="bottom:40px"><span style="font-size:44px" id="ic4">Un texte <b>court</b></span></div>'
      f'<div class="abs" style="left:40px;top:40px"><div class="stk" id="ov1" style="width:96px;height:96px">{I["spark"]}</div></div>'
      f'<div class="abs" style="right:40px;top:60px"><div class="stk" id="ov2" style="width:96px;height:96px">{I["heart"]}</div></div>')
m.add('<div class="slot" style="top:545px;height:720px"><div class="win" id="win"><div class="tb"><i></i><i></i><i></i><b></b></div>'
      f'<div class="pv">{pv}</div><div class="tracks">'
      '<div class="tr"><i class="clipb ink" style="left:1%;width:98%"></i></div>'
      '<div class="tr"><i class="clipb" id="cl1" style="left:4%;width:20%"></i><i class="clipb" id="cl2" style="left:26%;width:24%"></i>'
      '<i class="clipb" id="cl3" style="left:52%;width:20%"></i></div>'
      '<div class="tr"><i class="clipb soft" id="cl4" style="left:46%;width:16%"></i><i class="clipb soft" id="cl5" style="left:66%;width:14%"></i>'
      '<i class="clipb soft" id="cl6" style="left:82%;width:14%"></i></div>'
      '<i class="head" id="head" style="left:4%"></i></div></div></div>')
m.pop("#win", B[3], 0.6, sound="ui", vol=0.15)
m.tw("#head", "{x: 0}", "{x: 818}", B[3] + 0.3, B[4] - B[3] - 0.5, "none")
for k, t in enumerate((W[17], W[18], W[19])):
    m.tw(f"#cl{k + 1}", "{scaleX: 0, opacity: 0}", "{scaleX: 1, opacity: 1}", t - 0.04, 0.3, "back.out(1.6)")
for k, t in enumerate((W[21], W[23], W[25])):
    m.tw(f"#cl{k + 4}", "{scaleX: 0, opacity: 0}", "{scaleX: 1, opacity: 1}", t - 0.04, 0.3, "back.out(1.6)")
m.pop("#ic4", W[17] - 0.04, 0.35, 0.7, 10)
m.pop("#ov1", W[23] - 0.04, 0.45, 0.4, 0, sound="ui", vol=0.12); m.pop("#ov2", W[25] - 0.04, 0.45, 0.4, 0)
STEPS = [("Texte court", W[18]), ("Synchronisé", W[19]), ("Overlays au bon moment", W[24])]
m.add('<div class="slot" style="top:1262px;height:330px"><div style="display:flex;flex-direction:column;align-items:center;gap:22px">'
      + "".join(f'<div class="step" id="sp{k}"><span class="n">{k + 1}</span>{tx}<span class="tick" id="tk{k}">{I["check"]}</span></div>'
                for k, (tx, _) in enumerate(STEPS)) + "</div></div>")
for k, (tx, t) in enumerate(STEPS):
    m.slide(f"#sp{k}", t - 0.45 if k < 2 else W[19] + 0.4, 0, 24)
    m.tick(f"#tk{k}", t + 0.05, sound=(k == 0))
m.punch(W[19], 1.05, 0.5)
m.through(B[4])

# ---------------------------------------------------------------- 5. « Preuve rapide, plus de vues et plus de commentaires quand les sous-titres accompagnent. »
m.scene("s5", B[4], B[5], ground="nuit", fill="grid", glow=True); m.push(B[4], B[5])
say("t5a", range(27, 29), {27: "pill"}, W[29])
say("t5b", range(29, 40), {31: "kw", 35: "kw", 38: "kw"}, B[5])
mini = "".join(f'<div class="card mini" id="cm{k}"><span class="ic">{I["bubble"]}</span><span class="ln"><b></b><b></b></span></div>' for k in range(3))
m.add('<div class="slot" style="top:500px;height:720px;gap:150px">'
      f'<div class="phone sm" id="pa"><div class="island"></div><div class="scr">{person("var(--mo-line)", "var(--mo-card)")}</div></div>'
      f'<div class="phone sm" id="pb"><div class="island"></div><div class="scr">{person()}'
      '<div class="incap" style="bottom:70px"><span style="font-size:40px" id="ic5">plus de <b>vues</b></span></div>'
      f'<div class="coms">{mini}</div></div></div></div>')
m.add('<div class="abs" style="left:150px;top:1240px;width:300px;text-align:center"><span class="tag light" id="ta">Sans sous-titres</span></div>')
m.add('<div class="abs" style="left:630px;top:1240px;width:300px;text-align:center"><span class="tag" id="tb">Avec sous-titres</span></div>')
m.add(f'<div class="abs" style="left:830px;top:470px"><div class="stk" id="k5">{I["eye"]}</div><i class="ring" id="r5"></i></div>')
m.add(f'<div class="abs" style="left:705px;top:1350px"><div class="stk acc" id="k6">{I["check"].replace("<path", "<path style=" + chr(34) + "fill:none;stroke:var(--mo-on-accent);stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round" + chr(34))}</div><i class="ring" id="r6"></i></div>')
m.pop("#pa", B[4], 0.6); m.pop("#pb", B[4] + 0.12, 0.6, sound="ui", vol=0.15)
m.slide("#ta", W[28], 0, 30); m.slide("#tb", W[28] + 0.12, 0, 30)
m.pop("#ic5", W[31] - 0.04, 0.35, 0.7, 10)
m.pop("#k5", W[31] - 0.04, sound="ui", vol=0.13); m.shock("#r5", W[31]); m.bob("#k5", W[31] + 0.5, B[5], 8)
for k in range(3):
    m.slide(f"#cm{k}", W[35] - 0.3 + 0.2 * k, 0, 60, 0.45)
m.sound("ui", W[35] - 0.3, 0.12)
m.tw("#pa", "{opacity: 1}", "{opacity: 0.45}", W[39] - 0.04, 0.4, "power2.out", False)
m.pop("#k6", W[39] - 0.04, 0.5, 0.4, 20); m.shock("#r6", W[39]); m.sound("validation", W[39], 0.16)
m.punch(W[39], 1.05, 0.15)
m.through(B[5])

# ---------------------------------------------------------------- 6. « Recherchez Astuce Visibilité TikTok et testez ces astuces tout de suite ! »
m.scene("s6", B[5], B[6]); m.push(B[5], B[6], 1.0, 1.04)
m.say("t6", [(W[40], "Recherchez", ""), (W[41], "Astuce Visibilité TikTok", "pill"), (W[44], "et", ""), (W[45], "testez", "kw"),
             (W[46], "ces", ""), (W[47], "astuces", "kw"), (W[48], "tout", ""), (W[49], "de", ""), (W[50], "suite !", "kw")], MAIN, size=56)
m.add(f'<div class="slot" style="top:600px;height:140px"><div class="prompt" id="pr"><span class="si">{I["search"]}</span>'
      '<span><span id="ty"></span><i class="caret" id="car"></i></span></div></div>')
m.pop("#pr", B[5], 0.55, sound="ui", vol=0.15)
end_type = m.type("#ty", "Astuce Visibilité TikTok", W[41], 17)
m.sound("clavier-apple", W[41], 0.2); m.sound("clavier-apple", W[41] + 0.6, 0.16)
for k, t in enumerate((W[44] - 0.2, W[45] - 0.05, W[46] + 0.05)):
    m.add(f'<div class="abs" style="left:160px;top:{800 + 150 * k}px"><div class="card" id="re{k}" style="width:760px">'
          f'<span class="ic">{I["spark"]}</span><span class="ln" style="flex:1"><b style="width:380px"></b><b></b></span>'
          f'<span class="tick" id="rk{k}">{I["check"]}</span></div></div>')
    m.slide(f"#re{k}", t, 0, 50, 0.45)
for k, t in enumerate((W[45], W[46] + 0.15, W[47])):
    m.tick(f"#rk{k}", t + 0.25, sound=(k == 0))
m.add(f'<div class="abs" style="left:465px;top:1290px"><div class="stk acc" id="k7">{I["bolt"].replace("var(--mo-kw)", "var(--mo-on-accent)")}</div><i class="ring" id="r7"></i></div>')
m.pop("#k7", W[48] - 0.04, 0.55, 0.4, 20, sound="ui", vol=0.16); m.shock("#r7", W[48])
m.punch(W[48], 1.06, 0.6)

for k, (a, b, lab) in enumerate([(B[0], B[2], "01 / 04 · Pourquoi"), (B[2], B[4], "02 / 04 · La méthode"),
                                 (B[4], B[5], "03 / 04 · La preuve"), (B[5], MAIN, "04 / 04 · À toi")]):
    m.chapter(a, b, lab)

EXTRA = """
.card.mini { padding: 10px 16px 10px 10px; border-radius: 22px; gap: 12px; }
.card.mini .ic { width: 44px; height: 44px; border-radius: 14px; } .card.mini .ic svg { width: 26px; height: 26px; }
.card.mini .ln b { width: 150px; height: 11px; } .card.mini .ln b + b { width: 96px; }
.coms { position: absolute; left: 16px; right: 16px; top: 80px; display: flex; flex-direction: column; gap: 12px; }
"""
m.write(MAIN, "assets/voix.wav", VOICE_DUR, extra_css=EXTRA, title="sous-titres = vues (motion clair)")
