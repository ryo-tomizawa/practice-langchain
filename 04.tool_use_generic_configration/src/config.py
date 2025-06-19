import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# APIキーの設定
OPENAI_API_KEY = os.environ.get("OPEN_AI_KEY")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_KEY")

# モデル設定
DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0

# ログ設定
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# アプリケーション設定
DEFAULT_CITY = "東京"
MAX_RETRIES = 3
TIMEOUT = 30  # 秒

# エラーメッセージ
ERROR_MESSAGES = {
    "api_key_missing": "APIキーが設定されていません。",
    "weather_api_error": "天気情報の取得に失敗しました。",
    "food_api_error": "料理情報の取得に失敗しました。",
    "invalid_city": "指定された都市が見つかりません。",
    "no_information": "情報が見つかりませんでした。"
} 