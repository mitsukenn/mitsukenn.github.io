/**
 * サイト全体の設定・文言の一元管理ファイル。
 * キャッチコピーやリンク先の差し替えはこのファイルだけ編集すればよい。
 */
export const SITE = {
  name: 'まちのAI屋さん',
  // キャッチコピー確定版（2026-07-13）
  catchcopy: 'めんどうな事務仕事、AIで半分にしませんか。',
  subcopy: 'AIとホームページの、気軽な相談窓口です。',
  description:
    '長崎でAIの相談・AIセミナー・ホームページ制作なら「まちのAI屋さん」。補助金を活用したAI研修、月額制のAI顧問、Web制作・保守まで、地元の相談相手としてサポートします。',

  // LINE公式アカウント（@103fpxtv、2026-07-13開設）
  lineUrl: 'https://lin.ee/XYH9dqc',
  // TODO: Formspree のフォームIDを取得後に差し替え
  formspreeEndpoint: 'https://formspree.io/f/XXXXXXXX',

  area: '長崎県長崎市',
  // TODO: 掲載する代表者名の表記が決まったら設定（空の間は名前を表示しない）
  owner: '',
} as const;

export const CATEGORIES = {
  tutorial: 'AI活用チュートリアル',
  subsidy: '補助金・支援制度',
  case: '導入事例・現場の声',
  news: 'やさしいAIニュース',
} as const;

export type CategoryKey = keyof typeof CATEGORIES;
