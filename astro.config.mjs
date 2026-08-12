// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkBreaks from 'remark-breaks';

// https://astro.build/config
export default defineConfig({
  // 独自ドメイン（2026-07-13接続）
  site: 'https://machino-ai.jp',
  integrations: [sitemap()],
  markdown: {
    // 原稿の改行をそのまま<br>にする（2026-08-12導入）。
    // スマホ前提で1文ずつ行を分けて書くため。既存記事18本70か所の
    // 段落内改行も、これで書かれたとおりに表示されるようになる。
    remarkPlugins: [remarkBreaks],
  },
});
