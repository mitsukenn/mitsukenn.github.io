# -*- coding: utf-8 -*-
"""ブログ記事の文字入りサムネイル生成（A案・白カード中央型）
使い方: python scripts/generate-thumbnails.py
ARTICLES に slug: (タグ, 1行目, 2行目) を足して実行すると
public/assets/images/blog/thumb-<slug>.webp が生成される。
1行あたり全角11文字まで。フォントはサイトと同じ Zen Kaku Gothic New。
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "assets", "images", "blog")
FB = os.path.join(HERE, "fonts", "ZenKakuGothicNew-Bold.ttf")
FM = os.path.join(HERE, "fonts", "ZenKakuGothicNew-Medium.ttf")

W, H = 1200, 675
WHITE = (255, 255, 255)

# カテゴリ別配色: primary=メイン文字, accent=タグ・バー, bg_top/bg_bottom=背景グラデ, footer=下部文字
PALETTES = {
    "tutorial": {  # ブランド青
        "primary": (0, 74, 173), "accent": (14, 143, 190),
        "bg_top": (214, 232, 246), "bg_bottom": (232, 242, 250), "footer": (60, 90, 140),
    },
    "subsidy": {   # 緑（お金・安心）
        "primary": (9, 106, 68), "accent": (23, 160, 107),
        "bg_top": (214, 240, 227), "bg_bottom": (232, 248, 239), "footer": (46, 110, 82),
    },
    "news": {      # オレンジ（新着・話題）
        "primary": (176, 84, 8), "accent": (236, 144, 48),
        "bg_top": (250, 234, 216), "bg_bottom": (252, 243, 231), "footer": (150, 96, 48),
    },
    "case": {      # 紫（ストーリー・事例）
        "primary": (85, 58, 160), "accent": (139, 111, 216),
        "bg_top": (232, 228, 246), "bg_bottom": (242, 240, 250), "footer": (98, 80, 150),
    },
}

ARTICLES = {
    "nagasaki-chusho-ai-riyuu":        ("長崎 × AI活用", "人が来ないなら、", "仕事を軽くする。"),
    "chatgpt-hajimekata":              ("ChatGPT入門", "10分で始める、", "ChatGPT。"),
    "jimu-hanbun-checklist15":         ("事務効率化", "事務仕事、", "AIで半分に。"),
    "hp-seisaku-hiyou-nagasaki":       ("ホームページ", "制作費で損しない、", "5つのチェック。"),
    "line-koushiki-tsukurikata":       ("LINE活用", "お店のLINE、", "スマホだけで作れる"),
    "ai-soudan-aite-erabikata":        ("業者選び", "騙されないための、", "5箇条。"),
    "hp-hoshu-tsukutte-owari":         ("ホームページ", "作って終わりが、", "いちばん損。"),
    "hp-mitemorau-hoho":               ("ホームページ", "Googleは経験を、", "見ている。"),
    "55sai-chichi-to-ai":              ("実話", "スマホ音痴の父が、", "AIにハマるまで。"),
    "chatgpt-shigoto-herananai":       ("AI活用のツボ", "使えるのに、", "仕事が減らないナゾ"),
    "ai-app-nani-ga-ikura":            ("システム開発", "うちだけの、", "専用AIアプリ。"),
    "excel-kanrihyou-app-ka":          ("脱Excel", "転記だらけの毎日、", "卒業。"),
    "gijiroku-ai-jidouka":             ("議事録AI", "議事録1時間が、", "確認3分に。"),
    "digital-hojokin-guide":           ("長崎県の補助金", "AI研修、", "県の補助金で。"),
    "ai-news-202607":                  ("月刊AIニュース 2026年7月", "今月の3本だけ、", "押さえればOK。"),
    "ax-toha-nani":                    ("AX入門 ①", "DXの次は、", "AX。"),
    "honebuto-2026-ax":                ("AX入門 ②", "国がAXを、", "国策にした。"),
    "chiisana-kaisha-ax-hajimekata":   ("AX入門 ③", "最初の一歩は、", "0円から。"),
    "digital-ai-hojokin-2026":         ("補助金まるわかり", "国が半分、", "出してくれる。"),
    "digital-ai-hojokin-shinsei-nagare": ("申請ガイド", "今日やることは、", "2つだけ。"),
    "inshokuten-hojokin-mirai":        ("飲食店 × 補助金", "夜10時のレジ締め、", "消えるかも。"),
    "kensetsu-hojokin-mirai":          ("建設業 × 補助金", "現場終わりの日報、", "消えるかも。"),
    "kouri-hojokin-mirai":             ("小売店 × 補助金", "棚卸が、", "半分で終わるかも。"),
    "kaigo-iryo-hojokin-mirai":        ("介護・医療 × 補助金", "夜の見回り、", "半分になるかも。"),
    "seizo-hojokin-mirai":             ("町工場 × 補助金", "いつできる？に、", "即答できる工場へ。"),
    "shigyo-hojokin-mirai":            ("士業 × 補助金", "顧問先が1年で、", "30社増えた話。"),
    "ohama-tatami-seisaku-story":      ("制作事例", "畳屋さんのHPが、", "できるまで。"),
    "chatgpt-claude-code-codex-chigai": ("AIツール整理", "ChatGPTの次に、", "触るならこれ。"),
    "ai-ni-makaseru-4sou":             ("AIの任せ方 ①", "AIに渡せる仕事、", "渡せない仕事。"),
    "ai-daikou-kara-shikumi-he":       ("AIの任せ方 ②", "その作業、", "来年もやりますか？"),
    "merumaga-ai-de-yomu":             ("情報収集 × AI", "長いメルマガ、", "AIに読ませる。"),
}


def center(d, cx, y, text, font, fill):
    b = d.textbbox((0, 0), text, font=font)
    d.text((cx - (b[2] - b[0]) / 2, y), text, font=font, fill=fill)


def read_category(slug):
    p = os.path.join(HERE, "..", "src", "content", "blog", slug + ".md")
    with open(p, encoding="utf-8") as f:
        for line in f:
            if line.startswith("category:"):
                return line.split(":", 1)[1].strip()
    return "tutorial"


def make(tag, line1, line2, path, pal):
    primary, accent = pal["primary"], pal["accent"]
    bt, bb = pal["bg_top"], pal["bg_bottom"]
    img = Image.new("RGB", (W, H), bb)
    d = ImageDraw.Draw(img, "RGBA")
    for yy in range(H):
        t = yy / H
        d.line([(0, yy), (W, yy)], fill=tuple(int(bt[i] + (bb[i] - bt[i]) * t) for i in range(3)))
    d.ellipse([-140, -180, 320, 280], outline=accent + (50,), width=4)
    d.ellipse([980, 440, 1360, 820], outline=primary + (40,), width=4)
    d.ellipse([1010, 90, 1090, 170], fill=accent + (36,))
    d.ellipse([150, 520, 205, 575], fill=primary + (30,))

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([120, 132, 1080, 552], radius=26,
                                         fill=(primary[0] // 3, primary[1] // 3, primary[2] // 3, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    img.paste(sh, (0, 10), sh)
    d.rounded_rectangle([120, 122, 1080, 542], radius=26, fill=WHITE)

    center(d, 600, 168, "＼ " + tag + " ／", ImageFont.truetype(FM, 40), accent)
    f_main = ImageFont.truetype(FB, 82)
    center(d, 600, 244, line1, f_main, primary)
    center(d, 600, 356, line2, f_main, primary)
    d.rounded_rectangle([540, 476, 660, 487], radius=5, fill=accent)
    center(d, 600, 586, "まちのAI屋さん ｜ 長崎のAI・ホームページ相談窓口", ImageFont.truetype(FM, 32), pal["footer"])

    img.save(path, "WEBP", quality=85, method=6)


if __name__ == "__main__":
    for slug, (tag, l1, l2) in ARTICLES.items():
        cat = read_category(slug)
        pal = PALETTES.get(cat, PALETTES["tutorial"])
        p = os.path.join(OUT, f"thumb-{slug}.webp")
        make(tag, l1, l2, p, pal)
        print(f"thumb-{slug}.webp  [{cat}]  {os.path.getsize(p)//1024}KB")
    print(f"done: {len(ARTICLES)} thumbnails")
