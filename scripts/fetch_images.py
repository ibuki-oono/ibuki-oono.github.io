#!/usr/bin/env python3
"""Download the four original project photos, preserving existing local files."""
import json
from pathlib import Path
import subprocess
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent


def fetch(project):
    target = ROOT / 'image' / 'projects' / f'{project["slug"]}.jpg'
    if target.is_file():
        print(f'SKIP {project["slug"]}: 保存済み')
        return True
    request = Request(project['image'], headers={'User-Agent': 'ibuki-portfolio/1.0'})
    try:
        with urlopen(request, timeout=30) as response:
            data = response.read(20 * 1024 * 1024 + 1)
        if not data.startswith(b'\xff\xd8\xff'):
            raise ValueError('JPEG形式の写真を取得できませんでした')
        if len(data) > 20 * 1024 * 1024:
            raise ValueError('画像サイズが20MBを超えています')
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.jpg.download')
        try:
            temporary.write_bytes(data)
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
        print(f'OK   {project["slug"]}: {target.relative_to(ROOT)}')
        return True
    except (OSError, URLError, ValueError) as error:
        print(f'FAIL {project["slug"]}: {error}', file=sys.stderr)
        return False


def main():
    projects = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))
    results = [fetch(project) for project in projects]
    if any(results):
        subprocess.run([sys.executable, str(ROOT / 'scripts/build.py')], check=True)
    if not all(results):
        print('取得できなかった写真があります。外部通信が可能なターミナルで再実行してください。', file=sys.stderr)
        return 1
    print('写真の保存とHTMLの更新が完了しました。元写真は編集せずに保管しています。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
