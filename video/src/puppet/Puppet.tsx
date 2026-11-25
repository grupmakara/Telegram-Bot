import React from 'react';
import type { CharId, Ifade, Poz } from '../story/registry';
import { CHARACTERS } from './characters';
import { Arm, BackHair, Body, Face, Headwear } from './parts';

export const VIEW = { x: 0, y: -120, w: 400, h: 1120 };

/** Hareket eden kol için (omuz, dirsek) açıları; diğer kol dinlenir. */
const POSES: Record<Poz, [number, number]> = {
  durus: [12, -10],
  isaret: [100, -15],
  kol_kaldir: [160, -20],
  el_gogus: [20, -130],
};
const REST: [number, number] = [10, -8];

const seedOf = (id: string) => [...id].reduce((a, c) => a + c.charCodeAt(0), 0);

export type PuppetProps = {
  id: CharId;
  ifade?: Ifade;
  poz?: Poz;
  yon?: 'sol' | 'sag';
  mouthOpen?: number;
  frame: number;
  height: number;
};

export const Puppet: React.FC<PuppetProps> = ({ id, ifade = 'normal', poz = 'durus', yon = 'sag', mouthOpen = 0, frame, height }) => {
  const look = CHARACTERS[id];
  const seed = seedOf(id);
  const period = 100 + (seed % 30);
  const blink = (frame + seed * 7) % period < 4;
  const breathe = Math.sin(frame / 18 + seed) * 4;
  const sway = Math.sin(frame / 40 + seed) * 1.2 + mouthOpen * 1.5;
  const [gu, gl] = POSES[poz];
  const idle = Math.sin(frame / 25 + seed) * 2;
  const width = (height * VIEW.w) / VIEW.h;
  const flip = yon === 'sol' ? 'translate(400,0) scale(-1,1)' : '';

  return (
    <svg width={width} height={height} viewBox={`${VIEW.x} ${VIEW.y} ${VIEW.w} ${VIEW.h}`} style={{ overflow: 'visible' }}>
      <g transform={flip}>
        <g transform={`translate(0,${breathe * 0.4})`}>
          <Body look={look} />
          <g transform="translate(125,370)">
            <Arm look={look} upper={REST[0] + idle} lower={REST[1]} />
          </g>
        </g>
        <g transform={`translate(0,${breathe}) rotate(${sway},200,330)`}>
          <BackHair look={look} />
          <Face look={look} ifade={ifade} mouthOpen={mouthOpen} blink={blink} look_dx={5} />
          <Headwear look={look} />
        </g>
        <g transform={`translate(275,${370 + breathe * 0.4}) scale(-1,1)`}>
          <Arm look={look} upper={gu + idle} lower={gl} />
        </g>
      </g>
    </svg>
  );
};
