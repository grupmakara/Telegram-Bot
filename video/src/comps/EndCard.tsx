import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { trUpper } from '../story/registry';

export const EndCard: React.FC<{ bolum: number }> = ({ bolum }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 12], [0, 1], { extrapolateRight: 'clamp' });
  const s = interpolate(f, [0, 60], [0.92, 1.02]);
  return (
    <AbsoluteFill style={{ background: 'radial-gradient(circle at 50% 45%, #4a1016 0%, #12070a 75%)', justifyContent: 'center', alignItems: 'center', opacity: o }}>
      <div style={{ transform: `scale(${s})`, textAlign: 'center' }}>
        <div style={{ fontFamily: 'Cinzel, serif', fontWeight: 700, fontSize: 96, color: '#e9c46a' }}>{trUpper('devamı')}</div>
        <div style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 84, color: '#fff', marginTop: 10 }}>
          {bolum + 1}. {trUpper('bölümde')}
        </div>
        <div style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 44, color: '#e9c46a', marginTop: 60, border: '4px solid #e9c46a', borderRadius: 40, padding: '10px 40px' }}>
          Kaçırmamak için takip et
        </div>
      </div>
    </AbsoluteFill>
  );
};
