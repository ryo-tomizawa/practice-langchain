# プロジェクト概要

このプロジェクトでは、LangChainの基本的な利用方法について共有しています。<br>


## ディレクトリ構成
```
agent-design-pattern/
├── .env.sample
├── .gitignore
├── 00.basic_sample/
├── 01.multi_chain/
├── 02.multi_agent/
├── to be continued
└── ...
```

## 実行方法
### API KEYの準備

1. `.env.sample` ファイルを `.env` にリネームします。
2. `.env` ファイル内に以下のようにAPIキーを追記します。
```:.env
API_KEY=your_api_key_here
```

### .gitignoreファイルの作成

`.gitignore` ファイルを作成し、以下の内容を追加することで、`.env` ファイルがgitに含まれないようにします。

```:.gitignore
.env
```