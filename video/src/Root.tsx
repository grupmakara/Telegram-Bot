import React from 'react';
import { AbsoluteFill, Composition, Still } from 'remotion';
import './scene/fonts';
import { CharacterSheet } from './comps/CharacterSheet';
import { EpisodeComp, type EpisodeProps } from './comps/Episode';

const Smoke: React.FC = () => (
  <AbsoluteFill style={{ background: '#2b1a12', justifyContent: 'center', alignItems: 'center' }}>
    <div style={{ color: '#f3d27a', fontSize: 110, fontFamily: 'serif' }}>LALE İLE KAN</div>
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Smoke" component={Smoke} width={1080} height={1920} fps={30} durationInFrames={60} />
    <Composition
      id="Episode"
      component={EpisodeComp}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={60}
      defaultProps={{ episode: { bolum: 0, baslik: '', kanca: { kim: 'anlatici', metin: '-' }, sahneler: [], son: { kim: 'anlatici', metin: '-' }, aciklama: '', etiketler: [] }, timeline: { durationInFrames: 60, fps: 30, segments: [{ kind: 'devam', from: 0, dur: 60, lines: [] }] } } as EpisodeProps}
      calculateMetadata={({ props }) => ({ durationInFrames: props.timeline.durationInFrames })}
    />
    <Still id="CharacterSheet" component={CharacterSheet} width={1080} height={1920} />
  </>
);
