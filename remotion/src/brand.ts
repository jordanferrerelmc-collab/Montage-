// Charte de la marque pour Remotion : lue depuis public/brand/ (copiée par `npm run remotion:brand`).
// N'utiliser que ces valeurs dans les compositions : aucune couleur ni police en dur.
import { continueRender, delayRender, staticFile } from "remotion";
import spec from "../public/brand/brand.json";

type Colors = Record<string, string>;
const c = spec.colors as unknown as Colors;
const isGaming = (spec as { id?: string }).id === "specimen-gaming";

export const brand = {
  id: (spec as { id?: string }).id ?? "specimen-agency",
  name: spec.name,
  colors: c,
  font: `"${spec.fonts.family}", sans-serif`,
  logo: staticFile("brand/logo.png"),
  // Rôles communs aux deux chartes (mêmes noms que les alias de brand.css).
  accent: isGaming ? c.red : c.gold,
  accentLight: isGaming ? c.red_light : (c.gold_light ?? c.gold),
  bg: isGaming ? c.charcoal_deep : c.black,
  panel: isGaming ? c.charcoal : c.ink_black,
  text: isGaming ? c.white : (c.ivory ?? c.white),
};

// Charge TeX Gyre Heros (« Specimen Heros ») avant le rendu de la première image.
let loaded = false;
export const loadBrandFont = () => {
  if (loaded || typeof document === "undefined") return;
  loaded = true;
  const handle = delayRender("Police de la charte");
  const faces = [
    new FontFace(spec.fonts.family, `url(${staticFile("brand/fonts/texgyreheros-regular.otf")})`, { weight: "400" }),
    new FontFace(spec.fonts.family, `url(${staticFile("brand/fonts/texgyreheros-bold.otf")})`, { weight: "700" }),
  ];
  Promise.all(faces.map((f) => f.load()))
    .then((fs) => fs.forEach((f) => document.fonts.add(f)))
    .finally(() => continueRender(handle));
};
