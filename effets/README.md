# Bibliothèque d'effets

Éléments du catalogue HyperFrames installés ici (`hyperframes add`), prêts à intégrer dans les montages,
plus une banque maison de bruitages, de filtres couleur et de grain.

## Contenu

| Dossier | Contenu |
|---|---|
| `compositions/` | 191 éléments HyperFrames (blocs et composants), voir la liste plus bas |
| `vendor/` | GSAP 3.14.2 et ses plugins (CustomEase, SplitText, MorphSVG, DrawSVG, MotionPath…), Three.js 0.184, police Inter, en local |
| `sfx/` | 17 bruitages générés (libres de droits) : whoosh, riser, impact, glitch, shutter, pop, clic, ding, buzzer… |
| `luts/` | 6 filtres couleur `.cube` : cinema-teal-orange, or-chaud, froid-net, punchy-gaming, film-desature, noir-et-blanc |
| `overlays/` | grain de film en boucle (vertical et horizontal) |

## Outils

```bash
npm run fx:assets                                       # régénère sfx/, luts/, overlays/
bash scripts/grade.sh in.mp4 out.mp4 or-chaud --grain --vignette   # étalonnage + grain + vignette
bash scripts/transition.sh a.mp4 b.mp4 out.mp4 smoothleft 0.5     # transition FFmpeg entre deux vidéos
cd effets && ../hyperframes/node_modules/.bin/hyperframes add <nom> --no-clipboard   # ajouter un élément du catalogue
cd effets && ../hyperframes/node_modules/.bin/hyperframes catalog --tag transition   # parcourir le catalogue
```

Les éléments chargent GSAP depuis `vendor/` (copie locale). Les éléments 3D chargent Three.js depuis cdn.jsdelivr.net,
autorisé dans l'environnement « Montage ». Après un nouveau `hyperframes add`, relancer la réécriture GSAP locale
(`python3 scripts/fx-localize.py`).

## Recommandations par marque

**Specimen Agency (éditorial premium)** : light-leak, organic-light-leak-overlay, fade-through, focus-blur-resolve,
cross-warp-morph, domain-warp-dissolve, sdf-iris, iris-reveal, grain-overlay, vignette, per-word-rise,
caption-editorial-emphasis, titlecard-calm, logo-brand-close ; LUT `or-chaud` ou `film-desature` ; bruitages doux (whoosh-long, ding).

**Specimen Gaming (dynamique)** : glitch, whip-pan, whip-pan-cut, cinematic-zoom, chromatic-radial-split, swirl-vortex,
thermal-distortion, ridged-burn, shutter-slam, camera-shake, rgb-glitch-text, caption-kinetic-slam, caption-glitch-rgb,
headline-slam, char-slam-explode, beat-freeze-cut, confetti, tiktok-follow ; LUT `punchy-gaming` ou `froid-net` ;
bruitages percutants (impact-boom, glitch, whoosh-court, riser).

Les couleurs et la police des éléments doivent être remplacées par celles de la charte (`brand/<marque>/brand.css`)
avant usage : `npm run brand:check` refuse toute couleur ou police hors charte dans les montages.

Testés au rendu dans cet environnement (WebGL logiciel) : cinematic-zoom, whip-pan, glitch, light-leak, flash-through-white,
sdf-iris, cross-warp-morph, swirl-vortex, ridged-burn, thermal-distortion, transitions-3d.

## Transitions (70)

- **avatar-group-hover** — A distance-falloff avatar group lift with bouncy hover return
- **badge-pop** — A transitions.dev-inspired notification badge pop with elastic scale and count reveal
- **beat-freeze-cut** — A beat-driven speed ramp, freeze-frame hit, and hard-cut sequence for music-led promos and montages.
- **card-resize** — A transitions.dev-inspired card resize primitive that expands a compact card into a detail panel
- **chromatic-aberration-wipe** — A fast slide wipe with RGB channel split on peak frames.
- **chromatic-radial-split** — Shader transition with chromatic aberration radial split
- **cinematic-zoom** — Shader transition with dramatic zoom blur
- **code-slice-hero** — A tiled headline surface flips cell by cell under a sweeping depth field to reveal the rear headline.
- **cross-warp-morph** — Shader transition with cross-warped morphing
- **curtain-reveal** — Two pleated stage curtains gather outward from center, the way real velvet bunches at the tieback, revealing the stage underneath. A static pelmet fra
- **cut-the-curve** — A velocity-matched directional hard cut: the outgoing subject accelerates with power4.in, swaps at peak velocity, and the incoming subject continues i
- **directional-wipe** — A directional scene push that slides one panel over another.
- **domain-warp-dissolve** — Shader transition with fractal noise domain warping
- **editorial-flash-overlay** — Finite neutral-warm light layers for a seek-safe camera-flash cut or social reveal
- **fade-through** — A calm transition primitive that fades one layer out, passes through a wash, and reveals the next layer
- **flash-through-white** — Shader transition with white flash crossfade
- **glitch** — Shader transition with digital glitch artifacts
- **gravitational-lens** — Shader transition with gravitational lensing distortion
- **grid-pixelate-wipe** — Transition effect where the screen dissolves into a grid of squares that fade out with staggered timing — use between scenes
- **halftone-dissolve** — Scene A dissolves into scene B through a growing halftone dot field: accent ink dots pop onto a fixed grid smallest-first, each opens into a window on
- **hw-scribble-transition** — Overlay transition: scribble bands accumulate to cover the frame with a solid backstop, the host cuts beneath, and the scribble clears
- **icon-swap** — A scale-and-blur icon swap primitive for toolbar and action state changes
- **input-feedback** — A transitions.dev-inspired input feedback primitive with shake, clear affordance, and success state
- **iris-reveal** — A circle clip-path opens from an authored origin revealing state B over state A in one confident pass, then holds on B. Classic register dims and desa
- **light-leak** — Shader transition with cinematic light leak overlay
- **match-cut** — A circle accelerates into a hard single-frame scene swap, matches the incoming circle exactly, and continues into a smaller resting pose.
- **menu-morph** — A transitions.dev-inspired hamburger and plus-menu morph primitive for compact action menus
- **micro-transitions** — A transitions.dev-inspired pack of badge, dropdown, modal, tabs, tooltip, and success-check micro transitions
- **mk-clone-wall-transition** — Overlay transition: a tiled word wall covers the frame, inverts via difference blending, and clears — hard-cut the content beneath while covered
- **morph-swap** — Two slotted siblings stacked at one shared center: A holds, then condenses or reshapes into B on a shared 50% 50% transform origin. Condense shrink-fa
- **number-pop-in** — A transitions.dev-inspired digit pop-in with blur, lift, and staggered value reveal
- **ordered-dither-pass** — Bayer-matrix ordered dithering quantizes a slotted scene (rasterized once at mount): the image emerges from pure 2-tone noise to clean, or dissolves t
- **organic-light-leak-overlay** — Finite CSS light-leak overlay for memory beats and motivated transitions
- **page-slide** — A transitions.dev-inspired page slide primitive with outgoing and incoming panels
- **panel-reveal** — A panel reveal primitive with height expansion and content fade
- **paper-collage-reveal** — A scrapbook patchwork of torn paper scraps, each with its own texture and tilt, flutters away in a staggered scatter to reveal the content underneath.
- **parallax-device-dive** — A canonical phone rises into view before the camera pushes through its screen and layered app UI expands to fill the frame.
- **parallax-unzoom** — Reveal transition — focus card scales down from full frame as siblings parallax in to form a grid (reverse of parallax-zoom)
- **parallax-zoom** — Center card scales up to fill the frame while siblings parallax outward — inspired by the eBay Playbook hero transition
- **ridged-burn** — Shader transition with ridged turbulence burn effect
- **ripple-waves** — Shader transition with concentric ripple wave distortion
- **rubber-band-bumper** — An outgoing panel pulls against increasing resistance, holds at tension, then snaps past an edge with overshoot as the incoming panel settles behind i
- **sdf-iris** — Shader transition with signed distance field iris reveal
- **skeleton-reveal** — A skeleton loader transition that pulses, then cross-fades into content
- **success-check** — A success check primitive with ring pop, path draw, and subtle rotate blur
- **swirl-vortex** — Shader transition with swirling vortex distortion
- **tabs-slide-indicator** — A pill indicator transition that slides between active tabs
- **text-match-cut** — One line of text becomes another mid-move: both ride a single 85 % easy-ease curve and hard-swap at the speed peak, as scale, tracking, or a same-dire
- **text-stagger** — A transitions.dev-inspired text stagger primitive with enter, shimmer, and exit-ready words
- **text-state-swap** — A text state swap primitive with outgoing blur and incoming lift
- **thermal-distortion** — Shader transition with heat haze thermal distortion
- **tilt-card** — A transitions.dev-inspired tilt card primitive with depth layers and hover-style parallax
- **torn-paper-rip** — A fibrous paper tear runs across the frame: the torn sheet shows its white paper core along the edge and lifts away on a soft shadow, leaving the next
- **transitions-3d** — Showcase of 3D perspective flip and rotate transitions
- **transitions-blur** — Showcase of blur-based transitions between scenes
- **transitions-cover** — Showcase of cover/uncover slide transitions
- **transitions-destruction** — Showcase of destructive break-apart transitions
- **transitions-dissolve** — Showcase of dissolve and fade transitions
- **transitions-distortion** — Showcase of warp and distortion transitions
- **transitions-grid** — Showcase of grid-based tile transitions
- **transitions-light** — Showcase of light-based glow and flash transitions
- **transitions-mechanical** — Showcase of mechanical shutter and iris transitions
- **transitions-other** — Showcase of miscellaneous creative transitions
- **transitions-push** — Showcase of push and slide transitions
- **transitions-radial** — Showcase of radial wipe and reveal transitions
- **transitions-scale** — Showcase of scale and zoom transitions
- **type-match-cut** — A headline splits vertically around an incoming panel, which grows from the negative space and takes the frame as the words exit through opposite edge
- **whip-pan** — Shader transition simulating a fast camera whip pan
- **whip-pan-cut** — A full-frame whip pan: scene A whips off laterally with capped directional motion blur while scene B enters in the same direction at matched velocity,
- **zoom-through-transition** — A transition that zooms through a focal card into the next scene.

## Sous-titres (17)

- **caption-camera-follow** — One sentence written across a world far larger than the frame. Each word is sized against everything already written, so the block grows geometrically
- **caption-clip-wipe** — Left-to-right clip-path wipe reveal per word
- **caption-editorial-emphasis** — Dual-font system with dramatic size contrast for emphasis words
- **caption-emoji-pop** — Emoji integration with stroked text and horizontal squeeze entrance
- **caption-glitch-rgb** — RGB chromatic aberration with CRT scanline overlay
- **caption-gradient-fill** — Gradient-clipped text with elastic bounce entrance
- **caption-highlight** — Red background sweep behind each active word, TikTok-style
- **caption-kinetic-slam** — Full-screen single-word display with alternating entrance directions
- **caption-matrix-decode** — Character scramble animation before text reveal
- **caption-neon-accent** — Multi-color neon glow accents with wiggle drift animation
- **caption-neon-glow** — Cyan and magenta neon glow with keyword accent colors
- **caption-parallax-layers** — Behind-subject 3D text layering with vertical stretch effect
- **caption-particle-burst** — Keyword words trigger colored particle explosions
- **caption-pill-karaoke** — Pill-shaped container with per-word karaoke color highlight
- **caption-texture** — Flowing texture mask over large uppercase text — ships with 6 textures (lava, marble, metal, wood, concrete, rock), configurable via the texture varia
- **caption-weight-shift** — Elegant font-weight transition between caption lines
- **mk-callout-highlight** — A sentence whose word-by-word emphasis is driven by a single scalar — tween it to sync the highlight with a voiceover

## Bandeaux (lower thirds) (13)

- **lower-third-bild** — News-style lower third with tight-fit text boxes: white headline bar with red drop-shadow, red sub-line with white drop-shadow.
- **lt-accent-underline** — Cardless lower third for footage overlay: name rises, an accent rule draws left-to-right, role fades in; text-shadowed for legibility
- **lt-bold-block** — High-energy podcast lower third: solid dark block wipes in, uppercase name slams up, accent tag pops
- **lt-clean-bar** — Minimal white-card lower third for podcasts/interviews: accent tab, name + role, clip-wipe entrance
- **lt-color-block** — High-energy lower third: bold accent-color block slides in with overshoot, condensed name + mono role
- **lt-dark-card** — Charcoal card lower third for bright footage: name, drawn accent underline, role; slide-up entrance
- **lt-kicker-name** — Cardless lower third with an accent eyebrow/kicker tag, heavy name, and a drawn baseline; for footage
- **lt-mask-reveal** — Cardless lower third: an accent sweep crosses and clip-path-reveals a heavy name, role fades up; for footage
- **lt-neon-border** — Two arcs of light travel the edge of a rounded panel and snap corner to corner, trailing a soft three-layer bloom. A lower third for a name and role.
- **lt-side-rule** — Cardless lower third with a vertical accent bar; condensed display name + mono role, text-shadowed for footage
- **lt-soft-pill** — Rounded white pill lower third for podcasts/interviews: status dot, name + role, scale-pop entrance
- **lt-stack-bars** — Two stacked bars: a dark name bar wipes from the left, an accent role bar wipes from the right
- **news-ticker** — Premium broadcast-style lower-third ticker with live label, headline ribbon, and scrolling news crawl.

## Effets et textures (49)

- **ascii-render-pass** — A slotted scene renders as live ASCII: a canvas samples the source's luminance grid (rasterized once at mount) and draws glyphs from a density ramp ch
- **camcorder-hud** — Responsive REC, battery, editable date placeholder, and timeline-driven counter overlay for creator-camera and camcorder treatments
- **camera-shake** — Procedural handheld, telephoto and rig camera shake for any wrapper: nine measured profiles with per-lens projection, closed-form and seek-safe
- **caption-blend-difference** — Auto-inverting text using mix-blend-mode: difference — flips between white and black per-pixel against the background
- **cinemagraph** — A still photograph with one living region: the frame is frozen while a single feathered window keeps moving - here, steam rising over a cup - drawn fr
- **confetti** — A deterministic celebration burst with seeded particles and gravity.
- **echo-smear** — Distance-adaptive streak — records each element's real trajectory (position, rotation, scale, opacity), then trails time-offset copies behind it in pr
- **falling-lines** — White lines fall down the frame at varied speeds, each fading into a trail. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **filmed-screen** — Your scene, filmed off a screen: perspective, depth of field that follows an element you name, LED sub-pixels and per-shot colour grades. Shots glide
- **focus-swap** — Moves attention between two side-by-side cards as one recedes with scale, blur, and dimming while the other advances to full focus.
- **fractal-noise** — Soft grey fractal noise drifts across the frame like slow clouds. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **gabor-noise** — Grey streaky noise drifts across the frame like a moving fingerprint. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **gooey-split** — A dot splits into a three-dot menu with a gooey metaball neck, spins into a swirl mark under directional shutter motion blur, then breaks back into th
- **grain-field** — A clearly visible accent-tinted dot field drifts over a subtle luminance gradient in an exact ambient loop.
- **grain-overlay** — Animated film grain texture overlay using CSS keyframes — adds warmth and analog character to any composition
- **halftone-field** — A full-bleed halftone light field: a grid of dots whose size and colour track a slow flowing simplex-noise field, so broad bands of light sweep across
- **hw-arrow** — Wobbled draw-on arrow with straight, gentle, and swoop curve poses, a four-way stroke texture matrix (plain/soft/sharp/spray), and a travel-aligned he
- **hw-boil** — Hand-drawn jitter that re-poses every N frames, as seek-safe helpers: pose derives from quantized timeline time through a seeded hash; includes the sh
- **hw-box-label** — Wobbled rounded rectangle draws on — across the authored stroke matrix (plain/soft/sharp/spray) — or drops in and lands with a volume-true contact squ
- **hw-callout-circle** — Wobbled ellipse draws around a target with optional scribble fill and curved connector; the handwritten label pops in WITH momentum and the drawn shap
- **hw-path-text** — Handwriting flowing along any SVG path with a per-character reveal; the path is the only geometry input
- **hw-pipeline** — Wobbled boxes with handwritten labels joined by curved connectors, drawing on in sequence from a node list
- **hw-text-cloud** — Hand-drawn speech bubble with a positionable tail: outline draws on, paper fill fades in, handwritten text types per character; boils
- **hw-title** — Handwritten display text with a scalar-driven word-by-word highlight sweep and a seeded squiggle underline sized to the text; boils
- **hw-write-title** — True glyph write-on: filled Caveat letterforms revealed by baked per-glyph centerline strokes traced in real stroke order with a curvature-adaptive pe
- **ink-bleed-reveal** — Liquid ink blooms through paper under a gooey blur-plus-threshold filter, merges, then contracts as a crisp slotted mark resolves beneath it, with sta
- **light-sweep-pass** — A traveling key light re-shades a slotted scene: a soft diagonal gradient band crosses the frame once while every per-element highlight and shadow shi
- **marble** — Ink-dark veins wind through white in a marbled pattern that slowly shifts. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **mesh-gradient-bg** — A render-safe mesh gradient using animated radial layers.
- **motion-blur** — After Effects-style motion blur — integrates each element over a shutter window (shutter angle, phase, samples per frame) by sampling the GSAP timelin
- **native-notification-pop** — One system-faithful notification banner (iOS or macOS) drops in over any scene on an accurate interruptible spring: fast arrival, soft overshoot, sett
- **plasma** — Deep violet plasma folds and churns across the whole frame. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **ripples** — Concentric rings ripple outward from the centre, white on black. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **sheet-spring-up** — A bottom sheet rushes up from below the frame on a real spring sampled frame by frame from reference footage, overshooting its resting place and settl
- **shimmer-sweep** — Animated light sweep across text or elements using a CSS gradient mask — ideal for AI accents and premium reveals
- **shutter-slam** — One word thrown through six single-property beats under integrated shutter blur — two translate slams, a scale punch, then a full turn about each axis
- **snow** — Seek-safe falling-snow overlay: sparse or dense flakes drift down with size, speed and opacity correlated per flake for depth, radial-masked so the fr
- **spotlight-card** — A card with a scripted cursor spotlight and lit border.
- **starfield** — Seek-safe night-sky overlay: sparse or dense stars in three size tiers that twinkle and drift in two parallax layers, radial-masked to keep the frame
- **svg-mask-reveal** — A soft token-colored sweep reveals media only through an editable SVG wordmark mask.
- **texture-mask-text** — CSS luminance masks that cut holes through letterforms - 66 pre-built texture masks from ambientCG PBR color maps
- **typing-indicator** — The three-dot chat bubble that says someone is writing: it pops in at the thread's edge exactly as messaging apps do, holds while the reply is coming,
- **vignette** — Cinematic radial vignette overlay using a pure-CSS gradient — darkens the edges to pull focus toward the center
- **worley-noise** — A field of drifting cells, light at their centres and dark at their edges. A WebGPU shader from the Shaders library (shaders.com, MIT).
- **yt-camera-move** — Dynamic zoom, slide, and 3D tilt-pan helpers for any wrapper (video, include, card) with cubic-easing defaults and an edge-defocus pulse overlay
- **yt-circle-pointer** — Draw-on annotation ellipse around a target plus a countdown chip that pulses each tick
- **yt-feather-highlight** — Dims the frame except a feathered ellipse; the hole's position and size are CSS variables, so helpers glide the spotlight between targets
- **yt-lcd-background** — Textured paper board: scanlines with slow drift, optional pixel grid, static grain, and display text with a blur-focus entrance and chromatic-fringe t
- **yt-screen-warp** — Grid, scanline, vignette, and sheen overlay plus a 3D-warp wrapper class that makes footage read as if playing on a physical display

## Titres et texte (16)

- **canopy-part-title** — Leaves sweep through the frame and part to reveal the headline.
- **char-slam-explode** — Headline glyphs hold in a deterministic scatter, then reassemble with an overshooting slam and a three-frame landing shake.
- **extruded-logo** — Beveled 3D letters flip up one by one, the word swings so light runs across the bevels, then settles for a readable hold. Chrome, gold or matte.
- **focus-blur-resolve** — A premium focus pull from heavy blur to crisp text, then a soft blur-out exit.
- **glass-hero** — A solid glass object rises in front of a giant headline and keeps turning, so the type bends and splits into colour through it.
- **headline-slam** — A heavyweight headline scales down into frame, lands with a deterministic three-frame shake, holds with subtle drift, and whips upward on exit.
- **logo-brand-close** — A display-scale wordmark cascades letter by letter into a centered lockup, the accent brand period lands last, an optional tagline and wide-tracked mo
- **per-word-rise** — Words or characters rise into place in a controlled blur-to-sharp cascade, settle softly on landing, and hold still until the cut (optional fade or up
- **rgb-glitch-text** — RGB-offset text copies jitter briefly for a controlled glitch window.
- **scan-band** — A diagonal distortion band sweeps once across a clean wordmark, revealing clipped red and cyan offsets only inside the moving band.
- **staggered-fade-up** — Words fade in and slide up one after another with configurable delay.
- **titlecard-calm** — A restrained title card where a mono kicker and generous grotesque headline fade upward, drift almost imperceptibly, and exit cleanly.
- **titlecard-lockup** — The calm breather titlecard: an optional mono kicker fades up, the wordmark settles dead-center with one restrained move, a hairline rule draws left t
- **tracking-in** — A precise letter-spacing reveal for premium headings and interface labels
- **wireframe-portal-title** — A wireframe portal bursts open, the title comes through, then its letters swap into a second phrase.
- **yt-prism-title** — Display title on a transparent root: blur-focus entrance, red/blue fringe that settles then breathes, perspective bow, slow scale drift

## Logos, CTA et réseaux (12)

- **cta-close** — A display-scale action line lands per word and fills the frame with air, one generous CTA capsule pops beneath it with a single overshoot, and the fin
- **cta-lockup** — A canonical closing lockup that reveals an action line, pops in an accent CTA capsule, settles supporting microcopy, and holds with confidence.
- **freeze-frame-dressing** — Timeline-driven paper, tape, and flash dressing for a freeze-frame or background-removed subject
- **instagram-follow** — Animated Instagram follow overlay with profile card and follow button
- **logo-sting** — A wordmark slams into its final scale, fires one accent ring and one white impact frame, then holds completely still.
- **macos-notification** — Animated macOS-style notification banner with app icon and message
- **reddit-post** — Animated Reddit post card overlay with upvotes and comments
- **spotify-card** — Animated Spotify now-playing card with album art and progress bar
- **tiktok-follow** — Animated TikTok follow overlay with profile card and follow button
- **x-post** — Animated X/Twitter post card overlay with engagement metrics
- **yt-comment-card** — Social comments typing on over footage: avatar pop, username and time, per-character typewriter, likes row; image avatars or initials chips
- **yt-lower-third** — Animated YouTube subscribe lower third with avatar and channel info

## Autres (14)

- **beat-accent** — A single music-hit sting: impact flash, micro scale-pulse on the subject, immediate decay.
- **beat-pulse-background** — An accent-derived backdrop pulses its glow intensity and saturation on a deterministic, supplied beat grid.
- **count-up** — A token-native stat counter that eases between values, counting up or down, and lands with a restrained scale pulse.
- **echo-trail** — A moving element renders with N ghosted copies of itself at t minus i times delta, opacity stepped down per ghost; one traversal, echoes collapsing in
- **focus-rack** — Focus shifts once between two cards at different apparent depths through synchronized blur, dimming, scale, and parallax.
- **kinetic-center-build** — Words enter from the right and push the growing phrase left until the final line locks centered.
- **number-wheel** — A rolling digit counter primitive for metrics, prices, counts, and scoreboards
- **particle-text-dissolve** — Text assembles from a seeded particle cloud (or dissolves into it): per-particle targets sampled once from the rendered text bitmap at mount, table-dr
- **pull-back-reveal** — A tight stat detail holds, then one decelerating camera pull-back reveals the headline and supporting cards that recontextualize it.
- **push-in** — A centered headline gains focus through one slow, continuous camera push and a gentle fade out.
- **scramble-reveal** — A deterministic hacker-style text reveal that cycles fixed glyph rows and locks the target string from left to right.
- **slit-scan-reveal** — The frame's rows sample an authored subject at offset times: a canvas painter draws row slices of one pure position function evaluated at t minus offs
- **spring-pop** — A badge pops in from a visible near-rest scale, overshoots full size once, and settles cleanly.
- **text-shimmer** — A static headline receives one clean specular gradient sweep through its glyphs, then returns to its ordinary text color.
