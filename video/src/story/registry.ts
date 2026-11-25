export const CHAR_IDS = ['emir', 'murad', 'bekir', 'nilufer', 'saffet', 'lutfi', 'hizir', 'zeynep', 'yusuf'] as const;
export type CharId = (typeof CHAR_IDS)[number];
export type SpeakerId = CharId | 'anlatici';
export const SPEAKER_IDS = [...CHAR_IDS, 'anlatici'] as const;

export const MEKAN_IDS = ['divan', 'konak_salon', 'lale_bahcesi', 'halic_liman', 'carsi', 'zindan', 'idam_meydani'] as const;
export type MekanId = (typeof MEKAN_IDS)[number];

export const IFADELER = ['normal', 'ofkeli', 'uzgun', 'saskin', 'gulumseyen', 'sinsi'] as const;
export type Ifade = (typeof IFADELER)[number];
export const POZLAR = ['durus', 'isaret', 'kol_kaldir', 'el_gogus'] as const;
export type Poz = (typeof POZLAR)[number];

export const ISIMLER: Record<SpeakerId, string> = {
  emir: 'Emir', murad: 'Murad', bekir: 'Kara Bekir Paşa', nilufer: 'Nilüfer', saffet: 'Saffet Ağa',
  lutfi: 'Kadı Lütfi', hizir: 'Hızır Reis', zeynep: 'Zeynep', yusuf: 'Yusuf Efendi', anlatici: '',
};

export const trUpper = (s: string): string => s.toLocaleUpperCase('tr-TR');
