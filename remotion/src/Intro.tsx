import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type IntroProps = {
  title: string;
  subtitle: string;
};

export const Intro: React.FC<IntroProps> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

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
  const fadeOut = interpolate(frame, [durationInFrames - 18, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0b0d12",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "Helvetica Neue, Arial, sans-serif",
        color: "#f4f1ea",
        gap: 32,
        opacity: fadeOut,
      }}
    >
      <div
        style={{
          width: 640,
          height: 12,
          backgroundColor: "#ff5a36",
          transform: `scaleX(${bar})`,
          transformOrigin: "left center",
        }}
      />
      <h1
        style={{
          margin: 0,
          fontSize: 140,
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
    </AbsoluteFill>
  );
};
