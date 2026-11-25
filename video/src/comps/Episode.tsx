import React from 'react';
import { AbsoluteFill, Audio, Easing, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';
import type { Episode, Scene } from '../story/schema';
import type { Segment, TimedLine, Timeline } from '../timeline/build';
import { ISIMLER, trUpper, type CharId, type SpeakerId } from '../story/registry';
import { Puppet } from '../puppet/Puppet';
import { Background, FLOOR_Y } from '../scene/Backgrounds';
import { TopBand } from '../scene/TopBand';
import { Subtitle } from '../scene/Subtitle';
import { alignWords } from '../scene/subtitleLayout';
import { Hook } from './Hook';
import { EndCard } from './EndCard';
import { activeLine, mouthFor } from './anim';

export type EpisodeProps = { episode: Episode; timeline: Timeline };

const PUPPET_H = 1400;
const FEET = 0.987; // ayak tabanının kukla yüksekliğine oranı

export const audioSrc = (file: string) => staticFile(`audio/${file.split('/').pop()}`);

const LineSubtitle: React.FC<{ tl: TimedLine; abs: number; fps: number }> = ({ tl, abs, fps }) => {
  const ms = ((abs - tl.from) / fps) * 1000;
  const words = alignWords(tl.line.metin, tl.audio.words, tl.audio.durationMs);
  return <Subtitle words={words} currentMs={ms} speaker={ISIMLER[tl.line.kim] ? trUpper(ISIMLER[tl.line.kim]) : undefined} />;
};

const SceneView: React.FC<{ scene: Scene; seg: Segment; fps: number; focusAll?: boolean; title?: { bolum: number; baslik: string } }> = ({ scene, seg, fps, focusAll, title }) => {
  const f = useCurrentFrame();
  const abs = f + seg.from;
  const active = activeLine(seg.lines, abs);
  const speaker = active ? scene.karakterler.find((c) => c.id === active.line.kim) : undefined;

  const base = interpolate(f, [0, seg.dur], [1, 1.06]);
  let push = 0;
  if (focusAll) push = interpolate(f, [0, 15], [0, 1], { extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  else if (active && speaker && active.dur > 75) {
    const r = abs - active.from;
    push = interpolate(r, [0, 14, active.dur - 10, active.dur], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  }
  const zoom = base * (1 + (focusAll ? 0.3 : 0.15) * push);
  const originX = speaker ? speaker.x * 1080 : 540;
  const opacity = interpolate(f, [0, 10, seg.dur - 12, seg.dur], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})`, transformOrigin: `${originX}px 900px`, filter: scene.gecmis ? 'sepia(0.85) contrast(0.95) brightness(0.95)' : undefined }}>
        <Background mekan={scene.mekan} gece={scene.gece} />
        {scene.karakterler.map((c) => {
          const isSpeaker = active?.line.kim === c.id;
          const ifade = (isSpeaker ? active?.line.ifade : undefined) ?? c.ifade ?? 'normal';
          const poz = isSpeaker ? active?.line.poz : undefined;
          const width = (PUPPET_H * 400) / 1120;
          return (
            <div key={c.id} style={{ position: 'absolute', left: c.x * 1080 - width / 2, top: FLOOR_Y - FEET * PUPPET_H }}>
              <Puppet id={c.id as CharId} ifade={ifade} poz={poz} yon={c.yon ?? (c.x > 0.5 ? 'sol' : 'sag')} mouthOpen={mouthFor(c.id, active, abs, fps)} frame={abs} height={PUPPET_H} />
            </div>
          );
        })}
        {scene.gecmis && <AbsoluteFill style={{ boxShadow: 'inset 0 0 220px 80px rgba(40,20,5,0.8)' }} />}
      </AbsoluteFill>
      {active && <LineSubtitle tl={active} abs={abs} fps={fps} />}
      {title && f < 50 && (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', background: `rgba(10,4,4,${interpolate(f, [30, 50], [0.75, 0], { extrapolateLeft: 'clamp' })})`, opacity: interpolate(f, [30, 50], [1, 0], { extrapolateLeft: 'clamp' }) }}>
          <div style={{ fontFamily: 'Cinzel, serif', fontWeight: 700, fontSize: 120, color: '#e9c46a', textAlign: 'center', lineHeight: 1.1 }}>{trUpper('lale ile kan')}</div>
          <div style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 52, color: '#fff', marginTop: 24, textAlign: 'center', padding: '0 60px' }}>
            {title.bolum}. {trUpper('bölüm')}: {title.baslik}
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

const SegmentView: React.FC<{ ep: Episode; seg: Segment; fps: number }> = ({ ep, seg, fps }) => {
  switch (seg.kind) {
    case 'kanca':
      return <Hook ep={ep} seg={seg} fps={fps} />;
    case 'sahne':
      return <SceneView scene={ep.sahneler[seg.sceneIndex!]} seg={seg} fps={fps} title={seg.sceneIndex === 0 ? { bolum: ep.bolum, baslik: ep.baslik } : undefined} />;
    case 'son': {
      const last = ep.sahneler[seg.sceneIndex!];
      const kim = ep.son.kim;
      const scene: Scene = kim === 'anlatici' || last.karakterler.some((c) => c.id === kim)
        ? last
        : { ...last, karakterler: [...last.karakterler, { id: kim, x: 0.5 }] };
      return <SceneView scene={scene} seg={seg} fps={fps} focusAll />;
    }
    case 'devam':
      return <EndCard bolum={ep.bolum} />;
  }
};

export const EpisodeComp: React.FC<EpisodeProps> = ({ episode, timeline }) => {
  const lines = timeline.segments.flatMap((s) => s.lines);
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {timeline.segments.map((seg, i) => (
        <Sequence key={i} from={seg.from} durationInFrames={seg.dur} layout="none">
          <SegmentView ep={episode} seg={seg} fps={timeline.fps} />
        </Sequence>
      ))}
      {lines.map((tl, i) => (
        <Sequence key={'a' + i} from={tl.from} durationInFrames={tl.dur + 10} layout="none">
          <Audio src={audioSrc(tl.audio.file)} />
        </Sequence>
      ))}
      <TopBand bolum={episode.bolum} />
    </AbsoluteFill>
  );
};
