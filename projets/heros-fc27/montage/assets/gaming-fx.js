/* ==========================================================================
   gaming-fx.js — animations du style « gaming premium » (réf. references/gaming-style)
   Fonctions déterministes (GSAP, timeline en pause pilotée par HyperFrames).
   Toutes prennent la timeline `tl`, un sélecteur et un temps `t` (secondes).
   ========================================================================== */
(function () {
  const fx = {};

  /* Texte qui sort du flou (défocalisation → net), léger glissé vertical. */
  fx.blurIn = (tl, sel, t, o = {}) => {
    tl.fromTo(sel, { opacity: 0, filter: `blur(${o.blur ?? 18}px)`, y: o.y ?? 24, scale: o.scale ?? 1.04 },
      { opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: o.d ?? 0.45, ease: "power3.out", stagger: o.stagger ?? 0, immediateRender: true }, t);
  };

  /* Sortie floue (fondu + flou), utilisée pour les transitions entre étapes. */
  fx.blurOut = (tl, sel, t, o = {}) => {
    tl.to(sel, { opacity: 0, filter: `blur(${o.blur ?? 16}px)`, y: o.y ?? -10, duration: o.d ?? 0.3, ease: "power2.in" }, t);
  };

  /* Glissé latéral avec flou de mouvement (encadrés de stats, badges, notes). */
  fx.slideBlur = (tl, sel, t, o = {}) => {
    tl.fromTo(sel, { opacity: 0, x: o.x ?? -60, filter: "blur(10px)" },
      { opacity: 1, x: 0, filter: "blur(0px)", duration: o.d ?? 0.4, ease: "power3.out", stagger: o.stagger ?? 0.08, immediateRender: true }, t);
  };

  /* Anneau d'onde de choc qui s'étend et s'efface. */
  fx.shockwave = (tl, sel, t, o = {}) => {
    tl.fromTo(sel, { scale: 0.55, opacity: 0.9 }, { scale: o.to ?? 1.6, opacity: 0, duration: o.d ?? 0.8, ease: "power2.out", immediateRender: false }, t);
  };

  /* Révélation mystère : la silhouette « ? » se fond, la carte apparaît avec halo + onde de choc. */
  fx.mysteryReveal = (tl, mystery, card, ring, t, o = {}) => {
    tl.to(mystery, { opacity: 0, scale: 1.08, filter: "blur(12px)", duration: 0.22, ease: "power2.in" }, t - 0.05);
    tl.fromTo(card, { opacity: 0, scale: 0.86, filter: "blur(14px) brightness(2)" },
      { opacity: 1, scale: 1, filter: "blur(0px) brightness(1)", duration: 0.45, ease: "back.out(1.6)", immediateRender: true }, t);
    if (ring) fx.shockwave(tl, ring, t + 0.05, o);
  };

  /* Pulsation douce du halo (respiration) sur une durée. */
  fx.breathe = (tl, sel, t, dur, o = {}) => {
    const n = Math.max(1, Math.floor(dur / (o.period ?? 1.6)));
    tl.fromTo(sel, { opacity: o.min ?? 0.45 }, { opacity: o.max ?? 0.85, duration: (o.period ?? 1.6) / 2, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut", immediateRender: false }, t);
  };

  /* Compteur qui défile (pastille de prix, stat…). Déterministe : interpolation pilotée par la timeline. */
  fx.countUp = (tl, sel, from, to, t, d = 0.8, fmt = (v) => Math.round(v).toLocaleString("fr-FR")) => {
    const el = document.querySelector(sel);
    const state = { v: from };
    tl.fromTo(state, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false,
      onUpdate: () => { if (el) el.textContent = fmt(state.v); } }, t);
  };   /* le HTML de l'élément doit contenir la valeur de départ */

  /* Case de la barre de progression qui s'allume. */
  fx.trackerFill = (tl, sel, t) => {
    tl.to(sel, { backgroundColor: "var(--accent)", borderColor: "var(--accent)", duration: 0.2 }, t);
    tl.fromTo(sel, { scale: 1.35 }, { scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t);
  };

  /* Grille d'appel à l'action 2×2 : apparition en cascade, puis sortie floue. */
  fx.ctaGrid = (tl, sel, t, out) => {
    tl.fromTo(`${sel} .cta-btn`, { opacity: 0, scale: 0.8, filter: "blur(8px)" },
      { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "back.out(2)", stagger: 0.12, immediateRender: true }, t);
    if (out !== undefined) fx.blurOut(tl, sel, out);
  };

  window.GamingFX = fx;
})();
