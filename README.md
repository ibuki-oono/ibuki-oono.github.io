# ibuki's blog

ビルド済みHTMLをそのまま公開できる、GitHub Pages用の静的サイトです。

```text
ホーム /
├── 自己紹介 /about/
├── 制作物 /works/
│   ├── キャチロボ2026 /works/catchrobo-2026/
│   ├── つくばチャレンジ2025 /works/tsukuba-2025/
│   ├── キャチロボ2025 /works/catchrobo-2025/
│   └── ゴルフロボット /works/golf-robot/
└── 仕事依頼 /contact/
```

## ローカルで見る

リポジトリのルートで `python3 -m http.server 8000` を実行し、http://localhost:8000/ を開きます。

## 更新する

- 制作物の短い紹介・詳細・出典・画像URL: `data/projects.json`
- 共通ナビゲーション・ページ構成・自己紹介: `scripts/build.py`
- スタイル: `css/style.css`
- スクロール表示・パララックス: `js/main.js`

文章や構成を変更したら、`python3 scripts/build.py` でHTMLを再生成してください。Python標準ライブラリだけで動きます。公開時のPython実行や依存パッケージは不要です。

## 画像と出典

ホームと制作物ページには、指定されたロボット技術研究会公式ブログの実機写真を使用します。個別ページに原記事へのリンクを掲載しています。

外部通信が可能なターミナルで、次のコマンドを実行すると4作品の元写真を `image/projects/` に保存します。既存の写真は上書きせず、保存後にHTMLを再生成します。

```sh
python3 scripts/fetch_images.py
```

ビルド時には保存済みの写真を優先し、未取得のものは元記事の画像URLを参照します。取得できない画像は原記事での閲覧を案内します。

4作品とも、ダウンロードした実機写真の背景を切り抜いた透過PNGを `image/projects/作品名-cutout.png` に保存しています。写真編集には image_gen を使用し、編集指示は `data/photo-edits.json` に記録しました。架空のロボットの画像は使用していません。

元のJPEGは上書きせずに保管し、各制作物の詳細ページに「元の写真を見る」リンクを掲載しています。`data/projects.json` の `display_image` が掲載用の写真を指定します。この項目を削除して再ビルドすると元写真に戻せます。元のサメの写真は自己紹介に使用しています。

連絡先はXのみです。アニメーションは端末の `prefers-reduced-motion` 設定に従います。JavaScriptを無効にしても、本文・ページ遷移・目次を利用できます。
