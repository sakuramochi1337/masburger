#!/usr/bin/env python3
"""index.html をダブルクリック（file://）で開いても素材が読めるように、
画像・3Dモデル・効果音を data URI にして assets/bundle.js へまとめる。
（file:// だとブラウザが別ファイルの画像やモデルの読み込みを止めるため）

素材を差し替えたら作り直す:  python3 tools/make_bundle.py
サーバー（GitHub Pages など）で開くときは bundle.js は読まれない。"""
import base64, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIME = {'.jpg': 'image/jpeg', '.png': 'image/png', '.glb': 'model/gltf-binary', '.mp3': 'audio/mpeg'}
DIRS = ['assets/tex', 'assets/chars', 'assets/city', 'sfx']

out = {}
for d in DIRS:
    full = os.path.join(ROOT, d)
    if not os.path.isdir(full):
        continue
    for name in sorted(os.listdir(full)):
        ext = os.path.splitext(name)[1].lower()
        if ext not in MIME:
            continue
        with open(os.path.join(full, name), 'rb') as f:
            out[f'{d}/{name}'] = f'data:{MIME[ext]};base64,' + base64.b64encode(f.read()).decode('ascii')

dst = os.path.join(ROOT, 'assets', 'bundle.js')
with open(dst, 'w', encoding='utf-8') as f:
    f.write('/* tools/make_bundle.py が生成。file:// で開いたときだけ読まれる */\n')
    f.write('window.MB_BUNDLE=' + json.dumps(out, separators=(',', ':')) + ';\n')
print(f'{len(out)} files -> {os.path.relpath(dst, ROOT)} ({os.path.getsize(dst) / 1e6:.1f} MB)')
