#!/usr/bin/env node
// Vérifie qu'aucun texte ni aucune bulle n'approche les bords de l'écran (demande de l'utilisateur, 19/11/2026).
// Ouvre la composition dans Chromium, rejoue la timeline image par image (toutes les 0,1 s, zooms compris), affiche/cache
// les clips selon data-start / data-duration, et mesure la position RÉELLE des glyphes (Range) et des bulles.
// Marges : gauche/droite = colonne de la charte (Agency 90 px, Gaming 110 px), haut 90 px, bas 230 px (interface TikTok/IG).
// Usage : node scripts/check-marges.mjs projets/<nom>/montage/index.html [--pas 0.1]
import path from 'node:path';
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');   // Playwright préinstallé (résolu via NODE_PATH)

const file = path.resolve(process.argv[2] || '');
const step = Number((process.argv.indexOf('--pas') > -1 && process.argv[process.argv.indexOf('--pas') + 1]) || 0.1);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + file);
await page.waitForFunction(() => !!(window.__timelines && window.__timelines.main), null, { timeout: 30000, polling: 200 });
await page.evaluate(() => document.fonts && document.fonts.ready);

const res = await page.evaluate(async (step) => {
  const brand = document.querySelector('meta[name="brand"]')?.content || 'specimen-agency';
  const side = brand === 'specimen-gaming' ? 110 : 90, TOP = 90, BOTTOM = 1920 - 230, W = 1080;
  const tl = window.__timelines.main, dur = tl.duration();
  const clips = [...document.querySelectorAll('[data-start][data-duration]')].filter((e) => e.id !== 'root' && !e.hasAttribute('data-composition-id'));
  document.querySelectorAll('video, audio').forEach((m) => { m.pause && m.pause(); });
  const vis = (el) => {                                      // opacité effective et affichage (ancêtres compris)
    let o = 1;
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden') return 0;
      // transition zoom en cours (flou plein cadre ≥ 3 px) : image de passage, texte illisible par choix → ignorée
      const bl = /blur\(([\d.]+)px\)/.exec(cs.filter);
      if (bl && Number(bl[1]) >= 3) return 0;
      o *= Number(cs.opacity);
    }
    return o;
  };
  const inEnd = (el) => !!el.closest('#endcard');            // écran de fin de la charte : mise en page fixe validée
  const bad = new Map();
  const note = (t, what, r) => {
    const why = [];
    if (r.left < side - 0.5) why.push(`gauche ${Math.round(r.left)} px`);
    if (r.right > W - side + 0.5) why.push(`droite ${Math.round(W - r.right)} px du bord`);
    if (r.top < TOP - 0.5) why.push(`haut ${Math.round(r.top)} px`);
    if (r.bottom > BOTTOM + 0.5) why.push(`bas ${Math.round(1920 - r.bottom)} px du bord`);
    if (!why.length) return;
    const k = what + ' | ' + why.map((w) => w.replace(/\d+ px.*/, '')).join(',');
    if (!bad.has(k)) bad.set(k, { what, why: why.join(', '), from: t, to: t }); else bad.get(k).to = t;
  };
  for (let t = 0; t <= dur + 1e-6; t += step) {
    for (const c of clips) {
      const s = Number(c.dataset.start), d = Number(c.dataset.duration);
      c.style.display = t >= s && t < s + d ? '' : 'none';
    }
    tl.seek(t, false);
    // 1. glyphes de chaque texte visible
    const walker = document.createTreeWalker(document.getElementById('root') || document.body, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!n.textContent.trim() || inEnd(n.parentElement) || vis(n.parentElement) < 0.15) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) if (r.width > 1 && r.height > 1) note(+t.toFixed(2), `texte « ${n.textContent.trim().slice(0, 40)} »`, r);
    }
    // 2. bulles, cartes, pastilles (le fond aussi doit rester dans la zone)
    for (const el of document.querySelectorAll('.glass, .note, .card, .pill, .pill-cta, .cap, .badge')) {
      if (inEnd(el) || vis(el) < 0.15) continue;
      const r = el.getBoundingClientRect();
      if (r.width > 1 && r.height > 1) note(+t.toFixed(2), `bulle #${el.id || el.className.split(' ').join('.')}`, r);
    }
  }
  return { brand, side, items: [...bad.values()] };
}, step);
await browser.close();

if (!res.items.length) {
  console.log(`✅ Marges respectées (${res.brand} : ${res.side} px sur les côtés, 90 px en haut, 230 px en bas).`);
} else {
  for (const b of res.items) console.log(`✗ ${b.from.toFixed(2)}-${b.to.toFixed(2)} s  ${b.what} : ${b.why}`);
  console.log(`\n${res.items.length} élément(s) trop près d'un bord (${res.brand} : ${res.side} px sur les côtés, 90 px en haut, 230 px en bas).`);
  process.exitCode = 1;
}
