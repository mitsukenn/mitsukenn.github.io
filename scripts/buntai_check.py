# -*- coding: utf-8 -*-
"""まちのAI屋さん コラムの文体チェッカー

使い方
    python scripts/buntai_check.py src/content/blog/xxx.md
    python scripts/buntai_check.py src/content/blog          # フォルダごと
    python scripts/buntai_check.py src/content/blog --published   # 公開記事のみ

メモリ `kiji-buntai-casual` の文体ルールを機械化したもの。
文章の良し悪しは見ない。ルールから外れた箇所だけを出す。
判定は3段階。[NG]=ルール違反 / [警告]=たぶん直したほうがよい / [参考]=多数派から外れている
"""
import sys, os, re, glob

# ---- 分量の基準（全26記事145セクションの実測から。1セクション中央値256字）----
PARA_WARN, PARA_NG = 80, 100        # 1段落
SEC_WARN, SEC_NG = 300, 350         # 1セクション
LEAD_NG = 200                       # 見出しなしで続く冒頭の地の文

# ---- 演出フレーズ（AIっぽさの正体。オーナー指摘済み）----
ENSHUTSU = [
    "先に白状", "想像してみて", "見てほしいんです", "考えてみてください",
    "ちょっと想像", "どうでしょう。", "いかがでしょうか。", "ご存知でしょうか",
]
# ---- 一般的なAI臭マーカー（設計書6章）----
AISHU = [
    "非常に", "まさに", "極めて", "と言えるでしょう", "ではないでしょうか",
    "一概には言えません", "ケースバイケース", "していきましょう", "重要なポイント",
    "ぜひ活用", "いかがでしたか",
]


def strip_md(text):
    """frontmatter・HTMLコメント・コードブロックを落とし、(行番号, 行) で返す"""
    lines = text.split("\n")
    out, in_fm, in_code, in_comment = [], False, False, False
    for i, l in enumerate(lines, 1):
        if i == 1 and l.strip() == "---":
            in_fm = True
            continue
        if in_fm:
            if l.strip() == "---":
                in_fm = False
            continue
        if "<!--" in l:
            in_comment = True
        if in_comment:
            if "-->" in l:
                in_comment = False
            continue
        if l.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        out.append((i, l))
    return out


IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")


def is_media(l):
    """画像だけの行・リンクだけの行は本文として数えない（altやリンク文字は読者の読む量ではない）"""
    t = l.strip()
    if not t:
        return False
    t2 = re.sub(r"\[?!?\[[^\]]*\]\([^)]*\)\]?\([^)]*\)?", "", t)
    return len(re.sub(r"[\s（）()]", "", t2)) < 8


def visible(l):
    """本文として画面に出る部分だけを残す（URL・画像alt・リンク先を除く）"""
    l = IMG.sub("", l)                                  # 画像はaltごと落とす
    l = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", l)      # リンクはラベルだけ残す
    l = re.sub(r"<[^>]+>", "", l)                       # 生HTMLタグ
    return l


def paragraphs(rows):
    """見出し・箇条書き・表・画像行を除いた地の文の段落"""
    for ln, l in rows:
        if is_media(l):
            continue
        t = visible(l).strip()
        if not t or t.startswith(("#", "|", ">", "-", "*", "1.", "2.", "3.")):
            continue
        if re.fullmatch(r"\*\*[^*]+\*\*", t):           # 太字だけの疑似小見出し
            continue
        yield ln, t


def check(path):
    text = open(path, encoding="utf-8").read()
    rows = strip_md(text)
    ng = []

    def add(sev, ln, msg):
        ng.append((sev, ln, msg))

    # ---- 段落の長さ ----
    for ln, t in paragraphs(rows):
        n = len(re.sub(r"\*\*|`", "", t))
        if n > PARA_NG:
            add("NG", ln, f"1段落{n}字（100字超は必ず分割。スマホ360pxで1行約18字）")
        elif n > PARA_WARN:
            add("警告", ln, f"1段落{n}字（基準は80字以内）")

    # ---- セクションの長さ・見出しの形 ----
    secs, cur, cur_ln, head, subs = [], [], 1, None, 0
    for ln, l in rows:
        if l.startswith("## "):
            secs.append((head, cur_ln, "".join(cur), subs))
            head, cur, cur_ln, subs = l[3:].strip(), [], ln, 0
        elif not is_media(l):
            t = visible(l).strip()
            if re.fullmatch(r"\*\*[^*]+\*\*", t):    # 太字だけの段落＝疑似小見出し
                subs += 1
            if t and not t.startswith(("|", "#")):
                cur.append(re.sub(r"\*\*|`|<br>", "", t))
    secs.append((head, cur_ln, "".join(cur), subs))

    for i, (h, ln, body, subs) in enumerate(secs):
        n = len(body)
        if h is None:
            if n > LEAD_NG:
                add("NG", ln, f"見出しなしの冒頭が{n}字（200字を超えるなら小見出しを立てる）")
            continue
        if n > SEC_NG and subs == 0:
            add("NG", ln, f"1セクション{n}字「{h[:16]}」（350字超は分割。太字だけの行で内側を区切る）")
        elif n > SEC_NG and n > 600:
            add("警告", ln, f"1セクション{n}字「{h[:16]}」（疑似小見出しで区切ってあるが長い。分割を検討）")
        elif n > SEC_WARN and subs == 0:
            add("警告", ln, f"1セクション{n}字「{h[:16]}」（基準は250字前後）")
        # 「④ お金の話 ― たぶん、もう払っています」は現行の許容形なので26字までは通す
        if len(h) > 26:
            add("警告", ln, f"見出しが{len(h)}字「{h[:24]}」（長い文章型ではなくラベル調に）")
        # 番号なしが許されるのは冒頭の導入とまとめ・CTA。本編の途中だけ指摘する
        exempt = i <= 1 or i == len(secs) - 1 or re.search(r"まとめ|次回|あわせて|よくある", h)
        if not re.match(r"^[①-⑳]", h) and not exempt:
            add("参考", ln, f"小見出し「{h[:16]}」（本編は「## ① 短いラベル」の連番。"
                             f"冒頭の導入・まとめ・CTAは番号なしでよい）")

    # ---- 行単位のNGフレーズ ----
    for ln, l in rows:
        t = visible(l)
        if l.startswith("#") or not t.strip():
            continue
        for w in ENSHUTSU:
            if w in t:
                add("NG", ln, f"演出フレーズ「{w}」（前振りせず普通に言う）")
        for w in AISHU:
            if w in t:
                add("警告", ln, f"AI臭マーカー「{w}」")
        if re.search(r"[^\s:：]+[:：] ", t) and "http" not in l:
            m = re.search(r"([^\s:：]{1,12}[:：] )", t)
            add("NG", ln, f"コロンでのラベル書き「{m.group(1).strip()}」（―区切り・（）・普通の文に）")
        if re.search(r"\d{1,2}[:：]\d{2}", t):
            add("NG", ln, "時刻は「17時」の形式（コロン不可）")
        for m in re.finditer(r"[ぁ-んァ-ヶ一-龠ー]{2,}たち", t):
            if m.group() not in ("私たち", "子どもたち", "自分たち", "あなたたち"):
                add("警告", ln, f"「{m.group()}」擬人化・〜たちはNG（「道具たち」→「道具」）")
        if re.search(r"\*\*[^*]+\*\*\s*[―—‐-]\s*\S", t):
            add("NG", ln, "太字ラベルをダッシュで本文につないでいる（ラベルの直後で改行する）")
        for m in re.finditer(r"\*\*([^*]+)\*\*", t):
            s = m.group(1)
            if s and (s[0] in "」）。、・" or s[-1] in "「（"):
                add("警告", ln, f"太字の端が約物「{s[:12]}」（両端は非約物の文字に接する）")
            if m.end() < len(t) and t[m.start()-1:m.start()] in ("」", "）"):
                add("NG", ln, f"約物に接した太字「{s[:12]}」はMarkdownで解釈されない（生の**が残る）")

    # ---- 記事全体 ----
    body_all = "".join(visible(l) for _, l in rows)
    if not re.search(r"[0-9０-９]", body_all):
        add("参考", 1, "記事に数字が1つも無い（固有名詞・数字・自分の体験が無いのがAI臭の本質）")
    return ng


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only_pub = "--published" in sys.argv
    target = args[0] if args else "src/content/blog"
    files = sorted(glob.glob(os.path.join(target, "*.md"))) if os.path.isdir(target) else [target]
    total, done = 0, 0
    for f in files:
        if only_pub and "draft: true" in open(f, encoding="utf-8").read():
            continue
        done += 1
        res = check(f)
        total += len(res)
        if not res:
            print(f"\n■ {os.path.basename(f)}　指摘なし")
            continue
        print(f"\n■ {os.path.basename(f)}　{len(res)}件")
        for sev, ln, msg in sorted(res, key=lambda x: x[1]):
            print(f"  {sev:<4} L{ln:<4} {msg}")
    print(f"\n合計 {total}件 / {done}ファイル")


if __name__ == "__main__":
    main()
