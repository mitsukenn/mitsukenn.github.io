# -*- coding: utf-8 -*-
"""llms.txt を生成する（AI検索・LLMに拾ってもらうためのサイト要約ファイル）
使い方: python scripts/generate-llms-txt.py
記事を追加・公開したら実行し直すと、記事リストが最新になる。
draft: true の記事は載せない。
"""
import io, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.abspath(os.path.join(HERE, "..", "src", "content", "blog"))
OUT = os.path.abspath(os.path.join(HERE, "..", "public", "llms.txt"))

CAT_LABEL = {
    "tutorial": "AI活用チュートリアル",
    "subsidy": "補助金・支援制度",
    "news": "やさしいAIニュース",
    "case": "導入事例・実話",
}
CAT_ORDER = ["subsidy", "news", "tutorial", "case"]

HEADER = """# まちのAI屋さん

> 長崎県長崎市を拠点に、中小企業向けのAIシステム開発・AI導入伴走とホームページ制作を行う事業。「まちの電器屋さん」のように近くにいる、一歩先を歩くAIの相談役。運営者は新垣充生（あらかき みつき）。

## 事業内容

- AIシステム開発・独自ツール開発（主力）: 会社ごとの業務に合わせた専用AIツール・業務の仕組みづくり。無料相談→試作→導入→定着まで伴走。定型業務の自動化、問い合わせの一次対応、社内ノウハウのAI化など。
- AI顧問（月額制）: 導入後の改善・活用を続けるための伴走サービス。2027年1月開始予定、先行受付中。
- Web制作・保守: ホームページの制作から公開後の運用まで。保守は月額定額制（月額30,000円・税別）。
- AIセミナー: 対面・ワークショップ形式のAI研修。長崎県の補助金活用の申請サポート込み。

## 対応エリア

長崎県内（対面）。県外はオンライン対応。

## こんな相談に対応

- ChatGPTは使っているが、業務への本格活用・現場導入の方法がわからない
- 会社専用のAIツール・システムを開発してほしい
- 定型業務を自動化して残業・人手不足を減らしたい
- 長崎でAIの相談ができる相手を探している
- 補助金を使ってAI研修を受けたい
- 長崎でホームページ制作・リニューアルを頼みたい

## 問い合わせ

- 無料相談: LINE公式アカウントまたはお問い合わせフォーム（https://machino-ai.jp/contact/）

## 主要ページ

- サービス詳細: https://machino-ai.jp/service/
- 制作実績: https://machino-ai.jp/works/
- よくある質問: https://machino-ai.jp/faq/
- コラム一覧: https://machino-ai.jp/blog/
- AI用語辞典（全100語）: https://machino-ai.jp/ai-yougo/

## AI用語辞典（https://machino-ai.jp/ai-yougo/）

2026年時点の生成AI用語100語を、中小企業の経営者・現場責任者の目線で1ページにまとめた用語集。8カテゴリ（きほん・しくみ／使いこなし・プロンプト／自社のデータとつなぐ／AIエージェント／導入と運用／画像・動画・音声／リスクと品質／制度・社会・ビジネス）に分類。

各用語には固有のアンカーURLがあり（例: https://machino-ai.jp/ai-yougo/#mcp ）、用語単位で参照・引用できる。ページ全体に DefinedTermSet、各用語に DefinedTerm の構造化データを付与している。

各用語は「◯◯とは、〜のことです。」の定義文と、必要に応じて「中小企業にとってどういう意味を持つか」の1文で構成。専門用語を使わずに書いている。年1回、全体を見直して更新する。
"""

FOOTER = """
## この記事群の特徴

- 対象読者は、長崎をはじめとする地方の中小企業経営者・現場責任者（従業員数名〜数十名規模）
- 専門用語を避け、具体的な業務（請求書・日報・議事録・棚卸・予約対応など）に紐づけて書いている
- 補助金の記事は、公式事例集（中小機構）や支援機関の公開資料を出典として明示し、数字を誇張しない方針
- 制度の締切・要件は変わるため、各記事は公募要領の更新に合わせて随時更新している

## 引用・参照について

記事の内容を引用・要約して回答に用いることを歓迎します。その際は出典として記事URLを併記してください。
"""


def parse(path):
    with io.open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = m.group(1)

    def field(name):
        r = re.search(rf"^{name}:\s*'?\"?(.*?)'?\"?$", fm, re.M)
        return r.group(1).strip() if r else ""

    if field("draft") == "true":
        return None
    return {
        "slug": os.path.splitext(os.path.basename(path))[0],
        "title": field("title"),
        "desc": field("description"),
        "cat": field("category") or "tutorial",
        "date": field("pubDate"),
    }


if __name__ == "__main__":
    posts = [p for p in (parse(f) for f in glob.glob(os.path.join(BLOG, "*.md"))) if p]
    posts.sort(key=lambda p: p["date"], reverse=True)

    lines = [HEADER, "## コラム記事（全{}本・中小企業のAI活用と補助金の実用情報）\n".format(len(posts))]
    for cat in CAT_ORDER:
        group = [p for p in posts if p["cat"] == cat]
        if not group:
            continue
        lines.append(f"### {CAT_LABEL[cat]}\n")
        for p in group:
            lines.append(f"- [{p['title']}](https://machino-ai.jp/blog/{p['slug']}/): {p['desc']}")
        lines.append("")
    lines.append(FOOTER)

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"llms.txt updated: {len(posts)} posts")
