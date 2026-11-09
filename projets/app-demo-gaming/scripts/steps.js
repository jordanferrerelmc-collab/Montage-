// Démo « Ma 4-3-1-2 en 4 étapes » (Specimen Gaming) — scène 1200 × 750, interface 100 % originale (aucune UI du jeu).
const CK = '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" style="stroke:currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const abs = (l, t, w, h, extra = "") => `position:absolute;left:${l}px;top:${t}px;${w ? `width:${w}px;` : ""}${h ? `height:${h}px;` : ""}${extra}`;
const side = `<div class="sp-side"><h4>ÉQUIPE</h4>${["XI SPM", "Défense", "Réserve"]
  .map((n, i) => `<div class="sp-card${i === 0 ? " on" : ""}" style="font-size:26px">${n}</div>`).join("")}
  <div class="sp-muted" style="margin-top:auto">Specimen Gaming</div></div>`;
// joueurs (x %, y %) : gardien, 4 défenseurs, 4 milieux, 2 attaquants ; 4-4-2 → 4-3-1-2
const F442 = [[50, 91], [14, 73], [38, 77], [62, 77], [86, 73], [14, 48], [38, 52], [62, 52], [86, 48], [36, 18], [64, 18]];
const F4312 = [[50, 91], [14, 73], [38, 77], [62, 77], [86, 73], [24, 54], [50, 58], [76, 54], [50, 36], [36, 15], [64, 15]];
const pitch = (l, t, w, h) => `<div id="pitch" style="${abs(l, t, w, h, "border:2px solid var(--dark);border-radius:18px;background:var(--panel)")}">
  <i style="${abs(0, h / 2 - 1, w, 2, "background:var(--dark)")}"></i>
  <i style="${abs(w / 2 - 50, h / 2 - 50, 100, 100, "border:2px solid var(--dark);border-radius:50%")}"></i>
  ${F442.map((_, i) => `<b class="pl" style="position:absolute;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;
    background:${i >= 9 ? "var(--accent)" : "var(--ink)"};box-shadow:0 0 0 4px var(--black)"></b>`).join("")}</div>`;
function place($, from, to, k, hi = -1) {
  $("#pitch").querySelectorAll(".pl").forEach((el, i) => {
    el.style.left = `${from[i][0] + (to[i][0] - from[i][0]) * k}%`;
    el.style.top = `${from[i][1] + (to[i][1] - from[i][1]) * k}%`;
    el.style.transform = `scale(${i === hi ? 1.35 : 1})`;
    el.style.background = i === hi || i >= 9 ? "var(--accent)" : "var(--ink)";
  });
}
const ROLES = [[9, "Feller", "Renard des surfaces"], [10, "Chawinga", "Fausse 9"], [8, "López", "Meneuse de jeu"],
  [7, "Pedri", "Meneur de jeu"], [5, "Karchaoui", "Box-to-box"]];
const OPTS = ["4-4-2", "4-2-3-1", "4-3-1-2"];
const CODE = "Mpk&2iGeW4At";

const STEPS = [
  {
    id: "form", name: "Formation", dur: 4.4, say: "Choisis la <span class='a'>4-3-1-2</span>", clicks: [0.7, 1.9],
    html: `<div class="sp-app">${side}<div class="sp-main">
      <div class="sp-title">Formation</div>${pitch(32, 100, 340, 600)}
      <div class="sp-muted" style="${abs(420, 108)}">Dispositif</div>
      <div class="sp-card sp-row" id="dd" style="${abs(420, 150, 440, 70)}"><span id="ddv">4-4-2</span><svg viewBox="0 0 24 24" width="30" height="30"><path d="m6 9 6 6 6-6" fill="none" style="stroke:var(--accent)" stroke-width="3"/></svg></div>
      <div class="sp-card" id="menu" style="${abs(420, 230, 440, null, "padding:8px")}">${OPTS
        .map((o) => `<div class="opt" style="height:62px;padding:0 16px;display:flex;align-items:center;border-radius:12px">${o}</div>`).join("")}</div>
      <div class="sp-card" id="sum" style="${abs(420, 470, 440, null, "display:flex;flex-direction:column;gap:10px")}">
        <div class="sp-row"><span class="sp-muted">Défense</span><span>4</span></div>
        <div class="sp-row"><span class="sp-muted">Milieu</span><span>3 + 1</span></div>
        <div class="sp-row"><span class="sp-muted">Attaque</span><span style="color:var(--accent)">2</span></div></div></div></div>`,
    draw(t, $) {
      const open = t >= 0.7 && t < 1.95;
      $("#menu").style.opacity = open ? 1 : 0;
      $("#menu").querySelectorAll(".opt").forEach((o, i) => {
        o.style.background = open && i === 2 && t > 1.5 ? "var(--accent)" : "transparent";
        o.style.color = open && i === 2 && t > 1.5 ? "var(--black)" : "var(--ink)";
      });
      $("#ddv").textContent = t >= 1.9 ? "4-3-1-2" : "4-4-2";
      $("#dd").classList.toggle("on", open);
      place($, F442, F4312, ease(t, 2.1, 2.9));
      $("#sum").style.opacity = ease(t, 2.9, 3.2);
      return { cursor: glide(t, [[0, 0, 1080, 700], [0.05, 0.6, 960, 185], [1.0, 1.75, 820, 400], [2.3, 3.0, 1100, 700]], [0.7, 1.9]) };
    },
  },
  {
    id: "roles", name: "Rôles", dur: 4.8, say: "Un <span class='a'>rôle</span> à chaque poste", keys: [[0.3, 3.6]],
    html: `<div class="sp-app">${side}<div class="sp-main">
      <div class="sp-title">Rôles</div>${pitch(32, 100, 340, 600)}
      ${ROLES.map(([, n, r], i) => `<div class="sp-card role" style="${abs(410, 100 + i * 120, 460, 104, "display:flex;flex-direction:column;justify-content:center;gap:4px")}">
        <span class="nm" style="font-size:32px"></span><span class="sp-muted rl" style="color:var(--accent)"></span></div>`).join("")}</div></div>`,
    draw(t, $) {
      const cur = cue(t, ROLES.map((_, i) => [0.3 + i * 0.7, i]), -1);
      const rows = $(".sp-main").querySelectorAll(".role");
      ROLES.forEach(([, n, r], i) => {
        const a = 0.3 + i * 0.7;
        rows[i].style.opacity = t >= a ? 1 : 0.25;
        rows[i].classList.toggle("on", i === cur);
        rows[i].querySelector(".nm").textContent = typed(n, t, a, a + 0.3) || "·";
        rows[i].querySelector(".rl").textContent = typed(r, t, a + 0.25, a + 0.65);
      });
      place($, F4312, F4312, 1, cur < 0 ? -1 : ROLES[cur][0]);
      const ys = ROLES.map((_, i) => [0.3 + i * 0.7 - 0.25, 0.3 + i * 0.7, 820, 150 + i * 120]);
      return { cursor: glide(t, [[0, 0, 1080, 700], ...ys, [4.0, 4.6, 1100, 720]]) };
    },
  },
  {
    id: "set", name: "Réglages", dur: 4.4, say: "Jeu court, pressing <span class='a'>haut</span>", clicks: [0.9, 2.1],
    html: `<div class="sp-app">${side}<div class="sp-main">
      <div class="sp-title">Réglages</div>
      ${[["Construction", ["Équilibrée", "P. courtes", "Longues"], 120], ["Approche défensive", ["Basse", "Équilibrée", "Haute"], 340]]
        .map(([lbl, opts, y], g) => `<div class="sp-card" style="${abs(32, y, 836, 190)}"><div class="sp-muted">${lbl}</div>
          ${opts.map((o, j) => `<span class="sp-chip c${g}" style="${abs(28 + j * 262, 96, 240, 56, "justify-content:center")}">${o}</span>`).join("")}</div>`).join("")}
      <div class="sp-row" id="ok" style="${abs(32, 572, 836, null, "justify-content:flex-start")}"><span class="sp-check">${CK}</span><span>Jeu court · pressing haut</span></div></div></div>`,
    draw(t, $) {
      const pick = [t >= 0.9 ? 1 : 0, t >= 2.1 ? 2 : 1];
      [0, 1].forEach((g) => $(".sp-main").querySelectorAll(".c" + g).forEach((c, j) => c.classList.toggle("on", j === pick[g])));
      $("#ok").style.opacity = ease(t, 2.4, 2.7);
      return { cursor: glide(t, [[0, 0, 1080, 700], [0.2, 0.8, 760, 345], [1.3, 2.0, 1010, 565], [2.5, 3.2, 1100, 720]], [0.9, 2.1]) };
    },
  },
  {
    id: "code", name: "Code", dur: 4.6, say: "Copie le <span class='a'>code</span>", clicks: [2.0], keys: [[0.3, 1.5]],
    html: `<div class="sp-app">${side}<div class="sp-main">
      <div class="sp-title">Partager la tactique</div>
      <div class="sp-card on" style="${abs(32, 110, 836, 330)}">
        <div class="sp-muted">XI SPM · 4-3-1-2</div>
        <div id="code" style="margin-top:34px;font-size:76px;letter-spacing:0.04em"></div>
        <div class="sp-btn" id="cp" style="${abs(560, 236, 250)}">Copier</div></div>
      <div class="sp-toast" id="toast"><span class="sp-check">${CK}</span>Colle-le dans le jeu</div></div></div>`,
    draw(t, $) {
      const c = typed(CODE, t, 0.3, 1.5);
      $("#code").innerHTML = c + (t < 1.6 && Math.floor(t * 3) % 2 === 0 ? "<span style='color:var(--accent)'>|</span>" : "");
      const done = t >= 2.0;
      $("#cp").innerHTML = done ? `${CK}Copié !` : "Copier";
      $("#cp").classList.toggle("ghost", done);
      const k = ease(t, 2.2, 2.5);
      $("#toast").style.opacity = k;
      $("#toast").style.transform = `translate(-50%, ${(1 - k) * 30}px)`;
      return { cursor: glide(t, [[0, 0, 1080, 700], [1.0, 1.8, 1015, 380], [2.6, 3.4, 1100, 720]], [2.0]) };
    },
  },
];
