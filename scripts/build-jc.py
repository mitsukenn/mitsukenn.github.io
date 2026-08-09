# -*- coding: utf-8 -*-
"""JC特設ページのビルド（暗号化）スクリプト。

jc-src/ 直下の各HTML（平文・gitignore済み）を StatiCrypt でAES暗号化し、
public/jc/ （暗号文のみ・コミット対象）に出力する。

- <!--SHARED-CSS--> は jc-src/_shared-head.html の中身に置換される
- <img src="assets/..."> は base64 データURIとしてHTMLに埋め込まれる
  （画像も暗号化の中に入るので、画像だけ丸見えになることがない）
- 「_」始まりのHTMLはビルド対象外（部品・下書き用）

使い方:
    python scripts/build-jc.py

パスワード変更:
    jc-src/password.txt を書き換えて再実行するだけ。
    ※ソルトは jc-src/.staticrypt.json に固定保存（変更すると全員の
      「30日間記憶」と共有リンクが無効になるので、原則触らない）
"""
import base64
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "jc-src"
OUT = ROOT / "public" / "jc"

MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}

# utf-8-sig: PowerShell等がBOM付きで保存しても不可視文字がパスワードに混ざらないように
password = (SRC / "password.txt").read_text(encoding="utf-8-sig").strip()
shared_css = (SRC / "_shared-head.html").read_text(encoding="utf-8-sig")
npx = shutil.which("npx") or shutil.which("npx.cmd")

pages = [p for p in sorted(SRC.glob("*.html")) if not p.name.startswith("_")]
if not pages:
    sys.exit("jc-src/ にビルド対象のHTMLがありません")


def inline_assets(html: str, page_name: str) -> str:
    def repl(m):
        rel = m.group(1)
        f = SRC / rel
        if not f.exists():
            print(f"  警告: {page_name} が参照する {rel} が見つかりません（そのまま残します）")
            return m.group(0)
        data = base64.b64encode(f.read_bytes()).decode("ascii")
        mime = MIME.get(f.suffix.lower(), "application/octet-stream")
        return m.group(0).replace(f'src="{rel}"', f'src="data:{mime};base64,{data}"')

    return re.sub(r'<img[^>]+src="(assets/[^"]+)"', repl, html)


CONFIG = SRC / ".staticrypt.json"

with tempfile.TemporaryDirectory() as tmp:
    tmpdir = pathlib.Path(tmp)
    # staticryptは -c をcwd相対で扱うので、ソルト設定を作業ディレクトリに持ち込む
    if CONFIG.exists():
        shutil.copy2(CONFIG, tmpdir / ".staticrypt.json")
    for page in pages:
        html = page.read_text(encoding="utf-8-sig")
        html = html.replace("<!--SHARED-CSS-->", shared_css)
        html = inline_assets(html, page.name)
        (tmpdir / page.name).write_text(html, encoding="utf-8", newline="\n")

    cmd = [
        npx, "--yes", "staticrypt", *[p.name for p in pages],
        "-d", str(OUT),
        "-c", ".staticrypt.json",
        "--remember", "30",
        "--short",
        "--template-title", "議案づくり×AI 実践メモ（JC向け）",
        "--template-instructions", "JCメンバー向けの非公開ページです。共有されたパスワードを入力してください。",
        "--template-button", "開く",
        "--template-placeholder", "パスワード",
        "--template-error", "パスワードが違います",
        "--template-remember", "この端末で30日間パスワードを記憶する",
        "--template-color-primary", "#0e8fbe",
        "--template-color-secondary", "#004aad",
    ]
    env = dict(**os.environ, STATICRYPT_PASSWORD=password)
    subprocess.run(cmd, cwd=tmpdir, env=env, check=True)
    # 初回生成されたソルトを jc-src に残す（以後このソルトで固定）
    generated = tmpdir / ".staticrypt.json"
    if generated.exists() and not CONFIG.exists():
        shutil.copy2(generated, CONFIG)

# クローラー向けnoindexをパスワード入力画面のheadに注入（テンプレは素のHTMLなので）
for page in pages:
    out_html = OUT / page.name
    html = out_html.read_text(encoding="utf-8")
    if 'name="robots"' not in html:
        html = html.replace(
            "<head>", '<head>\n    <meta name="robots" content="noindex, nofollow" />', 1
        )
        out_html.write_text(html, encoding="utf-8", newline="\n")
    print(f"OK: {out_html.name} ({out_html.stat().st_size // 1024} KB)")

print("共有リンク作成: cd jc-src; npx staticrypt index.html --share https://machino-ai.jp/jc/")
