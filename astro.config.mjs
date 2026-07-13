// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // 独自ドメイン（2026-07-13接続）
  site: 'https://machino-ai.jp',
  integrations: [sitemap()],
});
