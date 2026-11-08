/* ==========================================================================
   motion3d.js — briques de motion design 3D (Three.js) pour HyperFrames
   Référence : references/motion-3 (pub verticale : téléphone 3D, objets 3D, halos, logo lumineux).

   Règles de rendu déterministe (comme les blocs 3D du catalogue) :
     - jamais de requestAnimationFrame : on rend dans tl.eventCallback("onUpdate") ;
     - toutes les valeurs animées vivent dans des objets « état » animés par GSAP ;
     - la timeline est enregistrée sur window.__timelines APRÈS la construction de la scène.
   Couleurs : lues dans les variables CSS de la charte (--accent, --black, --ivory…).
   ========================================================================== */
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

export { THREE };

/* couleur de charte (variable CSS) → THREE.Color */
export const brandColor = (name, fallback = "#ffffff") => {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback;
  return new THREE.Color(v);
};

/* Scène : rendu, caméra, éclairage d'environnement, bloom optionnel. */
export function createStage(canvas, { width = 1080, height = 1920, fov = 35, bloom = 0.45, threshold = 0.82, exposure = 0.9, background = null } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: background === null, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;
  const scene = new THREE.Scene();
  if (background) scene.background = background;
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(fov, width / height, 0.1, 100);
  camera.position.set(0, 0, 10);
  const key = new THREE.DirectionalLight(0xffffff, 1.4); key.position.set(3, 5, 6); scene.add(key);
  let composer = null;
  if (bloom > 0) {
    composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    composer.addPass(new UnrealBloomPass(new THREE.Vector2(width, height), bloom, 0.5, threshold));   // seuil élevé : seuls les éléments lumineux brillent
    composer.addPass(new OutputPass());
  }
  const render = () => (composer ? composer.render() : renderer.render(scene, camera));
  return { renderer, scene, camera, composer, render };
}

/* Texture dessinée sur un canvas 2D, redessinée à chaque image (interfaces animées sur l'écran). */
export function canvasScreen(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const ctx = c.getContext("2d");
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  return { canvas: c, texture: tex, update: (t) => { draw(ctx, w, h, t); tex.needsUpdate = true; } };
}

/* Téléphone 3D : coque arrondie, verre, écran (texture image, canvas ou couleur). */
export function phone({ screen, color = brandColor("--black", "#0b0b0d"), rim = brandColor("--accent", "#e3b25c"), w = 2.2, h = 4.6 } = {}) {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new RoundedBoxGeometry(w, h, 0.26, 8, 0.3),
    new THREE.MeshPhysicalMaterial({ color, metalness: 0.6, roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.15 }));
  g.add(body);
  const frame = new THREE.Mesh(new RoundedBoxGeometry(w + 0.04, h + 0.04, 0.2, 8, 0.32),
    new THREE.MeshStandardMaterial({ color: rim, metalness: 1, roughness: 0.3 }));
  frame.position.z = -0.04; g.add(frame);
  const scrMat = new THREE.MeshBasicMaterial({ map: screen?.texture || screen || null, color: screen ? 0xd8d8d8 : 0x111111 });
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(w - 0.16, h - 0.16), scrMat);
  scr.position.z = 0.135; g.add(scr);
  const island = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.17, 0.02, 4, 0.08), new THREE.MeshBasicMaterial({ color: 0x000000 }));
  island.position.set(0, h / 2 - 0.26, 0.15); g.add(island);
  g.userData.screen = scr;
  return g;
}

/* Carte flottante (panneau d'interface) avec texture. */
export function card({ texture, w = 2.4, h = 1.4, radius = 0.12, glow = brandColor("--accent", "#e3b25c") } = {}) {
  const g = new THREE.Group();
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, 0.05, 6, radius),
    new THREE.MeshStandardMaterial({ color: 0x111113, metalness: 0.2, roughness: 0.5 }));
  g.add(m);
  if (texture) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(w - 0.06, h - 0.06), new THREE.MeshBasicMaterial({ map: texture, toneMapped: false, transparent: true }));
    p.position.z = 0.03; g.add(p);
  }
  const edge = new THREE.Mesh(new RoundedBoxGeometry(w + 0.03, h + 0.03, 0.03, 6, radius), new THREE.MeshBasicMaterial({ color: glow }));
  edge.position.z = -0.02; g.add(edge);
  return g;
}

/* Bâtiment isométrique procédural (locaux, boutique, agence). */
export function isoBuilding({ wall = brandColor("--ivory", "#f7f1e3"), accent = brandColor("--accent", "#e3b25c"), ground = brandColor("--black", "#0b0b0d"), floors = 2 } = {}) {
  const g = new THREE.Group();
  const std = (c, r = 0.7, m = 0) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m });
  const base = new THREE.Mesh(new RoundedBoxGeometry(6, 0.2, 4.4, 4, 0.08), std(ground.clone().offsetHSL(0, 0, 0.08)));
  base.position.y = -0.1; g.add(base);
  const bh = floors * 1.1;
  const body = new THREE.Mesh(new THREE.BoxGeometry(3.6, bh, 2.4), std(wall.clone().multiplyScalar(0.55), 0.85)); body.position.y = bh / 2; g.add(body);
  const roof = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.15, 2.6), std(ground, 0.5, 0.3)); roof.position.y = bh + 0.07; g.add(roof);
  const band = new THREE.Mesh(new THREE.BoxGeometry(3.62, 0.18, 2.42), new THREE.MeshStandardMaterial({ color: accent, emissive: accent, emissiveIntensity: 0.6 }));
  band.position.y = bh - 0.25; g.add(band);
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x223040, metalness: 0.1, roughness: 0.05, transmission: 0.2, clearcoat: 1 });
  for (let f = 0; f < floors; f++) for (let i = 0; i < 4; i++) {
    const win = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.55, 0.04), glass);
    win.position.set(-1.25 + i * 0.83, 0.55 + f * 1.1, 1.22); g.add(win);
  }
  for (let i = 0; i < 6; i++) {           // places de parking
    const l = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.01, 0.9), new THREE.MeshBasicMaterial({ color: wall }));
    l.position.set(-2.5 + i * 1.0, 0.01, 1.9); g.add(l);
  }
  g.userData.band = band;
  return g;
}

/* Orbe lumineux (sprite additif) : intro « halo », points de lumière. */
export function glowOrb({ color = brandColor("--accent", "#e3b25c"), size = 2 } = {}) {
  const c = document.createElement("canvas"); c.width = c.height = 256;
  const x = c.getContext("2d"); const grd = x.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, "rgba(255,255,255,1)"); grd.addColorStop(0.25, `rgba(${(color.r * 255) | 0},${(color.g * 255) | 0},${(color.b * 255) | 0},0.9)`);
  grd.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = grd; x.fillRect(0, 0, 256, 256);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
  s.scale.setScalar(size); return s;
}

/* Logo plat (PNG transparent) avec halo émissif — pour les révélations de logo. */
export async function logoPlane(url, { height = 2.2 } = {}) {
  const tex = await new THREE.TextureLoader().loadAsync(url); tex.colorSpace = THREE.SRGBColorSpace;
  const r = tex.image.width / tex.image.height;
  return new THREE.Mesh(new THREE.PlaneGeometry(height * r, height), new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false }));
}

/* Modèle 3D fourni par l'utilisateur (.glb / .gltf). */
export async function loadModel(url) {
  const gltf = await new GLTFLoader().loadAsync(url); return gltf.scene;
}

/* Image → texture (captures d'écran, photos). */
export async function imageTexture(url) {
  const t = await new THREE.TextureLoader().loadAsync(url); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}

/* Branche le rendu sur la timeline (aucune boucle libre) et l'enregistre une fois prête. */
export function bindTimeline(tl, id, stage, onFrame) {
  const render = () => { if (onFrame) onFrame(tl.time()); stage.render(); };
  tl.eventCallback("onUpdate", render);
  render();
  window.__timelines = window.__timelines || {};
  window.__timelines[id] = tl;
}
