import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Puppet } from '../puppet/Puppet';
import { CHAR_IDS, ISIMLER, trUpper, type Ifade, type Poz } from '../story/registry';

const DEMO: Partial<Record<string, { ifade: Ifade; poz: Poz }>> = {
  emir: { ifade: 'ofkeli', poz: 'durus' },
  murad: { ifade: 'sinsi', poz: 'el_gogus' },
  bekir: { ifade: 'sinsi', poz: 'isaret' },
  nilufer: { ifade: 'gulumseyen', poz: 'durus' },
  saffet: { ifade: 'ofkeli', poz: 'kol_kaldir' },
  lutfi: { ifade: 'saskin', poz: 'durus' },
  hizir: { ifade: 'normal', poz: 'isaret' },
  zeynep: { ifade: 'uzgun', poz: 'el_gogus' },
  yusuf: { ifade: 'uzgun', poz: 'durus' },
};

export const CharacterSheet: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: 'linear-gradient(#f3e6c8, #e2cfa4)', padding: 30 }}>
      <div style={{ textAlign: 'center', fontFamily: 'Cinzel, serif', fontSize: 72, color: '#6b1a1a', fontWeight: 700 }}>LALE İLE KAN</div>
      <div style={{ textAlign: 'center', fontFamily: 'Nunito, sans-serif', fontSize: 34, color: '#4a3a2a', marginBottom: 10 }}>Karakterler</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', rowGap: 8 }}>
        {CHAR_IDS.map((id) => (
          <div key={id} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Puppet id={id} frame={frame} height={480} {...DEMO[id]} />
            <div style={{ fontFamily: 'Nunito, sans-serif', fontWeight: 800, fontSize: 32, color: '#2b1d14', marginTop: -6 }}>
              {trUpper(id === 'murad' ? 'Emir (Tüccar Murad)' : ISIMLER[id])}
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
