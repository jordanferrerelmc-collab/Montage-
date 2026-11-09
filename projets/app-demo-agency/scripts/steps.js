// Démo « Du rush au Reel » (Specimen Agency) — scène 1200 × 750, une étape = { id, name, dur, html, draw, say, clicks, keys }.
// Interface 100 % originale, couleurs uniquement par variables de la charte.
const CK = '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" style="stroke:currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const side = (on) => `<div class="sp-side"><h4>PROJETS</h4>${["Reel conseils", "Interview", "Process"]
  .map((n, i) => `<div class="sp-card${i === on ? " on" : ""}" style="font-size:26px">${n}</div>`).join("")}
  <div class="sp-muted" style="margin-top:auto">Specimen Agency</div></div>`;
const abs = (l, t, w, h, extra = "") => `position:absolute;left:${l}px;top:${t}px;${w ? `width:${w}px;` : ""}${h ? `height:${h}px;` : ""}${extra}`;
const WAVE = Array.from({ length: 64 }, (_, i) => {
  const silent = [10, 11, 12, 24, 25, 38, 39, 40, 52, 53].includes(i);
  return { silent, h: silent ? 5 : 22 + 70 * Math.abs(Math.sin(i * 1.7) * Math.cos(i * 0.43)) };
});
const GROUPS = [[1.2, "Tes vidéos"], [2.0, "Instagram"], [2.7, "font"], [3.2, "<span style='color:var(--accent)'>200 vues</span>"]];

const STEPS = [
  {
    id: "import", name: "Importer", dur: 3.6, say: "Importe ton <span class='a'>rush</span>", clicks: [1.35],
    html: `<div class="sp-app">${side(0)}<div class="sp-main">
      <div class="sp-title">Nouveau montage</div><div class="sp-muted">Glisse ta vidéo ou importe-la</div>
      <div id="drop" style="${abs(32, 170, 836, 420, "border:3px dashed var(--dark);border-radius:22px")}"></div>
      <div class="sp-btn" id="imp" style="${abs(330, 348, 240)}">Importer</div>
      <div class="sp-card" id="file" style="${abs(32, 170, 836, 420, "display:flex;gap:30px;align-items:center;padding:30px")}">
        <img src="assets/thumb.jpg" style="height:356px;width:200px;object-fit:cover;border-radius:14px"/>
        <div style="flex:1;display:flex;flex-direction:column;gap:20px">
          <div style="font-size:34px">video1.mp4</div><div class="sp-muted">1080 × 1920 · 28,4 s · voix</div>
          <div class="sp-progress" id="pg"><i></i></div>
          <div class="sp-row" style="justify-content:flex-start"><span class="sp-check" id="ok">${CK}</span><span class="sp-muted" id="okt">Import…</span></div>
        </div></div></div></div>`,
    draw(t, $) {
      const k = ease(t, 1.5, 1.8);
      $("#drop").style.borderColor = t > 0.9 && t < 1.5 ? "var(--accent)" : "var(--dark)";
      $("#imp").style.opacity = t < 1.5 ? 1 : 0;
      $("#file").style.opacity = k;
      $("#file").style.transform = `translateY(${(1 - k) * 24}px)`;
      $("#pg").style.setProperty("--p", ease(t, 1.7, 2.9));
      $("#ok").style.opacity = t > 2.9 ? 1 : 0.15;
      $("#okt").textContent = t > 2.9 ? "Importé" : "Import…";
      return { cursor: glide(t, [[0, 0, 1020, 660], [0.3, 1.2, 750, 380], [1.8, 2.6, 1060, 690]], [1.35]) };
    },
  },
  {
    id: "cut", name: "Silences", dur: 5.0, say: "Les blancs <span class='a'>disparaissent</span>", clicks: [0.8],
    html: `<div class="sp-app">${side(0)}<div class="sp-main">
      <div class="sp-row"><div class="sp-title">video1.mp4</div><div class="sp-title" id="len" style="color:var(--accent)">28,4 s</div></div>
      <div class="sp-muted">Détection des silences</div>
      <div id="wave" style="${abs(32, 180, 836, 260, "display:flex;align-items:center;gap:3px")}">${WAVE
        .map((b) => `<i class="${b.silent ? "sil" : ""}" style="display:block;flex:0 0 10px;height:${b.h}%;border-radius:4px;background:var(--stone)"></i>`).join("")}</div>
      <div class="sp-btn" id="go" style="${abs(32, 480, 340)}">Couper les blancs</div>
      <div class="sp-toast" id="toast"><span class="sp-check">${CK}</span>1,4 s de blancs retirés · 10 coupes</div></div></div>`,
    draw(t, $) {
      const mark = ease(t, 0.9, 1.3), cut = ease(t, 1.8, 2.7);
      $("#wave").querySelectorAll("i").forEach((el) => {
        if (!el.classList.contains("sil")) return;
        el.style.background = mark > 0 ? "var(--accent)" : "var(--stone)";
        el.style.opacity = String(1 - cut);
        el.style.flexBasis = `${10 * (1 - cut)}px`;
        el.style.height = `${5 + 90 * mark * (1 - cut)}%`;
      });
      $("#len").textContent = `${(28.4 - 1.4 * cut).toFixed(1).replace(".", ",")} s`;
      $("#go").style.opacity = t > 2.7 ? 0.35 : 1;
      const k = ease(t, 2.3, 2.6);
      $("#toast").style.opacity = k;
      $("#toast").style.transform = `translate(-50%, ${(1 - k) * 30}px)`;
      return { cursor: glide(t, [[0, 0, 1040, 690], [0.1, 0.7, 520, 515], [1.2, 2.0, 980, 640]], [0.8]) };
    },
  },
  {
    id: "subs", name: "Sous-titres", dur: 4.6, say: "Sous-titres <span class='a'>mot à mot</span>", clicks: [0.8],
    html: `<div class="sp-app">${side(0)}<div class="sp-main">
      <div style="${abs(32, 28, 300, 533, "border-radius:22px;overflow:hidden;border:2px solid var(--dark)")}">
        <img src="assets/thumb.jpg" style="width:100%;height:100%;object-fit:cover"/>
        <div id="cap" style="position:absolute;left:0;right:0;top:330px;text-align:center;font-size:34px;color:var(--ink);text-shadow:0 3px 14px rgba(0,0,0,0.8)"></div></div>
      <div class="sp-muted" style="${abs(380, 34)}">Style des sous-titres</div>
      <div class="sp-chip" id="c1" style="${abs(380, 80, 300, null, "justify-content:center")}">Classique</div>
      <div class="sp-chip" id="c2" style="${abs(380, 140, 300, null, "justify-content:center")}">Charte Specimen</div>
      <div class="sp-card" id="spec" style="${abs(380, 210, 470, null, "display:flex;flex-direction:column;gap:12px")}">
        <div class="sp-row"><span class="sp-muted">Police</span><span>Specimen Heros · gras</span></div>
        <div class="sp-row"><span class="sp-muted">Rythme</span><span>1 à 3 mots</span></div>
        <div class="sp-row"><span class="sp-muted">Mots clés</span><span style="color:var(--accent)">Or</span></div></div>
      <div id="lines" style="${abs(380, 420, 470, null, "display:flex;flex-direction:column;gap:8px;font-size:26px")}">${GROUPS
        .map(([at, w]) => `<div class="sp-row"><span class="sp-muted">${at.toFixed(1).replace(".", ",")} s</span><span>${w}</span></div>`).join("")}</div>
      </div></div>`,
    draw(t, $) {
      const on = t > 0.8;
      $("#c1").classList.toggle("on", !on);
      $("#c2").classList.toggle("on", on);
      $("#spec").style.opacity = ease(t, 0.85, 1.15);
      $("#spec").classList.toggle("on", on);
      const g = cue(t, GROUPS.map(([at], i) => [at, i]), -1);
      $("#cap").innerHTML = g < 0 ? "" : GROUPS[g][1];
      $("#lines").querySelectorAll(".sp-row").forEach((r, i) => { r.style.opacity = i <= g ? 1 : 0.3; });
      return { cursor: glide(t, [[0, 0, 1020, 640], [0.1, 0.7, 830, 165], [1.4, 2.2, 1100, 700]], [0.8]) };
    },
  },
  {
    id: "export", name: "Exporter", dur: 4.4, say: "Ton Reel est <span class='a'>prêt</span>", clicks: [0.7],
    html: `<div class="sp-app">${side(0)}<div class="sp-main">
      <div class="sp-title">Exporter</div>
      ${[["Format", "1080 × 1920 · Reel"], ["Son", "Normalisé à -14 LUFS"], ["Fichiers", "HD + version légère"]]
        .map(([a, b]) => `<div class="sp-card sp-row"><span class="sp-muted">${a}</span><span>${b}</span></div>`).join("")}
      <div class="sp-row" style="justify-content:flex-start;gap:28px"><div class="sp-btn" id="ex" style="width:260px">Exporter</div>
        <div style="flex:1;display:flex;flex-direction:column;gap:10px"><div class="sp-progress" id="pg"><i></i></div><div class="sp-muted" id="pc">0 %</div></div></div>
      <div class="sp-toast" id="toast"><span class="sp-check">${CK}</span>Reel prêt · 1080×1920 · 27 s</div></div></div>`,
    draw(t, $) {
      const p = ease(t, 0.9, 2.2);
      $("#pg").style.setProperty("--p", p);
      $("#pc").textContent = t < 0.9 ? "Prêt à exporter" : `${Math.round(p * 100)} %`;
      $("#ex").classList.toggle("ghost", t > 0.7);
      const k = ease(t, 2.3, 2.6);
      $("#toast").style.opacity = k;
      $("#toast").style.transform = `translate(-50%, ${(1 - k) * 30}px)`;
      return { cursor: glide(t, [[0, 0, 1040, 690], [0.1, 0.6, 470, 455], [1.2, 2.0, 1080, 660]], [0.7]) };
    },
  },
];
