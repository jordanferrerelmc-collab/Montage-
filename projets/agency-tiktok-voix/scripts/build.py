"""« Arrête de commencer par Salut » — TikTok Specimen Agency, DA motion design (DA.md, templates/reel-motion).

Voix fournie par l'utilisateur (src/voix.mp3, 33 s) et sa photo (src/photo.png, utilisée telle quelle, jamais animée
ni recouverte au niveau du visage). 7 scènes calées sur la voix, fonds clair / éclat / nuit, HUD de chapitres.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
sys.path.insert(0, f"{REPO}/templates/reel-motion")
from motion import Motion, ICONS as I, person

BRAND = os.environ.get("BRAND", "specimen-agency")
words = json.load(open(f"{ROOT}/work/transcript.json"))
words = words if isinstance(words, list) else words["words"]
W = [w["start"] for w in words]
T = [w["text"] for w in words]
VOICE_DUR, MAIN = 33.07, 33.4
B = [0.0, 5.45, 8.40, 13.05, 16.40, 22.20, 28.20, MAIN]
m = Motion(REPO, ROOT, BRAND)

X_SVG = '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" fill="none" style="stroke:var(--mo-ink)" stroke-width="3" stroke-linecap="round"/></svg>'
CUT_SVG = ('<svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.2"/>'
           '<circle cx="6" cy="18" r="3" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.2"/>'
           '<path d="M8.5 7.5L20 18M8.5 16.5L20 6" fill="none" style="stroke:var(--mo-ink)" stroke-width="2.2" stroke-linecap="round"/></svg>')
SAVE_SVG = '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" style="fill:var(--mo-on-accent)"/></svg>'
CHECK_ACC = I["check"].replace("<path", '<path style="fill:none;stroke:var(--mo-on-accent);stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round"')
PHOTO = '<img class="ph" src="assets/photo.jpg" alt=""/>'

def say(sid, idx, kinds, end, **kw):
    m.say(sid, [(W[i], T[i].replace("«", "").replace("»", "").strip() or T[i], kinds.get(i, "")) for i in idx], end, **kw)

def phone(pid, inner, cls=""):
    return f'<div class="phone {cls}" id="{pid}"><div class="island"></div><div class="scr">{inner}</div></div>'

def stk(sid, svg, x, y, acc=False, size=None):
    st = f' style="width:{size}px;height:{size}px"' if size else ""
    return f'<div class="abs" style="left:{x}px;top:{y}px"><div class="stk{" acc" if acc else ""}" id="{sid}"{st}>{svg}</div><i class="ring" id="{sid}r"></i></div>'

# ------------------------------------------------ 1. « Arrête de commencer tes vidéos par “Salut, aujourd'hui je vais vous parler de…” »
m.scene("s1", B[0], B[1]); m.push(B[0], B[1])
say("t1", range(0, 6), {0: "pill", 4: "kw"}, B[1])
m.add('<div class="slot" style="top:430px;height:960px">' + phone("ph1", PHOTO + '<div class="qb" id="qb"><span id="qt"></span><i class="caret"></i>'
      '<i class="strike" id="st"></i></div>') + "</div>")
m.add(stk("kx", X_SVG, 790, 1080))
m.tw("#ph1", "{scale: 0.94, y: 20}", "{scale: 1, y: 0}", 0.0, 0.8)          # visible dès l'image 0 (miniature)
m.pop("#qb", W[7] - 0.2, 0.45, 0.7, 20, sound="ui", vol=0.14)
m.type("#qt", "Salut, aujourd'hui je vais vous parler de…", W[7] - 0.05, 14)
m.sound("clavier-apple", W[7], 0.16); m.sound("clavier-apple", W[11], 0.13)
m.tw("#st", "{scaleX: 0, rotation: -5}", "{scaleX: 1, rotation: -5}", W[14] - 0.15, 0.3, "power3.out")
m.pop("#kx", W[14] - 0.1, 0.45, 0.4, 0, sound="impact-sec", vol=0.18); m.shock("#kxr", W[14] - 0.05)
m.wipe(B[1])

# ------------------------------------------------ 2. « Les premières secondes décident si on reste ou si on scrolle. » — ÉCLAT
m.scene("s2", B[1], B[2], ground="eclat", fill="lines"); m.push(B[1], B[2], 1.0, 1.03)
m.kin("k2", [("Les", False), ("premières", False), ("secondes.", True)], W[15] - 0.12, B[2], top=520,
      stagger=[W[15] - 0.12, W[16] - 0.12, W[17] - 0.12])
m.add('<div class="slot" style="top:1290px;height:120px;gap:40px"><span class="tag light" id="g1">rester</span>'
      '<span class="tag" id="g2">scroller</span></div>')
m.pop("#g1", W[21] - 0.05, 0.45, 0.6, 20, sound="ui", vol=0.13); m.pop("#g2", W[25] - 0.05, 0.45, 0.6, 20)
m.wipe(B[2])

# ------------------------------------------------ 3. « Si tu te présentes avant d'apporter quelque chose, la personne est déjà partie. » — NUIT
m.scene("s3", B[2], B[3], ground="nuit", fill="grid", glow=True); m.push(B[2], B[3])
say("t3", range(26, 39), {29: "kw", 31: "kw", 32: "kw", 33: "kw", 38: "pill"}, B[3], size=54)
feed = ('<div class="feed" id="feed"><div class="fi">' + PHOTO +
        f'<div class="abs" style="left:18px;right:18px;bottom:60px"><div class="card mini2" id="c3a"><span class="ic">{I["bubble"]}</span>'
        '<span class="ln" style="flex:1"><b></b><b></b></span></div></div></div>'
        f'<div class="fi">{person("var(--mo-line)", "var(--mo-card)")}</div></div>')
m.add('<div class="slot" style="top:500px;height:920px">' + phone("ph3", feed) + "</div>")
m.add(stk("kq", '<b class="qm">?</b>', 800, 640))
m.add(stk("ku", I["up"], 130, 1000))
m.pop("#ph3", B[2], 0.6, sound="ui", vol=0.15)
m.slide("#c3a", W[29] - 0.1, 0, 40, 0.45)
m.pop("#kq", W[31] - 0.05, 0.5, 0.4, 0); m.shock("#kqr", W[31]); m.bob("#kq", W[31] + 0.5, B[3], 8)
m.tw("#feed", "{yPercent: 0}", "{yPercent: -50}", W[37] - 0.1, 0.45, "power3.inOut")      # la personne scrolle
m.sound("whoosh-court", W[37] - 0.15, 0.16)
m.pop("#ku", W[37], 0.45, 0.4, 0); m.shock("#kur", W[37] + 0.05)
m.through(B[3])

# ------------------------------------------------ 4. « Fais l'inverse ! Commence par la promesse ou le résultat. »
m.scene("s4", B[3], B[4]); m.push(B[3], B[4])
say("t4", range(39, 48), {40: "pill", 44: "kw", 47: "kw"}, B[4])
m.add(stk("ks", I["sync"], 450, 520, acc=True, size=180))
m.add('<div class="slot" style="top:860px;height:420px;gap:28px">'
      f'<div class="opt" id="o1"><div class="stk">{I["spark"]}</div><b>La promesse</b></div>'
      '<span class="tag" id="ou">ou</span>'
      f'<div class="opt" id="o2"><div class="stk">{I["up"]}</div><b>Le résultat</b></div></div>')
m.pop("#ks", W[39] - 0.05, 0.5, 0.4, 0, sound="ui", vol=0.15); m.shock("#ksr", W[40])
m.tw("#ks svg", "{rotation: 0}", "{rotation: 180}", W[40] - 0.05, 0.6, "back.inOut(1.6)")
m.punch(W[40], 1.05, 0.4)
m.pop("#o1", W[44] - 0.08, 0.5, 0.6, 30, sound="ui", vol=0.13)
m.pop("#ou", W[45] - 0.05, 0.4, 0.5, 10)
m.pop("#o2", W[47] - 0.08, 0.5, 0.6, 30, sound="ui", vol=0.13)
m.through(B[4])

# ------------------------------------------------ 5. « Par exemple, voici comment attirer plus de clients dans ta boutique. Et seulement après, tu expliques. »
m.scene("s5", B[4], B[5]); m.push(B[4], B[5])
say("t5", range(48, 64), {52: "kw", 53: "kw", 54: "kw", 55: "kw", 58: "kw", 61: "pill"}, B[5], size=52)
m.add('<div class="slot" style="top:500px;height:700px">' + phone("ph5", PHOTO + '<div class="qb good" id="qb5"><span id="qt5"></span>'
      '<i class="caret"></i></div>', "sm") + "</div>")
m.add(stk("k5", CHECK_ACC, 790, 940, acc=True))
m.pop("#ph5", B[4], 0.6, sound="ui", vol=0.14)
m.pop("#qb5", W[50] - 0.25, 0.4, 0.7, 20)
end5 = m.type("#qt5", "Voici comment attirer plus de clients dans ta boutique", W[50] - 0.05, 21)
m.sound("clavier-apple", W[50], 0.16); m.sound("clavier-apple", W[54], 0.13)
m.pop("#k5", end5 + 0.05, 0.5, 0.4, 0, sound="validation", vol=0.15); m.shock("#k5r", end5 + 0.1)
STEPS5 = [("La promesse", W[59]), ("L'explication", W[62])]
m.add('<div class="slot" style="top:1225px;height:220px"><div style="display:flex;flex-direction:column;align-items:center;gap:20px">'
      + "".join(f'<div class="step" id="p5{k}"><span class="n">{k + 1}</span>{tx}<span class="tick" id="p5t{k}">{I["check"]}</span></div>'
                for k, (tx, _) in enumerate(STEPS5)) + "</div></div>")
for k, (tx, t) in enumerate(STEPS5):
    m.slide(f"#p5{k}", t - 0.1, 0, 24, 0.45)
    m.tick(f"#p5t{k}", t + 0.35, sound=False)
m.through(B[5])

# ------------------------------------------------ 6. « Test simple. Reprends ta dernière vidéo, coupe la première phrase et regarde si elle démarre mieux. »
m.scene("s6", B[5], B[6]); m.push(B[5], B[6])
say("t6a", range(64, 66), {64: "pill"}, W[66] - 0.05)
say("t6b", range(66, 80), {68: "kw", 69: "kw", 70: "kw", 72: "kw", 73: "kw", 79: "kw"}, B[6])
pv = PHOTO.replace('class="ph"', 'class="ph wide"')      # visage visible, aucun texte dessus
m.add('<div class="slot" style="top:520px;height:860px"><div class="win" id="win"><div class="tb"><i></i><i></i><i></i><b></b></div>'
      f'<div class="pv">{pv}</div><div class="tracks">'
      '<div class="tr"><i class="clipb ink" id="c0" style="left:1%;width:20%"><em id="i6a">Salut…</em></i><div class="rest" id="rest">'
      '<i class="clipb" style="left:22%;width:30%"></i><i class="clipb" style="left:53%;width:22%"></i><i class="clipb" style="left:76%;width:23%"></i></div></div>'
      '<div class="tr"><i class="clipb soft" style="left:10%;width:40%"></i><i class="clipb soft" style="left:55%;width:30%"></i></div>'
      '<i class="head" id="head6" style="left:2%"></i></div></div></div>')
m.add(stk("kc", CUT_SVG, 465, 1400))
m.add(stk("k6", I["up"], 800, 470))
m.pop("#win", B[5], 0.6, sound="ui", vol=0.15)
m.tw("#head6", "{x: 0}", "{x: 160}", B[5] + 0.3, W[70] - B[5] - 0.3, "none")
m.pop("#kc", W[70] - 0.1, 0.45, 0.4, 0, sound="impact-sec", vol=0.16); m.shock("#kcr", W[70])
m.tw("#c0", "{scaleX: 1, opacity: 1}", "{scaleX: 0, opacity: 0}", W[72], 0.3, "power2.in", False)
m.tw("#i6a", "{opacity: 1}", "{opacity: 0}", W[72], 0.2, "power2.in", False)
m.tw("#rest", "{x: 0}", "{x: -182}", W[73], 0.45, "power3.inOut", False)
m.tw("#head6", "{x: 160}", "{x: 0}", W[74], 0.25, "power2.out", False)
m.tw("#head6", "{x: 0}", "{x: 700}", W[74] + 0.3, B[6] - W[74] - 0.6, "none", False)
m.pop("#k6", W[79] - 0.1, 0.45, 0.4, 0, sound="ui", vol=0.14); m.shock("#k6r", W[79])
m.punch(W[70], 1.05, 0.4)
m.through(B[6])

# ------------------------------------------------ 7. « Enregistre cette vidéo pour la retrouver et commente Hook si tu veux d'autres astuces comme celle-là. »
m.scene("s7", B[6], B[7]); m.push(B[6], B[7], 1.0, 1.04)
say("t7", range(80, 96), {80: "kw", 88: "pill", 93: "kw"}, MAIN, size=56)
m.add(stk("ksv", SAVE_SVG, 440, 560, acc=True, size=200))
m.add('<div class="slot" style="top:900px;height:130px"><div class="prompt" id="pc" style="width:820px">'
      f'<span class="si">{I["bubble"]}</span><span><span id="tyc"></span><i class="caret"></i></span></div></div>')
m.add(f'<div class="slot" style="top:1090px;height:120px"><div class="card" id="cmt"><span class="ic">{I["bubble"]}</span>Hook</div></div>')
m.pop("#ksv", W[80] - 0.05, 0.55, 0.4, 0, sound="ui", vol=0.16); m.shock("#ksvr", W[80])
m.bob("#ksv", W[80] + 0.6, MAIN, 8)
m.pop("#pc", W[86] - 0.2, 0.5, 0.7, 20)
end7 = m.type("#tyc", "Hook", W[88] - 0.05, 9)
m.sound("clavier-apple", W[88], 0.16)
m.slide("#cmt", end7 + 0.15, 0, 40, 0.45); m.sound("validation", end7 + 0.15, 0.14)
m.punch(W[88], 1.05, 0.4)

for a, b, lab in [(B[0], B[3], "01 / 03 · Le problème"), (B[3], B[6], "02 / 03 · La méthode"), (B[6], MAIN, "03 / 03 · À toi")]:
    m.chapter(a, b, lab)

EXTRA = """
.ph { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 28%; display: block; }
.ph.wide { object-position: 50% 37%; }
#win .pv { height: 520px; }
.clipb em { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-style: normal;
  font-weight: 700; font-size: 28px; color: var(--mo-bg); white-space: nowrap; }
.qb { position: absolute; left: 16px; right: 16px; bottom: 64px; min-height: 120px; padding: 18px 22px; border-radius: 24px;
  background: rgba(0, 0, 0, 0.62); color: #ffffff; font-weight: 700; font-size: 32px; line-height: 1.22; }
.phone.sm .qb { font-size: 28px; bottom: 40px; min-height: 100px; }
.qb.good { background: rgba(227, 178, 92, 0.94); color: #0b0b0d; }
.qb .caret { height: 32px; vertical-align: -4px; background: currentColor; }
.strike { position: absolute; left: 6px; right: 6px; top: 48%; height: 8px; border-radius: 4px; background: var(--mo-accent);
  transform-origin: 0 50%; transform: scaleX(0); }
.feed { position: absolute; left: 0; right: 0; top: 0; height: 200%; }
.feed .fi { position: relative; height: 50%; overflow: hidden; }
.card.mini2 { padding: 12px 18px 12px 12px; border-radius: 22px; }
.card.mini2 .ic { width: 48px; height: 48px; } .card.mini2 .ln b { width: 180px; height: 12px; } .card.mini2 .ln b + b { width: 110px; }
.qm { font-size: 92px; font-weight: 700; color: var(--mo-kw); line-height: 1; }
.opt { width: 340px; padding: 40px 24px 36px; border-radius: 44px; background: var(--mo-card); display: flex; flex-direction: column;
  align-items: center; gap: 26px; box-shadow: 0 26px 60px rgba(var(--mo-shadow), 0.22); }
.opt .stk { width: 130px; height: 130px; } .opt .stk svg { width: 72px; height: 72px; }
.opt b { font-size: 42px; letter-spacing: -0.02em; white-space: nowrap; }
.rest { position: absolute; inset: 0; }
"""
m.write(MAIN, "assets/voix.wav", VOICE_DUR, extra_css=EXTRA, title="arrête de commencer par salut")
