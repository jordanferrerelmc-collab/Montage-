import { Composition } from "remotion";
import { Intro, type IntroProps } from "./Intro";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Intro"
      component={Intro}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ title: "Montage", subtitle: "Remotion · React → MP4" } satisfies IntroProps}
    />
  );
};
