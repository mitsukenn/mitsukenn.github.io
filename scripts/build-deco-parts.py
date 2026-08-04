# -*- coding: utf-8 -*-
"""ChatGPTが生成した背景パーツ（透過PNG）を、Webで使える素材に切り出す。

入力: 99_image_output/deco_parts/raw/part01..NN.png（1536x1024・RGBA）
出力: machino-ai-site/public/assets/images/deco/*.webp
      99_image_output/deco_parts/candidates/*.webp（不採用ぶんの控え）

■ なぜ「切り出す」のか（2026-08-04 の作り直し）
生成される素材は「16:9の1枚絵の四隅にパーツが配置された絵」になっている。
これをセクション全面に background-size:100% 100% で敷くと、
セクションの縦横比が素材と違うぶんだけ絵が潰れる。
記事ページのように縦4000pxのセクションでは、3:2の素材が極端に間延びして崩れた。

そこで1枚絵から「絵が描かれている塊」だけを個別に切り出し、
CSSでは原寸比のまま（background-size: <px> auto）四隅に置く。
これなら親要素の縦横比がいくら変わっても絵は一切歪まない。

やっていること
  1. 暗い背景用に「白インク」で描かれた素材をブランド青へ置換
  2. アルファを粗いグリッドに落として連結成分をとり、塊ごとに切り出す
  3. 塊の重心から、どの隅に置くべきかを判定して名前に付ける（tl/tr/bl/br）
  4. 長辺を詰めて alpha 付き WebP で書き出す
"""
import colorsys
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT.parent / "99_image_output" / "deco_parts" / "raw"
OUT = ROOT / "public" / "assets" / "images" / "deco"
# 実際にCSSで使っていない素材まで public に置くと、使わない画像まで本番へ配信されてしまう。
# 候補としては残したいので、未使用分はサイトの外（成果物フォルダ）へ書き出す
POOL = ROOT.parent / "99_image_output" / "deco_parts" / "candidates"
OUT.mkdir(parents=True, exist_ok=True)
POOL.mkdir(parents=True, exist_ok=True)

ACCENT = (14, 143, 190)   # --accent #0e8fbe
CELL = 8                  # 連結成分をとるときの粗いグリッドの1マス(px)
MIN_CELLS = 26            # これ未満の塊はノイズとして捨てる
GAP = 3                   # この距離(マス)以内の塊は同じパーツとみなす（点描対策）
MAX_EDGE = 560            # 切り出し後の長辺。隅に置く飾りなので大きさは要らない
QUALITY = 78
# 1枚1パーツの素材は細い線が密に入っていてWebPが効きにくい。
# 薄く敷く飾りなので、解像度と画質を落として転送量を優先する
SINGLE_EDGE = 440
SINGLE_QUALITY = 70

NAMES = {
    1: "diagonal-halftone", 2: "corner-bracket", 3: "halftone-blob", 4: "circuit-lines",
    5: "network-mesh", 6: "hairline", 7: "soft-glow", 8: "corner-grid",
    9: "dot-gradient", 10: "corner-diagonal",
    # --- 2バッチ目（2026-08-04 追加分） ---
    11: "corner-wedge", 12: "diagonal-fill", 13: "streak", 14: "mesh-fill",
    15: "hairline-fine", 16: "soft-field", 17: "corner-frame", 18: "corner-line",
    19: "grid-corner", 20: "bracket-blob",
    # --- 3バッチ目（2026-08-04）。プロンプトを「1枚に1パーツ・正方形・青のみ・線画のみ」に
    #     変えてもらったぶん。切り出し不要でそのまま使える ---
    21: "frame-circuit", 22: "wire-corner", 23: "dot-frame", 24: "dot-diagonal",
    25: "hatch-diagonal", 26: "target", 27: "flow", 28: "scale-line",
    29: "grid-bracket", 30: "wave-graph",
}

# 1枚に1パーツで描かれている素材。連結成分で切り出すとバラバラになってしまうので、
# トリムだけして丸ごと使う（part21以降がこれ）
SINGLE = set(range(21, 31))

# ベタ塗りが主役の素材（*-fill / *-wedge / *-blob / mesh 等）は、
# 明るい背景では面積が大きすぎて悪目立ちするので採用しない
# 3バッチ目（1枚1パーツ・青のみ・線画のみ）で作り直したものに一本化する。
# 1〜2バッチ目は切り出しが必要なうえ、線の太さや彩度がバラつくので候補プールに戻した。
# 全部を public に置くと1MB近くになるのも理由（下のサイズ調整と合わせて約1/3に収めている）。
# dot-frame と grid-bracket は枠の内側が密なドットで埋まっているため、
# 200〜300pxで置くとドットが潰れて「青い四角い塊」に見える。外した。
# （重い2枚でもあり、これで public は約340KB→200KB台に落ちる）
USED = {"frame-circuit", "wire-corner", "dot-diagonal",
        "hatch-diagonal", "target", "flow", "scale-line",
        "wave-graph", "hairline-fine"}


def ink_is_white(im):
    """不透明画素の平均色が白に近い＝暗背景用の素材かを判定する。"""
    px = [p for p in im.get_flattened_data() if p[3] > 200]
    if not px:
        return False
    n = len(px)
    r, g, b = (sum(p[i] for p in px) / n / 255 for i in range(3))
    _, s, v = colorsys.rgb_to_hsv(r, g, b)
    return s < 0.16 and v > 0.82


def recolor(im, rgb):
    """アルファ（＝形）を保ったまま、インクの色だけ差し替える。"""
    a = im.getchannel("A")
    solid = Image.new("RGB", im.size, rgb)
    solid.putalpha(a)
    return solid


def clusters(im):
    """アルファのある領域を粗いグリッドに落として、連結した塊のbboxを返す。"""
    a = im.getchannel("A")
    gw, gh = (im.width + CELL - 1) // CELL, (im.height + CELL - 1) // CELL
    small = a.resize((gw, gh), Image.BOX)
    filled = [[small.getpixel((x, y)) > 10 for y in range(gh)] for x in range(gw)]

    seen = [[False] * gh for _ in range(gw)]
    boxes = []
    for sx in range(gw):
        for sy in range(gh):
            if not filled[sx][sy] or seen[sx][sy]:
                continue
            q = deque([(sx, sy)])
            seen[sx][sy] = True
            cells = []
            while q:
                x, y = q.popleft()
                cells.append((x, y))
                for dx in range(-GAP, GAP + 1):
                    for dy in range(-GAP, GAP + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < gw and 0 <= ny < gh and filled[nx][ny] and not seen[nx][ny]:
                            seen[nx][ny] = True
                            q.append((nx, ny))
            if len(cells) < MIN_CELLS:
                continue
            xs = [c[0] for c in cells]
            ys = [c[1] for c in cells]
            boxes.append((min(xs) * CELL, min(ys) * CELL,
                          min((max(xs) + 1) * CELL, im.width),
                          min((max(ys) + 1) * CELL, im.height)))
    return boxes


def anchor_of(box, size):
    """塊の重心から、置くべき隅を決める。"""
    cx = (box[0] + box[2]) / 2 / size[0]
    cy = (box[1] + box[3]) / 2 / size[1]
    return ("t" if cy < 0.5 else "b") + ("l" if cx < 0.5 else "r")


rows = []
for i in sorted(NAMES):
    src = RAW / f"part{i:02d}.png"
    if not src.exists():
        continue
    im = Image.open(src).convert("RGBA")
    name = NAMES[i]
    used = name in USED

    if ink_is_white(im):
        im = recolor(im, ACCENT)

    if i in SINGLE:
        boxes = [(0, 0, im.width, im.height)]      # 丸ごと1パーツ
    else:
        boxes = clusters(im)
        if not boxes:
            continue
        boxes.sort(key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
        boxes = boxes[:4]                          # 大きい塊から最大4つまで

    taken = {}
    for box in boxes:
        piece = im.crop(box)
        bb = piece.getbbox()          # グリッド分の余白をきっちり落とす
        if bb:
            piece = piece.crop(bb)
        edge = SINGLE_EDGE if i in SINGLE else MAX_EDGE
        if max(piece.size) > edge:
            sc = edge / max(piece.size)
            piece = piece.resize((max(1, round(piece.width * sc)),
                                  max(1, round(piece.height * sc))), Image.LANCZOS)

        if i in SINGLE:
            dst = (OUT if used else POOL) / f"{name}.webp"
            suffix = "-"
        else:
            a = anchor_of(box, im.size)
            taken[a] = taken.get(a, 0) + 1
            suffix = a if taken[a] == 1 else f"{a}{taken[a]}"
            dst = (OUT if used else POOL) / f"{name}-{suffix}.webp"
        piece.save(dst, "WEBP",
                   quality=SINGLE_QUALITY if i in SINGLE else QUALITY, method=6)
        rows.append((name, suffix, piece.size, dst.stat().st_size / 1024, used))

for name, suf, size, kb, used in rows:
    print(f"{name:20s} {suf:3s} {str(size):11s} {kb:6.1f} KB "
          f"{'[public]' if used else '[pool]'}")
print(f"\npublic {sum(1 for r in rows if r[4])} ピース / "
      f"{sum(r[3] for r in rows if r[4]):.0f} KB")
