/* ==========================================================================
   app-demo.js — fenêtre « html-demo » pilotée par la timeline HyperFrames.
   Le moteur d'origine (step-window.js, MengTo, MIT) a sa propre horloge en temps réel ;
   ici on la met en pause et on appelle seek(t) à chaque image : rendu exact, déterministe.

   AppDemo.bind(tl, el, { steps, tabs, label, start }) :
     steps : [{ id, name, dur, html, draw(t, $) → { cursor:{x,y,press,hide} } }]  (API d'origine)
     start : instant (s) où la fenêtre commence dans la vidéo.
   Renvoie { total, ctl, sound(fn) } ; sound(fn) appelle fn(tempsAbsolu, type) pour chaque clic
   déclaré dans steps[i].clicks (secondes relatives à l'étape) → bruitages.
   ========================================================================== */
(function () {
  const D = window.HTMLDemo;
  function bind(tl, el, { steps, tabs = [], label = "Démo", start = 0, bar = true }) {
    const ctl = D.mount(el, { steps, tabs, label, bar });
    ctl.pause();
    const total = steps.reduce((s, x) => s + x.dur, 0);
    const clock = { t: 0 };
    tl.fromTo(clock, { t: 0 }, { t: total, duration: total, ease: "none", immediateRender: false,
      onUpdate: () => ctl.seek(clock.t) }, start);
    ctl.seek(0);
    return {
      total, ctl,
      sound(fn) {
        let acc = start;
        steps.forEach((s) => { (s.clicks || []).forEach((c) => fn(acc + c, "clic")); acc += s.dur; });
      },
    };
  }
  window.AppDemo = { bind, ...D };
})();
