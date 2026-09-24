# -*- coding: utf-8 -*-
"""背景あしらいのCSS（src/styles/deco.css）を生成する。

オーナー選定（2026-08-04）の4点を実装する。
  1. 波形のセクション区切り（ゆるやか二層波）… .section--wave
  2. 方眼グリッド（設計図っぽさ）          … .section--grid
  3. ロゴの透過ウォーターマーク（散らし）  … .section--logo
  4. 気づくか気づかないレベルの極薄グラデ  … .section（全セクション共通のベース）

波形のパスは手書きだと破綻するのでここで計算してdata URIに焼き込む。
波の高さや振幅を変えたいときはこのファイルの数値を直して再生成すること。
    python scripts/build-deco-css.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "styles" / "deco.css"

W = 1440          # SVGのviewBox幅（preserveAspectRatio=noneで横に伸ばす）
H = 92            # 波形の高さ（CSS側の --wave-h と合わせる）

ACCENT = "#0e8fbe"
BRAND = "#004aad"
WHITE = "#ffffff"
BLUE1 = "#dceef8"   # 二層波の下の層
LOGO = "/assets/images/logo-mark.png"

# 波の稜線。上端用に「白がどこまで下りてくるか」をy座標で書く
WAVE_LOWER = [58, 44, 68, 46, 60]   # 淡い水色の層
WAVE_UPPER = [34, 22, 46, 24, 38]   # 白の層


def smooth(pts):
    """点列を横方向ハンドルのベジェで滑らかにつなぐ。"""
    d = f"M{pts[0][0]:.0f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        dx = (x1 - x0) / 2
        d += f" C{x0+dx:.1f},{y0:.1f} {x1-dx:.1f},{y1:.1f} {x1:.0f},{y1:.1f}"
    return d


def ys(values, flip=False):
    n = len(values) - 1
    return [(W * i / n, (H - v) if flip else v) for i, v in enumerate(values)]


def fill_above(values):
    return smooth(ys(values)) + f" L{W},0 L0,0 Z"


def fill_below(values):
    return smooth(ys(values, flip=True)) + f" L{W},{H} L0,{H} Z"


def esc(svg):
    svg = " ".join(svg.split())
    return (svg.replace("%", "%25").replace("#", "%23")
               .replace("<", "%3C").replace(">", "%3E").replace('"', "'"))


def svg_url(inner):
    s = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' "
         f"preserveAspectRatio='none'>{inner}</svg>")
    return f'url("data:image/svg+xml,{esc(s)}")'


# 上端用：白 → 淡い水色 → セクション色
wave_top = svg_url(
    f"<path fill='{BLUE1}' d='{fill_above(WAVE_LOWER)}'/>"
    f"<path fill='{WHITE}' d='{fill_above(WAVE_UPPER)}'/>")

# 下端用：上下反転（セクション色 → 淡い水色 → 白）
wave_bottom = svg_url(
    f"<path fill='{BLUE1}' d='{fill_below(WAVE_LOWER)}'/>"
    f"<path fill='{WHITE}' d='{fill_below(WAVE_UPPER)}'/>")

# ---------- 回路トレース（サーキット）のタイル ----------
# 参考イメージ（オーナー提示・2026-08-04）の基板パターンを再現する。
# グリッド上をマンハッタン移動するランダムウォークで配線を引き、端点に丸ノードを置く。
# 座標をタイル幅で剰余して進めたうえで、同じ図形を3x3に並べて描くことで継ぎ目なく敷ける。
import random

TILE = 480
GRID = 16                      # 1タイルあたりのマス数（細かいほど基板らしくなる）
CELL = TILE // GRID            # = 30px
random.seed(20260804)          # 毎回同じ絵になるよう固定
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def _turn(d):
    return random.choice([(d[1], d[0]), (-d[1], -d[0])])


def _circuit_parts():
    """配線・端点ノード・ビア（丸穴）・分岐スタブを作る。"""
    segs, nodes, vias, pads = [], [], [], []
    for _ in range(22):
        x, y = random.randrange(GRID), random.randrange(GRID)
        d = random.choice(DIRS)
        nodes.append((x, y))
        for step in range(random.randint(6, 14)):
            # 2〜3マス進んでは直角に折れる。長い直進を作らないのが基板らしさの肝
            run = random.randint(1, 3)
            for _ in range(run):
                nx, ny = x + d[0], y + d[1]
                segs.append((x, y, nx, ny))
                x, y = nx % GRID, ny % GRID
            if random.random() < 0.18:
                vias.append((x, y))
            # 短い枝を生やして先端にパッドを置く
            if random.random() < 0.22:
                b = _turn(d)
                bx, by = x + b[0], y + b[1]
                segs.append((x, y, bx, by))
                pads.append((bx % GRID, by % GRID))
            d = _turn(d)
        nodes.append((x, y))
    return segs, nodes, vias, pads


_segs, _nodes, _vias, _pads = _circuit_parts()
_body = "".join(
    f"<path d='M{a*CELL},{b*CELL} L{c*CELL},{d*CELL}'/>" for a, b, c, d in _segs)
_body += "".join(f"<circle cx='{x*CELL}' cy='{y*CELL}' r='3.4' fill='{ACCENT}' "
                 f"stroke='none' opacity='.30'/>" for x, y in _nodes)
_body += "".join(f"<circle cx='{x*CELL}' cy='{y*CELL}' r='4.6' fill='none'/>"
                 for x, y in _vias)
_body += "".join(f"<rect x='{x*CELL-3}' y='{y*CELL-3}' width='6' height='6' "
                 f"fill='{ACCENT}' stroke='none' opacity='.26'/>" for x, y in _pads)
# 3x3に複製して、タイル境界をまたぐ配線を継ぎ目なくつなぐ。
# 図形を9回書き出すとCSSが230KBまで膨らむので、defsに1つ置いて <use> で参照する
# '#c' は esc() が %23c に変換する（先に書くと %25 で二重エスケープされるので生で書く）
_grid9 = "".join(f"<use href='#c' x='{dx*TILE}' y='{dy*TILE}'/>"
                 for dx in (-1, 0, 1) for dy in (-1, 0, 1))
_circuit_svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{TILE}' height='{TILE}' "
                f"viewBox='0 0 {TILE} {TILE}'>"
                f"<defs><g id='c'>{_body}</g></defs>"
                f"<g fill='none' stroke='{ACCENT}' stroke-width='1.2' opacity='.17' "
                f"stroke-linecap='round'>{_grid9}</g></svg>")
CIRCUIT = f'url("data:image/svg+xml,{esc(_circuit_svg)}")'

# 極薄グラデ。上げすぎると「色を塗った」感が出るので .05 前後が上限
GRAD = ("radial-gradient(900px 480px at 14% -12%, rgba(14, 143, 190, 0.055), transparent 62%),\n"
        "    radial-gradient(760px 420px at 92% 108%, rgba(0, 74, 173, 0.04), transparent 60%)")

CSS = f"""/* ============================================================
   背景あしらい（波形の区切り／方眼グリッド／ロゴ透過／極薄グラデ）

   このファイルは scripts/build-deco-css.py が生成しています。
   手で編集せず、スクリプト側の数値を直して再生成してください。
       python scripts/build-deco-css.py
   ============================================================ */

:root {{
  --wave-h: {H}px;
}}

/* ---------- 0. 回路トレース（基板パターン）のページ全面レイヤー ----------
   ページ全体の下敷き。左右の余白側だけに出るようマスクを掛けているので、
   読み幅（中央）には線が入らない。背景色を持つセクション（--bg-soft や CTA）は
   この層を塗りつぶすので、白い面だけに現れて自然な強弱がつく。 */
body {{
  position: relative;
}}

body::before {{
  content: '';
  position: absolute;
  inset: 0;
  z-index: -1;   /* 本文より奥。ここを外すと絶対配置なので本文の上に出る */
  pointer-events: none;
  background-image: {CIRCUIT};
  background-size: {TILE}px {TILE}px;
  background-repeat: repeat;
  -webkit-mask-image: linear-gradient(90deg, #000 0%, transparent 24%, transparent 76%, #000 100%);
  mask-image: linear-gradient(90deg, #000 0%, transparent 24%, transparent 76%, #000 100%);
}}

/* ---------- 4. 全セクション共通の極薄グラデーション ----------
   「気づくか気づかないか」の濃さで無地感だけを消す。
   背景色は塗らないので .section--soft のベージュにもそのまま乗る */
.section {{
  background-image:
    {GRAD};
  background-repeat: no-repeat;
}}

/* あしらいを持つセクションの共通土台 */
.section--wave,
.section--grid,
.section--logo {{
  position: relative;
  overflow: hidden;
}}

.section--wave > .container,
.section--grid > .container,
.section--logo > .container {{
  position: relative;
  z-index: 1;
}}

/* ---------- 1. 波形のセクション区切り ----------
   上下端に二層の波を敷く。白い層が隣接セクション（白）と繋がるので、
   ベージュのセクションに付けると切り替わりが波になる */
.section--wave {{
  padding: calc(56px + var(--wave-h)) 0;
  background-image:
    {wave_top},
    {wave_bottom},
    {GRAD};
  background-repeat: no-repeat, no-repeat, no-repeat, no-repeat;
  background-position: top center, bottom center, 0 0, 0 0;
  background-size:
    100% var(--wave-h),
    100% var(--wave-h),
    auto,
    auto;
}}

/* ---------- 2. 方眼グリッド（設計図っぽさ） ----------
   中央はマスクで抜くので、本文や見出しの上には線が来ない */
.section--grid::before {{
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(14, 143, 190, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(14, 143, 190, 0.07) 1px, transparent 1px);
  background-size: 32px 32px, 32px 32px;
  -webkit-mask-image: radial-gradient(680px 400px at 50% 50%, transparent 10%, #000 74%);
  mask-image: radial-gradient(680px 400px at 50% 50%, transparent 10%, #000 74%);
}}

/* ---------- 3. ロゴのウォーターマーク（白ベタ・左上と右下に散らす） ----------
   青いロゴを薄く敷くと «透けて汚れた青» に見えるので、filter で白ベタに変換して置く。
   白なので白背景のセクションでは消える。必ずベージュ（--bg-soft）か
   水色（--accent-soft）の面と組み合わせること */
.section--logo::after {{
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: url("{LOGO}"), url("{LOGO}");
  background-repeat: no-repeat, no-repeat;
  background-position: left -46px top 56px, right -58px bottom -78px;
  background-size: 200px auto, 330px auto;
  /* brightness(0) で一度真っ黒にしてから invert(1) で白へ。アルファ（ロゴの形）は保たれる */
  filter: brightness(0) invert(1);
  opacity: 0.8;
}}

@media (max-width: 720px) {{
  :root {{
    --wave-h: 52px;
  }}
  .section--wave {{
    padding: calc(40px + var(--wave-h)) 0;
  }}
  .section--grid::before {{
    background-size: 24px 24px, 24px 24px;
    -webkit-mask-image: radial-gradient(300px 320px at 50% 50%, transparent 6%, #000 78%);
    mask-image: radial-gradient(300px 320px at 50% 50%, transparent 6%, #000 78%);
  }}
  .section--logo::after {{
    background-position: left -34px top 40px, right -40px bottom -50px;
    background-size: 130px auto, 210px auto;
  }}
}}

/* 動きを減らす設定の人にも影響しない静的な装飾なので prefers-reduced-motion の分岐は不要 */
"""

OUT.write_text(CSS, encoding="utf-8")
print(f"written: {OUT}  ({len(CSS)/1024:.1f} KB)")
