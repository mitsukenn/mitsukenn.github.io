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
NAVY = (0, 74, 173)
BLUE = (14, 143, 190)
WHITE = (255, 255, 255)

ARTICLES = {
    "nagasaki-chusho-ai-riyuu":        ("長崎 × AI活用", "人が来ないなら、", "仕事を軽くする。"),
    "chatgpt-hajimekata":              ("ChatGPT入門", "10分で始める、", "ChatGPT。"),
    "jimu-hanbun-checklist15":         ("事務効率化", "事務仕事、", "AIで半分に。"),
    "hp-seisaku-hiyou-nagasaki":       ("ホームページ", "制作費で損しない、", "5つのチェック。"),
    "line-koushiki-tsukurikata":       ("LINE活用", "お店のLINE、", "スマホだけで作れる"),
    "ai-soudan-aite-erabikata":        ("業者選び", "騙されないための、", "5箇条。"),
    "hp-hoshu-tsukutte-owari":         ("ホームページ", "作って終わりが、", "いちばん損。"),
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
}


def center(d, cx, y, text, font, fill):
    b = d.textbbox((0, 0), text, font=font)
    d.text((cx - (b[2] - b[0]) / 2, y), text, font=font, fill=fill)


def make(tag, line1, line2, path):
    img = Image.new("RGB", (W, H), (225, 238, 248))
    d = ImageDraw.Draw(img, "RGBA")
    for yy in range(H):
        t = yy / H
        d.line([(0, yy), (W, yy)], fill=(int(214 + 18 * t), int(232 + 10 * t), int(246 + 4 * t)))
    d.ellipse([-140, -180, 320, 280], outline=(14, 143, 190, 50), width=4)
    d.ellipse([980, 440, 1360, 820], outline=(0, 74, 173, 40), width=4)
    d.ellipse([1010, 90, 1090, 170], fill=(14, 143, 190, 36))
    d.ellipse([150, 520, 205, 575], fill=(0, 74, 173, 30))

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([120, 132, 1080, 552], radius=26, fill=(0, 50, 120, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    img.paste(sh, (0, 10), sh)
    d.rounded_rectangle([120, 122, 1080, 542], radius=26, fill=WHITE)

    center(d, 600, 168, "＼ " + tag + " ／", ImageFont.truetype(FM, 40), BLUE)
    f_main = ImageFont.truetype(FB, 82)
    center(d, 600, 244, line1, f_main, NAVY)
    center(d, 600, 356, line2, f_main, NAVY)
    d.rounded_rectangle([540, 476, 660, 487], radius=5, fill=BLUE)
    center(d, 600, 586, "まちのAI屋さん ｜ 長崎のAI・ホームページ相談窓口", ImageFont.truetype(FM, 32), (60, 90, 140))

    img.save(path, "WEBP", quality=85, method=6)


if __name__ == "__main__":
    for slug, (tag, l1, l2) in ARTICLES.items():
        p = os.path.join(OUT, f"thumb-{slug}.webp")
        make(tag, l1, l2, p)
        print(f"thumb-{slug}.webp  {os.path.getsize(p)//1024}KB")
    print(f"done: {len(ARTICLES)} thumbnails")
