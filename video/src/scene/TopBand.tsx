import React from 'react';
import { trUpper } from '../story/registry';

export const TopBand: React.FC<{ bolum: number }> = ({ bolum }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 230, background: 'linear-gradient(#1a0c0c 0%, rgba(26,12,12,0.85) 70%, rgba(26,12,12,0) 100%)', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 36 }}>
    <div style={{ fontFamily: 'Cinzel, serif', fontWeight: 700, fontSize: 78, letterSpacing: 6, color: '#e9c46a', textShadow: '0 4px 0 #5a141a' }}>
      {trUpper('lale ile kan')}
    </div>
    <div style={{ marginTop: 4, fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 40, color: '#fff', background: '#7a1f24', borderRadius: 30, padding: '2px 30px', border: '3px solid #e9c46a' }}>
      {bolum}. {trUpper('bölüm')}
    </div>
  </div>
);
