import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import type { Episode } from '../story/schema';
import type { Segment } from '../timeline/build';
import type { CharId } from '../story/registry';
import { Background } from '../scene/Backgrounds';
import { Puppet } from '../puppet/Puppet';
import { mouthFor, activeLine } from './anim';

/** Açılış kancası: konuşanın yakın planı + krem bantta tırnak içinde replik. Kapak karesi de buradan alınır. */
export const Hook: React.FC<{ ep: Episode; seg: Segment; fps: number }> = ({ ep, seg, fps }) => {
  const f = useCurrentFrame();
  const abs = f + seg.from;
  const kim = ep.kanca.kim;
  const scene = ep.sahneler.find((s) => s.karakterler.some((c) => c.id === kim)) ?? ep.sahneler[0];
  const zoom = interpolate(f, [0, seg.dur], [1.0, 1.08]);
  const active = activeLine(seg.lines, abs);
  const opacity = interpolate(f, [seg.dur - 8, seg.dur], [1, 0], { extrapolateLeft: 'clamp' });
  const H = 2000;
  return (
    <AbsoluteFill style={{ opacity }}>
      <AbsoluteFill style={{ filter: `blur(10px) brightness(0.7)${scene.gecmis ? ' sepia(0.8)' : ''}`, transform: 'scale(1.1)' }}>
        <Background mekan={scene.mekan} gece={scene.gece} />
      </AbsoluteFill>
      {kim !== 'anlatici' && (
        <AbsoluteFill style={{ transform: `scale(${zoom})`, transformOrigin: '540px 600px' }}>
          <div style={{ position: 'absolute', left: 540 - (H * 400) / 1120 / 2, top: 160 }}>
            <Puppet id={kim as CharId} ifade={ep.kanca.ifade ?? 'ofkeli'} poz={ep.kanca.poz ?? 'durus'} mouthOpen={mouthFor(kim, active, abs, fps)} frame={abs} height={H} />
          </div>
        </AbsoluteFill>
      )}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 1330, minHeight: 300, background: '#f4ead5', borderTop: '8px solid #7a1f24', borderBottom: '8px solid #7a1f24', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '30px 70px', boxShadow: '0 10px 40px rgba(0,0,0,0.5)' }}>
        <div style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontStyle: 'italic', fontSize: 66, color: '#2b1d14', textAlign: 'center', lineHeight: 1.2 }}>
          “{ep.kanca.metin}”
        </div>
      </div>
    </AbsoluteFill>
  );
};
