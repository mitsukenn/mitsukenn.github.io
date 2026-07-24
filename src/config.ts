/**
 * サイト全体の設定・文言の一元管理ファイル。
 * キャッチコピーやリンク先の差し替えはこのファイルだけ編集すればよい。
 */
export const SITE = {
  name: 'まちのAI屋さん',
  // キャッチコピー ver2.0（2026-07-21、ターゲット=田中さん・主力=AIシステム開発）
  catchcopy: 'その“あったらいいな”、AIでつくれます。',
  subcopy: '長崎のAIシステム開発・導入伴走。「うちだと何ができる？」の無料相談から始められます。',
  description:
    '長崎でAIを使った業務システム・独自ツールの開発なら「まちのAI屋さん」。ChatGPTの先の業務活用を、無料相談から試作・導入・定着まで伴走します。ホームページ制作・AIセミナーも。',

  // LINE公式アカウント（@103fpxtv、2026-07-13開設）
  lineUrl: 'https://lin.ee/XYH9dqc',
  // TODO: Formspree のフォームIDを取得後に差し替え
  formspreeEndpoint: 'https://formspree.io/f/XXXXXXXX',

  area: '長崎県長崎市',
  // TODO: 掲載する代表者名の表記が決まったら設定（空の間は名前を表示しない）
  owner: '',
} as const;

/**
 * トップページ「人気記事ベスト5」の表示順（blogのスラッグを指定）。
 * 当面は編集部選定。GA4のアクセス数が貯まったら月1回、実数で入れ替える。
 */
export const RANKING = [
  'jimu-hanbun-checklist15',
  'chatgpt-shigoto-herananai',
  'ai-app-nani-ga-ikura',
  'nagasaki-chusho-ai-riyuu',
  'chatgpt-hajimekata',
] as const;

export const CATEGORIES = {
  tutorial: 'AI活用チュートリアル',
  subsidy: '補助金・支援制度',
  case: '導入事例・現場の声',
  news: 'やさしいAIニュース',
} as const;

export type CategoryKey = keyof typeof CATEGORIES;
