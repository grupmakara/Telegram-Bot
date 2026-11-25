import type { CharId } from '../story/registry';

export type Headwear = 'sarik' | 'sarik_sorguc' | 'kavuk_tall' | 'kavuk_big' | 'katip' | 'hotoz' | 'basortu' | 'kece' | 'none';
export type Hair = 'short' | 'braid' | 'none';
export type Beard = 'none' | 'short' | 'full';
export type Outfit = 'kaftan' | 'entari' | 'vest';

export type Look = {
  female: boolean;
  skin: string;
  hair: Hair;
  hairColor: string;
  beard: Beard;
  beardColor: string;
  mustache: boolean;
  browColor: string;
  browWidth: number;
  headwear: Headwear;
  headwearColor: string; // ana renk (kavuk/sarık beyazı, keçe kırmızısı...)
  outfit: Outfit;
  coat: string; // kaftan / entari / yelek rengi
  trim: string; // kenar şeridi
  shirt: string; // iç gömlek / entari altı
  belt: string;
  pants: string;
  shoes: string;
  fur?: boolean;
  scar?: boolean;
  eyepatch?: boolean;
  glasses?: boolean;
  old?: boolean;
  dagger?: boolean;
};

const base: Omit<Look, 'skin' | 'coat'> = {
  female: false, hair: 'short', hairColor: '#2a1c14', beard: 'none', beardColor: '#2a1c14', mustache: false,
  browColor: '#2a1c14', browWidth: 10, headwear: 'none', headwearColor: '#f4f1ea', outfit: 'kaftan',
  trim: '#d9b25c', shirt: '#efe6d2', belt: '#8a5a2b', pants: '#4a3a2e', shoes: '#c9952f',
};

export const CHARACTERS: Record<CharId, Look> = {
  emir: { ...base, skin: '#e3ad84', beard: 'short', mustache: true, browWidth: 13, headwear: 'sarik', coat: '#1f2f57', trim: '#c9a55a', belt: '#6b4a2a', shirt: '#e9e1cf' },
  murad: { ...base, skin: '#e3ad84', beard: 'short', mustache: true, browWidth: 13, headwear: 'sarik_sorguc', coat: '#7a1f2b', trim: '#e2b84a', belt: '#e2b84a', shirt: '#f2e6c8', shoes: '#e2b84a' },
  bekir: { ...base, skin: '#d59d76', old: true, beard: 'full', beardColor: '#8d8a86', mustache: true, browColor: '#6f6b67', browWidth: 15, headwear: 'kavuk_tall', coat: '#17151a', trim: '#d4a73c', fur: true, belt: '#d4a73c', shirt: '#7a1f2b' },
  nilufer: { ...base, female: true, skin: '#f2cdb0', hair: 'braid', hairColor: '#7a3b22', browColor: '#6b3320', browWidth: 6, headwear: 'hotoz', headwearColor: '#e2b84a', outfit: 'entari', coat: '#9fcf9a', trim: '#e2b84a', shirt: '#f6f1e4', belt: '#e2b84a', shoes: '#c94f4f' },
  saffet: { ...base, skin: '#c58a60', mustache: true, browWidth: 14, scar: true, dagger: true, outfit: 'vest', coat: '#a62b25', trim: '#d9b25c', shirt: '#ece4d4', belt: '#3a2a20', pants: '#2f2a28', shoes: '#3a2a20' },
  lutfi: { ...base, skin: '#e4bb98', old: true, beard: 'full', beardColor: '#f1efe9', mustache: true, browColor: '#d9d6cf', browWidth: 10, glasses: true, headwear: 'kavuk_big', coat: '#264d36', trim: '#e8e2d2', shirt: '#e8e2d2', belt: '#264d36' },
  hizir: { ...base, skin: '#c68f66', old: true, beard: 'short', beardColor: '#efece6', mustache: true, browColor: '#e6e2da', browWidth: 12, eyepatch: true, headwear: 'kece', headwearColor: '#b23a2e', outfit: 'vest', coat: '#2e5e9e', trim: '#e8d9a8', shirt: '#efe4cc', belt: '#8a5a2b', pants: '#3b4a63', shoes: '#5a3b24' },
  zeynep: { ...base, female: true, skin: '#edc3a0', hair: 'none', browWidth: 6, headwear: 'basortu', outfit: 'entari', coat: '#8f8f96', trim: '#b9b9c0', shirt: '#e9e6e0', belt: '#6d6d74', shoes: '#4a3b30' },
  yusuf: { ...base, skin: '#dcab85', old: true, beard: 'full', beardColor: '#9a948c', mustache: true, browColor: '#7f7a73', headwear: 'katip', headwearColor: '#f1ece2', coat: '#6b4a2f', trim: '#c9a55a', shirt: '#e8dcc4', belt: '#3f2b1b' },
};
