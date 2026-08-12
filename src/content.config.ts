import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    category: z.enum(['tutorial', 'subsidy', 'case', 'news']),
    ogImage: z.string().optional(),
    heroImage: z.string().optional(),
    draft: z.boolean().default(false),
    // 連載もの。トップの「新着コラム」には各連載1本（seriesOrder: 1）だけを出す。
    // 一覧ページ・ランキングには全回そのまま出る。
    series: z.string().optional(),
    seriesOrder: z.number().int().positive().optional(),
  }),
});

export const collections = { blog };
