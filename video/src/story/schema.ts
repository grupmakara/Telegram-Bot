import { z } from 'zod';
import { CHAR_IDS, IFADELER, MEKAN_IDS, POZLAR, SPEAKER_IDS } from './registry';

export const LineSchema = z.object({
  kim: z.enum(SPEAKER_IDS),
  metin: z.string().min(1),
  ifade: z.enum(IFADELER).optional(),
  poz: z.enum(POZLAR).optional(),
});

export const SceneSchema = z.object({
  mekan: z.enum(MEKAN_IDS),
  gecmis: z.boolean().optional(),
  gece: z.boolean().optional(),
  karakterler: z.array(z.object({
    id: z.enum(CHAR_IDS),
    x: z.number().min(0).max(1),
    ifade: z.enum(IFADELER).optional(),
    yon: z.enum(['sol', 'sag']).optional(),
  })).min(1),
  satirlar: z.array(LineSchema).min(1),
});

export const EpisodeSchema = z.object({
  bolum: z.number().int().positive(),
  baslik: z.string().min(1),
  kanca: LineSchema,
  sahneler: z.array(SceneSchema).min(1),
  son: LineSchema,
  aciklama: z.string(),
  etiketler: z.array(z.string()),
}).superRefine((ep, ctx) => {
  ep.sahneler.forEach((s, si) => {
    const present = new Set(s.karakterler.map((k) => k.id));
    s.satirlar.forEach((l, li) => {
      if (l.kim !== 'anlatici' && !present.has(l.kim)) {
        ctx.addIssue({ code: 'custom', path: ['sahneler', si, 'satirlar', li, 'kim'], message: `'${l.kim}' bu sahnede yok` });
      }
    });
  });
});

export type Line = z.infer<typeof LineSchema>;
export type Scene = z.infer<typeof SceneSchema>;
export type Episode = z.infer<typeof EpisodeSchema>;
