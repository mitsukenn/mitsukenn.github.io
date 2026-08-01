# -*- coding: utf-8 -*-
"""ダウンロード済みの解説図解を記事へ配置する（2026-08-01）
MAP[slug] = [(DLファイル名, 保存名, 挿入アンカー, alt), ...]
アンカー文字列の直前に画像Markdownを挿入する。
"""
import io, os, shutil
from PIL import Image

DL = os.path.expanduser("~/Downloads")
HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.abspath(os.path.join(HERE, "..", "public", "assets", "images", "blog"))
BLOG = os.path.abspath(os.path.join(HERE, "..", "src", "content", "blog"))
ARC = os.path.abspath(os.path.join(HERE, "..", "..", "99_image_output", "sup"))

MAP = {
 "ax-toha-nani": [
  ("T1-13", "zu-ax-sousa-vs-tanomu", "## AXにも「レベル」がある",
   "比較図。DXでは人がシステムを操作する、AXではAIに頼む"),
  ("T1-15", "zu-ax-3level", "## なぜ「今年から」急に言われ始めたのか",
   "AXの3レベル。個人の道具、業務に組み込む、経営の前提"),
 ],
 "honebuto-2026-ax": [
  ("T1-16", "zu-honebuto-5point", "## 注意 ― 「骨太に書いてある」≠「明日から使える制度」",
   "骨太の方針2026のポイント5つ。AXへの転換、地域AX、補助金の名称変更、17分野への集中投資、AI人材の育成"),
 ],
 "chiisana-kaisha-ax-hajimekata": [
  ("T1-17", "zu-gyoumu-3kijun", "## 第3段階 ― 事業をAI前提で見直す（半年〜）",
   "業務を選ぶ3つの基準。毎日おきる、型が決まっている、夜や休日にやっている"),
  ("T5-03", "zu-koka-timeline", "## お金の話 ― 無料の支援と補助金の使いどころ",
   "効果が出るまでの時間の目安。今日は個人で使う、1〜3か月で業務に組み込む、半年から事業を見直す"),
 ],
 "digital-ai-hojokin-2026": [
  ("T1-18", "zu-hojokin-henka3", "## 意外と知られていない大事な仕組み",
   "旧IT導入補助金からの変化。AIツール、賃上げ要件、2回目以降の3点比較"),
  ("T3-15", "zu-hojokin-taisho", "## 次の締切は8月25日",
   "補助金の対象になりやすいもの・なりにくいもの。登録済みITツールは対象、完全オーダーメイド開発は対象外"),
 ],
 "digital-ai-hojokin-shinsei-nagare": [
  ("T1-19", "zu-shinsei-otoshiana", "## 8月25日締切からの逆算スケジュール",
   "補助金申請の3つの落とし穴。交付決定前の発注、後払いの資金繰り、報告義務の軽視"),
  ("T5-04", "zu-soudan-junbi", "## まとめ",
   "相談前に用意しておくと早い3つ。困っている業務、今のやり方、どのくらい時間がかかるか"),
 ],
 "inshokuten-hojokin-mirai": [
  ("T1-20", "zu-inshoku-dougu-map", "## ③ 勘の答え合わせができる",
   "飲食店に入れる道具のマップ。セルフレジ、QRオーダー、POS、在庫管理、予約・顧客管理"),
  ("T2-09", "zu-inshoku-qr-kaikei", "## ④ これ全部、補助金の対象",
   "店頭でお客様がQRコードを使って会計する様子のイラスト"),
 ],
 "nagasaki-chusho-ai-riyuu": [
  ("T1-21", "zu-kuraberu-aite", "## 理由3 ― 長崎では、今始めれば十分早いから",
   "比べる相手は東京の先進企業ではなく地元の同業者"),
  ("T5-02", "zu-ai-makaseru-junban", "## 長崎でAIの相談は、どこでできる？",
   "AIに任せる順番。失敗しても平気な文章、毎日の定型作業、お金や判断が絡むものは最後"),
 ],
 "chatgpt-hajimekata": [
  ("T1-22", "zu-chatgpt-template", "## ステップ3 ― 毎日の「面倒な文章仕事」をひとつ任せる",
   "ChatGPTへの最初の質問テンプレート。私は長崎で〇〇業をしています、従業員は〇人です、AIが手伝えることを簡単な順に5つ教えてください"),
  ("T3-14", "zu-ai-omoikomi", "## まとめ",
   "よくある思い込みと実際。AIが勝手に全部やってくれるのではなく、下書きはAI、確認と判断は人"),
 ],
 "jimu-hanbun-checklist15": [
  ("T4-01", "zu-ai-hito-buntan", "## ② 整理系 — 議事録やメモの整理、夜にやっていませんか？",
   "AIがやることと人がやることの分担。下書き・整理・計算の準備はAI、判断とお金の最終確認は人"),
 ],
 "hp-seisaku-hiyou-nagasaki": [
  ("T4-02", "zu-hp-soba-3dankai", "## チェック1 ― 月々の保守費はある？その中身は何？",
   "ホームページ費用相場の3段階。ひな形、デザインから制作、EC・予約つき"),
  ("T2-08", "zu-mitsumori-nayamu", "## 「作って終わり」が一番もったいない",
   "複数の見積書を前に腕組みして悩む店主のイラスト"),
 ],
 "line-koushiki-tsukurikata": [
  ("T4-03", "zu-line-aisatsu-4yoso", "## うまくいかない時は、どうすればいい？",
   "あいさつメッセージに入れる4要素。名乗り、送っていい例、返信の目安、気軽さの一言"),
  ("T1-01", "zu-line-qr-annai", "## まとめ",
   "レジ横のQRコードでお客様に友だち追加を案内する様子"),
 ],
 "ai-soudan-aite-erabikata": [
  ("T2-10", "zu-soudan-yoi-abunai", "## 5箇条その3 ― 料金が明朗か？",
   "良い相手と危ない相手の対比。先に話を聞く・できないことも言う・料金が明朗か、いきなり契約書・何でもできると言う・料金が不明か"),
  ("T1-02", "zu-kiken-sign", "## まとめ",
   "危険サインの注意図"),
 ],
 "hp-hoshu-tsukutte-owari": [
  ("T2-11", "zu-hp-houchi-jingai", "## なぜ「作って終わり」になってしまうのか？",
   "ホームページを放置すると起きる3つの実害。古い情報でお客様が困る、スマホで崩れて不信感、検索で見つからない"),
  ("T1-04", "zu-hoshu-nakami", "## まとめ",
   "保守で実際にやること。文言の修正、お知らせ更新、表示の点検、相談対応"),
 ],
 "55sai-chichi-to-ai": [
  ("T2-12", "zu-hajimekata-3kotsu", "## 「パソコンが苦手でも大丈夫ですか？」への私の答え",
   "AIの始め方3つのコツ。声で話しかける、正解を求めない、最初は誰かと一緒に"),
  ("T1-14", "zu-chichi-sumaho", "## 父から学んだこと — 人は本来、知りたい動物",
   "スマートフォンのAIに話しかけて驚く年配男性のイラスト"),
 ],
 "chatgpt-shigoto-herananai": [
  ("T2-13", "zu-jitan-vs-shikumi", "## まとめ",
   "個人の時短から業務の仕組みへ。ここを越えると会社全体が変わる"),
  ("T1-06", "zu-office-ai-aibou", "## で、何から始めればいいの？",
   "オフィスで全員がAIロボットと一緒に働くイラスト"),
 ],
 "ai-app-nani-ga-ikura": [
  ("T1-07", "zu-app-kousou3", "## で、いくらかかるの？",
   "自社専用AIアプリの構想例3つ。見積・請求書、写真から報告書、問い合わせ対応"),
  ("T2-14", "zu-app-shippai-shinai", "## まとめ",
   "失敗しない進め方3つ。使う人を巻き込む、100点を狙わない、相談相手を確保する"),
 ],
 "excel-kanrihyou-app-ka": [
  ("T1-09", "zu-mazuha-1mai", "## 最初の「1枚」は、どう選べばいい？",
   "書類の山から、まずは1枚だけを選ぶ図"),
  ("T1-10", "zu-genba-nyuryoku-renkei", "## まとめ",
   "現場のスマホ入力が事務所の画面に同時反映される図"),
 ],
 "gijiroku-ai-jidouka": [
  ("T1-11", "zu-gijiroku-3kimegoto", "## 気をつけることはある？",
   "議事録AI導入前に決める3つ。目的を決める、型を決める、確認する人を決める"),
  ("T4-05", "zu-ai-ireteyoi-dame", "## まとめ",
   "AIに入れてよい情報とだめな情報。一般的な相談や社外に出ている情報はよい、お客様の個人情報や社外秘の数字はだめ"),
 ],
 "digital-hojokin-guide": [
  ("T2-01", "zu-kenhojokin-4step", "## よくあるつまずきポイント",
   "県の補助金申請4ステップ。対象を確認、研修計画、書類を提出、決定後に受講"),
  ("T5-05", "zu-kenhojokin-tsumazuki", "## まとめ",
   "よくあるつまずき。交付決定の前に契約しない、書類の準備を後回しにしない"),
 ],
 "ai-news-202607": [
  ("T4-04", "zu-news-202607-3topics", "## ① ChatGPTに「仕事を任せる」新機能Work ― 事務仕事に効く話",
   "2026年7月のAIニュース3本。ChatGPTに仕事を任せるWork、人と話せる音声AI、国の無料伴走支援が始動"),
  ("T2-03", "zu-onsei-ai-kaiwa", "## ③ 国の「生産性向上支援センター」が本格始動 ― お金と制度の話",
   "スマートフォンの音声AIと自然に会話するイラスト"),
 ],
 "kensetsu-hojokin-mirai": [
  ("T2-04", "zu-kensetsu-suuji3", "## ② もし自分が現場を回していたら",
   "建設業の実例。日報作成9割減、設計変更対応6割短縮、施工ミス7割減"),
  ("T5-01", "zu-kensetsu-1nichi", "## ③ 職人さんの経験が、写真と記録で残る",
   "現場の一日のビフォーアフター。いまは事務所に戻って日報を書き直す、導入後は現場でスマホに一言でそのまま直帰"),
 ],
 "kouri-hojokin-mirai": [
  ("T2-06", "zu-kouri-suuji3", "## ② もし自分の店だったら",
   "小売店の実例。棚卸時間5割減、廃棄ロス8%から3%、EC売上1.5倍"),
  ("T2-07", "zu-kouri-barcode", "## ③ 商圏が、店の場所から自由になる",
   "ハンディスキャナーでバーコードを読み取って棚卸を進めるイラスト"),
 ],
 "kaigo-iryo-hojokin-mirai": [
  ("T3-01", "zu-kaigo-suuji3", "## ② もし自分が現場にいたら",
   "介護・医療の実例。夜間巡回5割効率化、診療時間25%短縮、発注工数7割減"),
  ("T3-02", "zu-kaigo-tonari-ni-suwaru", "## ③ 「人にしかできない仕事」に時間が戻る",
   "タブレットを置いて利用者の隣に座って話す介護スタッフのイラスト"),
 ],
 "seizo-hojokin-mirai": [
  ("T3-03", "zu-seizo-suuji3", "## ② もし自分の工場だったら",
   "製造業の実例。納期遅延8割減、稼働率15%向上、管理工数半減"),
  ("T3-11", "zu-seizo-kouteihyou", "## ③ 「いつできる？」に即答できるのは、信用になる",
   "頭の中の工程表が画面の工程表に変わる図"),
 ],
 "shigyo-hojokin-mirai": [
  ("T3-05", "zu-shigyo-30sha", "## ② もし自分の事務所だったら",
   "顧問先が1年で30社増。入力が減って受け入れ枠が広がった"),
  ("T3-12", "zu-shigyo-sagyo-handan", "## ③ AIは判断をしない。判断こそ士業の仕事",
   "作業から判断へ。入力・転記・チェックから、正しい扱いとこれからの方針へ"),
 ],
 "ohama-tatami-seisaku-story": [
  ("T3-13", "zu-hp-5step", "## ステップ3 ― 写真と文章は、どうやって準備した？",
   "ホームページ制作の5ステップ。聞き取り、構成の提案、写真と文章、公開、保守"),
  ("T3-07", "zu-tatami-kikitori", "## ステップ5 ― 公開してからが本番（保守はどうする？）",
   "畳職人の工房で話を聞きながらメモを取る制作風景のイラスト"),
 ],
}

if __name__ == "__main__":
    conv, ins, issues = 0, 0, []
    for slug, items in MAP.items():
        md_path = os.path.join(BLOG, slug + ".md")
        with io.open(md_path, encoding="utf-8") as f:
            text = f.read()
        changed = False
        for dl_name, save_name, anchor, alt in items:
            src = os.path.join(DL, dl_name + ".png")
            webp = os.path.join(DST, save_name + ".webp")
            if not os.path.exists(src):
                issues.append(f"{dl_name}.png missing")
                continue
            if not os.path.exists(webp):
                img = Image.open(src).convert("RGB")
                w, h = img.size
                img = img.resize((1200, round(h * 1200 / w)), Image.LANCZOS)
                img.save(webp, "WEBP", quality=82, method=6)
                shutil.copy2(src, os.path.join(ARC, save_name + ".png"))
                conv += 1
            md_img = f"![{alt}](/assets/images/blog/{save_name}.webp)"
            if md_img in text:
                continue
            if anchor not in text:
                issues.append(f"{slug}: anchor not found -> {anchor[:26]}")
                continue
            text = text.replace(anchor, md_img + "\n\n" + anchor, 1)
            ins += 1
            changed = True
        if changed:
            with io.open(md_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    print(f"converted={conv} inserted={ins}")
    print("issues:", issues if issues else "none")
