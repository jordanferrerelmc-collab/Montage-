import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { brand, loadBrandFont } from "./brand";

loadBrandFont();

export type IntroProps = {
  title: string;
  subtitle: string;
};

// Intro aux couleurs et à la police de la marque choisie (BRAND=… npm run remotion:brand).
export const Intro: React.FC<IntroProps> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const vertical = height > width;

  const titleScale = spring({ frame, fps, config: { damping: 200 } });
  const bar = interpolate(frame, [6, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const subtitleIn = interpolate(frame, [33, 54], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const logoIn = interpolate(frame, [50, 70], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [durationInFrames - 18, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: brand.bg,
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        fontFamily: brand.font,
        color: brand.text,
        gap: 32,
        padding: vertical ? "0 90px" : 0,
        opacity: fadeOut,
      }}
    >
      <div
        style={{
          width: vertical ? 420 : 640,
          height: 12,
          backgroundColor: brand.accent,
          transform: `scaleX(${bar})`,
          transformOrigin: "center",
        }}
      />
      <h1
        style={{
          margin: 0,
          fontSize: vertical ? 120 : 140,
          fontWeight: 700,
          letterSpacing: "-0.04em",
          lineHeight: 1,
          transform: `scale(${0.92 + 0.08 * titleScale})`,
        }}
      >
        {title}
      </h1>
      <p
        style={{
          margin: 0,
          fontSize: 44,
          opacity: 0.75 * subtitleIn,
          transform: `translateY(${(1 - subtitleIn) * 30}px)`,
        }}
      >
        {subtitle}
      </p>
      <Img src={brand.logo} style={{ height: vertical ? 120 : 90, marginTop: 24, opacity: logoIn }} />
    </AbsoluteFill>
  );
};
