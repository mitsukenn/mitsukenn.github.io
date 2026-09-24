# -*- coding: utf-8 -*-
"""背景あしらい比較ラボ 第2弾（波形セクション区切り × ロゴ透過ウォーターマーク）を生成する。

ChatGPTに出してもらった案（99_image_output/deco_ref/gpt_01, gpt_02）を、
実サイトのCSSトークンでそのまま実装したもの。出力は public/deco-lab2.html。
波形パスと等高線は手書きだと破綻するのでここで計算して埋め込む。
"""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "public" / "deco-lab2.html"

W = 1440  # SVG の viewBox 幅（preserveAspectRatio=none で横に伸ばす）

ACCENT = "#0e8fbe"
BRAND = "#004aad"
WHITE = "#ffffff"
BLUE1 = "#dceef8"   # 淡い水色（波の第1層）
BLUE2 = "#eaf5fb"   # さらに淡い水色（波の第2層）
BEIGE = "#f8f6f2"   # --bg-soft


# ---------- パスづくり ----------
def smooth(pts):
    """点列を横方向ハンドルのベジェで滑らかにつなぐ。"""
    d = f"M{pts[0][0]:.0f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        dx = (x1 - x0) / 2
        d += f" C{x0+dx:.1f},{y0:.1f} {x1-dx:.1f},{y1:.1f} {x1:.0f},{y1:.1f}"
    return d


def band(pts):
    """波線より上を塗りつぶす閉じたパス。"""
    return smooth(pts) + f" L{W},0 L0,0 Z"


def ys(values):
    """等間隔に並べた (x, y) 点列にする。"""
    n = len(values) - 1
    return [(W * i / n, v) for i, v in enumerate(values)]


def zigzag(base, amp, teeth, h):
    """浅いギザギザの波。上側を塗る閉じパス。"""
    d = f"M0,{base:.1f}"
    step = W / (teeth * 2)
    for i in range(1, teeth * 2 + 1):
        y = base - amp if i % 2 else base + amp
        d += f" L{step*i:.1f},{y:.1f}"
    return d + f" L{W},0 L0,0 Z"


def esc(svg):
    """CSS の url() に入れられる形へ。"""
    svg = " ".join(svg.split())
    return (svg.replace("%", "%25").replace("#", "%23")
               .replace("<", "%3C").replace(">", "%3E").replace('"', "'"))


def svg_url(inner, h):
    s = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {h}' "
         f"preserveAspectRatio='none'>{inner}</svg>")
    return f'url("data:image/svg+xml,{esc(s)}")'


# ---------- 波形6種（上端用。下端は CSS で180度回す） ----------
H = 92

# W1 ゆるやか二層
w1 = svg_url(
    f"<path fill='{BLUE1}' d='{band(ys([58, 44, 68, 46, 60]))}'/>"
    f"<path fill='{WHITE}' d='{band(ys([34, 22, 46, 24, 38]))}'/>", H)

# W2 細い青ライン一本（推し）
_p2 = ys([46, 26, 60, 30, 50])
w2 = svg_url(
    f"<path fill='{WHITE}' d='{band(_p2)}'/>"
    f"<path fill='none' stroke='{ACCENT}' stroke-width='2' opacity='.55' d='{smooth(_p2)}'/>", H)

# W3 三層の重なり
w3 = svg_url(
    f"<path fill='{BLUE1}' d='{band(ys([70, 54, 78, 58, 72]))}'/>"
    f"<path fill='{BLUE2}' d='{band(ys([54, 40, 62, 36, 56]))}'/>"
    f"<path fill='{WHITE}' d='{band(ys([32, 20, 42, 18, 34]))}'/>", H)

# W4 斜め＋細線シェーディング
_hatch = "".join(
    f"<line x1='{i*60}' y1='0' x2='{i*60-160}' y2='{H}' stroke='{ACCENT}' "
    f"stroke-width='1' opacity='.16'/>" for i in range(3, 27))
w4 = svg_url(
    f"<path fill='{BLUE1}' d='M0,0 H{W} V26 L0,86 Z'/>"
    f"<g>{_hatch}</g>"
    f"<path fill='{WHITE}' d='M0,0 H{W} V12 L0,64 Z'/>", H)

# W5 浅いギザギザ
w5 = svg_url(f"<path fill='{WHITE}' d='{zigzag(42, 11, 22, H)}'/>", H)

# W6 等高線バンド（長崎の坂・地形）
# 単一の正弦波だと「ただの縞」になるので、周波数の違う波を3つ重ねた共通の起伏を作り、
# 線ごとに振幅を変える。こうすると線が寄ったり離れたりして地形図の表情になる。
HC = 170
N = 21


def relief(t):
    return (0.62 * math.sin(2.1 * t)
            + 0.30 * math.sin(3.7 * t + 1.2)
            + 0.16 * math.sin(6.3 * t + 2.6))


_lines = []
for i in range(N):
    amp = 30 * (0.42 + 0.58 * math.sin(i * 0.5 + 0.4) ** 2)
    base = 6 + i * (HC - 14) / (N - 1)
    pts = [(W * k / 24, base + amp * relief(k / 24 * 6.0)) for k in range(25)]
    _lines.append(f"<path fill='none' stroke='{ACCENT}' stroke-width='1' "
                  f"opacity='{0.26 - i*0.007:.3f}' d='{smooth(pts)}'/>")

# 帯の下端を直線で切るとセクション色との境目に線が出るので、波で閉じる
_foot = ys([HC - 34, HC - 20, HC - 44, HC - 24, HC - 36])
_foot_d = smooth(_foot) + f" L{W},{HC} L0,{HC} Z"
w6 = svg_url(f"<rect width='{W}' height='{HC}' fill='{WHITE}'/>"
             + "".join(_lines)
             + f"<path fill='{BEIGE}' d='{_foot_d}'/>", HC)


# ---------- パターン定義 ----------
LOGO = "/assets/images/logo-mark.png"

PATTERNS = [
    ("P1", "細い青ライン波 × ロゴ右下に大きくひとつ",
     "いちばん主張が控えめ。白場を食わないので本文の読みやすさを保てる（一押し）",
     "w2", "corner"),
    ("P2", "ゆるやか二層波 × ロゴを左上と右下に散らす",
     "ベタ塗り二層。装飾感ははっきり出るが、そのぶん面積を取る",
     "w1", "scatter"),
    ("P3", "三層の重なり波 × ロゴなし",
     "波だけでどこまで持つかの検証。いちばん静か",
     "w3", "none"),
    ("P4", "浅いギザギザ波 × ロゴ右下に大きくひとつ",
     "折り紙・和紙っぽい表情。手仕事感が出るぶん少しカジュアル寄り",
     "w5", "corner"),
    ("P5", "斜め波＋細線シェーディング × ロゴを散らす",
     "動きがいちばん強い。連続で使うとうるさくなる",
     "w4", "scatter"),
    ("P6", "等高線バンド × ロゴをタイル状に",
     "長崎の坂の地形。CTAや下層ページの見出し帯など、切り札として1〜2か所に",
     "w6", "tile"),
]

CARDS = """
      <div class="cards">
        <div class="card"><span class="card__no">1</span><h3>AIシステム開発</h3><p>Excelの管理表を、そのまま使えるアプリに。現場の手順に合わせて作ります。</p></div>
        <div class="card"><span class="card__no">2</span><h3>AI活用アドバイザー</h3><p>「どこから手をつけるか」から一緒に。月1回の相談でも大丈夫です。</p></div>
        <div class="card"><span class="card__no">3</span><h3>ホームページ制作</h3><p>作って終わりにしない。更新のしやすさまで含めてお手伝いします。</p></div>
      </div>
      <div class="center"><a class="btn" href="#">まずは無料で相談する</a></div>
"""

blocks = []
for key, title, note, wave, wm in PATTERNS:
    wmclass = "" if wm == "none" else f" wm wm--{wm}"
    blocks.append(f"""
<div class="lab-label"><div class="container"><span class="lab-tag">{key}</span><b>{title}</b><span>{note}</span></div></div>
<section class="pat pat--{wave}{wmclass}">
  <span class="wv wv--top"></span>
  <span class="wv wv--bot"></span>
  <div class="container">
    <div class="section-title"><span class="section-title__sub">できること</span><h2>まちのAI屋さんにできること</h2></div>
{CARDS}  </div>
</section>
<section class="between"><div class="container"><p>↑↓ 前後の白いセクションとのつながり方を見るための余白です</p></div></section>""")

HTML = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>波形×ロゴ透過 比較ラボ｜まちのAI屋さん</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{
  --accent:{ACCENT}; --accent-soft:#e4f5fc; --accent-dark:#0a6e93; --brand:{BRAND};
  --text:#333a40; --text-weak:#6b7580; --bg:#fff; --bg-soft:{BEIGE}; --border:#e6e2db;
  --radius:16px; --shadow:0 4px 20px rgba(60,50,40,.08);
  --font-body:'Zen Kaku Gothic New','Hiragino Kaku Gothic ProN','Meiryo',sans-serif;
  --wave-h:{H}px; --contour-h:{HC}px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--font-body);color:var(--text);background:var(--bg);line-height:1.9;font-size:17px;-webkit-font-smoothing:antialiased}}
img{{max-width:100%;height:auto;display:block}}

.lab-head{{background:#212a33;color:#fff;padding:28px 20px;text-align:center}}
.lab-head h1{{font-size:20px;letter-spacing:.06em}}
.lab-head p{{font-size:14px;opacity:.75;margin-top:6px}}
.lab-label{{background:#212a33;color:#fff;padding:14px 20px}}
.lab-label .container{{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap}}
.lab-label b{{font-size:17px;letter-spacing:.05em}}
.lab-label span{{font-size:13px;opacity:.7}}
.lab-tag{{background:var(--accent);border-radius:999px;padding:2px 12px;font-size:12px;font-weight:700}}

.container{{max-width:1080px;margin:0 auto;padding:0 20px}}
.section-title{{text-align:center;margin-bottom:40px}}
.section-title h2{{font-size:28px;font-weight:700;letter-spacing:.05em}}
.section-title__sub{{display:block;color:var(--accent);font-size:13px;font-weight:700;letter-spacing:.15em;margin-bottom:6px}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
.card{{background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:28px 24px;box-shadow:var(--shadow)}}
.card h3{{font-size:19px;margin-bottom:10px}}
.card p{{font-size:15px;color:var(--text-weak);line-height:1.8}}
.card__no{{display:inline-flex;width:38px;height:38px;border-radius:50%;background:var(--accent-soft);color:var(--accent);font-weight:700;align-items:center;justify-content:center;margin-bottom:14px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;padding:16px 36px;border-radius:999px;font-weight:700;background:var(--accent);color:#fff;text-decoration:none;box-shadow:var(--shadow);margin-top:32px}}
.center{{text-align:center}}
.between{{padding:56px 0;text-align:center}}
.between p{{font-size:13px;color:#b9b3aa}}

/* ---------- 波形セクション区切りの土台 ----------
   .wv--top / .wv--bot に SVG を敷く。下端は同じ SVG を180度回して使う。 */
.pat{{position:relative;background:var(--bg-soft);overflow:hidden;
  padding:calc(var(--wave-h) + 40px) 0 calc(var(--wave-h) + 40px)}}
.pat > .container{{position:relative;z-index:1}}
.wv{{position:absolute;left:0;right:0;height:var(--wave-h);pointer-events:none;
  background-repeat:no-repeat;background-size:100% 100%}}
.wv--top{{top:-1px}}
.wv--bot{{bottom:-1px;transform:rotate(180deg)}}

.pat--w1 .wv{{background-image:{w1}}}
.pat--w2 .wv{{background-image:{w2}}}
.pat--w3 .wv{{background-image:{w3}}}
.pat--w4 .wv{{background-image:{w4}}}
.pat--w5 .wv{{background-image:{w5}}}

/* 等高線バンドだけ背が高い */
.pat--w6{{padding:calc(var(--contour-h) + 24px) 0 calc(var(--wave-h) + 40px)}}
.pat--w6 .wv--top{{height:var(--contour-h);background-image:{w6}}}
.pat--w6 .wv--bot{{background-image:{w2}}}

/* ---------- ロゴ透過ウォーターマーク ---------- */
.wm::before,.wm::after{{content:'';position:absolute;pointer-events:none}}

/* 右下に大きくひとつ */
.wm--corner::after{{width:400px;height:400px;right:-64px;bottom:-96px;
  background:url("{LOGO}") no-repeat center/contain;opacity:.055}}

/* 左上と右下に散らす */
.wm--scatter::before{{width:210px;height:210px;left:-40px;top:{H+10}px;
  background:url("{LOGO}") no-repeat center/contain;opacity:.045;transform:rotate(-10deg)}}
.wm--scatter::after{{width:340px;height:340px;right:-56px;bottom:-72px;
  background:url("{LOGO}") no-repeat center/contain;opacity:.06}}

/* タイル状に小さく繰り返す */
.wm--tile::before{{inset:0;background:url("{LOGO}") repeat;background-size:86px 86px;opacity:.05}}

@media(max-width:720px){{
  :root{{--wave-h:52px;--contour-h:110px}}
  .cards{{grid-template-columns:1fr}}
  .wm--corner::after{{width:230px;height:230px}}
  .wm--scatter::before{{width:130px;height:130px}}
  .wm--scatter::after{{width:200px;height:200px}}
  .wm--tile::before{{background-size:84px 84px}}
}}
</style>
</head>
<body>

<div class="lab-head">
  <h1>波形セクション区切り × ロゴ透過ウォーターマーク</h1>
  <p>ChatGPTに出してもらった案を、実サイトのCSSトークンでそのまま実装した6パターン。好きな記号を教えてください</p>
</div>
{''.join(blocks)}
<div class="lab-head" style="padding:40px 20px">
  <p style="opacity:1;font-size:15px">波形もロゴ透過もCSSとSVGだけで描いているので、画像ファイルは1つも増えません（ロゴは既存の logo-mark.png を流用）。<br>色は --accent 変数に連動するので、あとからテーマ色を変えても自動で追従します。</p>
</div>

</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"written: {OUT}  ({len(HTML)/1024:.0f} KB)")
