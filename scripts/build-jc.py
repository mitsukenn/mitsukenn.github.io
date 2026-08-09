# -*- coding: utf-8 -*-
"""JC特設ページのビルド（暗号化）スクリプト。

jc-src/index.html（平文・gitignore済み）を StatiCrypt でAES暗号化し、
public/jc/index.html（暗号文のみ・コミット対象）を生成する。

使い方:
    python scripts/build-jc.py

パスワード変更:
    jc-src/password.txt を書き換えて再実行するだけ。
    ※ソルトは jc-src/.staticrypt.json に固定保存（変更すると全員の
      「30日間記憶」と共有リンクが無効になるので、原則触らない）
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "jc-src"
OUT = ROOT / "public" / "jc"

# utf-8-sig: PowerShell等がBOM付きで保存しても不可視文字がパスワードに混ざらないように
password = (SRC / "password.txt").read_text(encoding="utf-8-sig").strip()
npx = shutil.which("npx") or shutil.which("npx.cmd")

cmd = [
    npx, "--yes", "staticrypt", "index.html",
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

env = dict(**__import__("os").environ, STATICRYPT_PASSWORD=password)
subprocess.run(cmd, cwd=SRC, env=env, check=True)

# クローラー向けnoindexをパスワード入力画面のheadに注入（テンプレは素のHTMLなので）
out_html = OUT / "index.html"
html = out_html.read_text(encoding="utf-8")
if 'name="robots"' not in html:
    html = html.replace(
        "<head>", '<head>\n    <meta name="robots" content="noindex, nofollow" />', 1
    )
    out_html.write_text(html, encoding="utf-8")

print("OK:", out_html, f"({out_html.stat().st_size // 1024} KB)")
print("共有リンク作成: cd jc-src; npx staticrypt index.html --share https://machino-ai.jp/jc/")
