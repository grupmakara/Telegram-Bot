import React from 'react';
import { AbsoluteFill, Composition } from 'remotion';

const Smoke: React.FC = () => (
  <AbsoluteFill style={{ background: '#2b1a12', justifyContent: 'center', alignItems: 'center' }}>
    <div style={{ color: '#f3d27a', fontSize: 110, fontFamily: 'serif' }}>LALE İLE KAN</div>
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Smoke" component={Smoke} width={1080} height={1920} fps={30} durationInFrames={60} />
  </>
);
