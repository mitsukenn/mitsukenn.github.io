# -*- coding: utf-8 -*-
"""補足画像52枚をwebp変換して記事に挿入する。
1) 99_image_output/sup/*.png → public/assets/images/blog/sup-*.webp（1200px幅）
2) SPECのアンカー直前に画像Markdownを挿入（既に挿入済みならスキップ）
"""
import io, os
from PIL import Image
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec_path = os.path.join(HERE, "sup-images-spec.py")
spec_mod = importlib.util.spec_from_file_location("spec", spec_path)
m = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(m)
SPEC = m.SPEC

SRC = os.path.abspath(os.path.join(HERE, "..", "..", "99_image_output", "sup"))
DST = os.path.abspath(os.path.join(HERE, "..", "public", "assets", "images", "blog"))
BLOG = os.path.abspath(os.path.join(HERE, "..", "src", "content", "blog"))

converted, inserted, missing = 0, 0, []
for slug, items in SPEC.items():
    md_path = os.path.join(BLOG, slug + ".md")
    with io.open(md_path, encoding="utf-8") as f:
        text = f.read()
    changed = False
    for num, _prompt, anchor, alt in items:
        name = f"sup-{slug}-{num}"
        png = os.path.join(SRC, name + ".png")
        webp = os.path.join(DST, name + ".webp")
        if os.path.exists(png) and not os.path.exists(webp):
            img = Image.open(png).convert("RGB")
            w, h = img.size
            img = img.resize((1200, round(h * 1200 / w)), Image.LANCZOS)
            img.save(webp, "WEBP", quality=82, method=6)
            converted += 1
        if not os.path.exists(webp):
            missing.append(name)
            continue
        md_img = f"![{alt}](/assets/images/blog/{name}.webp)"
        if md_img in text:
            continue
        if anchor not in text:
            missing.append(name + " (anchor not found)")
            continue
        text = text.replace(anchor, md_img + "\n\n" + anchor, 1)
        inserted += 1
        changed = True
    if changed:
        with io.open(md_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

print(f"converted={converted} inserted={inserted}")
print("issues:", missing if missing else "none")
