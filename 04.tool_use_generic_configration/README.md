# Weather and Food Information Retrieval System

このプロジェクトは、日本の都市の天気情報と料理情報を取得するためのシステムです。OpenAIのGPTモデルと各種APIを使用して、自然な日本語で情報を提供します。

## 機能

- 天気情報の取得
  - 現在の天気
  - 気温
  - 湿度
  - 風速
  - 天気の説明

- 料理情報の取得
  - 地域の名物料理
  - 料理の特徴
  - 歴史的背景
  - 関連情報

## 必要条件

- Python 3.8以上
- OpenAI APIキー
- OpenWeather APIキー

## インストール

1. リポジトリをクローン:
```bash
git clone <repository-url>
cd 04.tool_use_generic_configration
```

2. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
`.env`ファイルを作成し、以下の内容を設定:
```
OPEN_AI_KEY=your_openai_api_key
OPENWEATHER_KEY=your_openweather_api_key
```

## 使用方法

1. アプリケーションを起動:
```bash
python src/main.py
```

2. プロンプトに従って質問を入力:
- 天気情報: "東京の天気は？"
- 料理情報: "大阪の名物料理は？"
- 両方の情報: "名古屋の天気と名物料理を教えて"

3. 終了するには 'quit' または 'exit' と入力

## プロジェクト構造

```
04.tool_use_generic_configration/
├── src/
│   ├── agents/          # エージェントの実装
│   ├── prompts/         # プロンプトテンプレート
│   ├── tools/           # ツールの実装
│   ├── utils/           # ユーティリティ
│   ├── config.py        # 設定ファイル
│   └── main.py          # メインエントリーポイント
├── examples/            # 使用例
├── requirements.txt     # 依存パッケージ
└── README.md           # ドキュメント
```

## エラーハンドリング

システムは以下のような状況を適切に処理します：
- APIキーが未設定
- 都市名が無効
- 情報が見つからない
- APIリクエストの失敗

## ライセンス

MIT License 