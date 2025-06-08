from openai import OpenAI
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
# APIキーの設定
OPENAI_KEY = os.environ["OPEN_AI_KEY"]
OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]

def get_actual_weather(city: str) -> dict:
    """OpenWeather APIを使用して実際の天気情報を取得"""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_KEY,
        "units": "metric",  # 摂氏温度を使用
        "lang": "ja"  # 日本語で天気情報を取得
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_weather_info(question: str) -> str:
    # OpenAIクライアントの初期化
    client = OpenAI(
        api_key=OPENAI_KEY
    )
    
    # 質問から都市名を抽出するためのプロンプト
    extract_city_prompt = f"""以下の質問から都市名を抽出してください。
    質問: {question}
    都市名のみを英語に変換のうえ回答してください。"""

    # 都市名の抽出
    city_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは質問から都市名を抽出するアシスタントです。"},
            {"role": "user", "content": extract_city_prompt}
        ],
        temperature=0
    )
    
    city = city_response.choices[0].message.content.strip()
    
    # 実際の天気情報を取得
    weather_data = get_actual_weather(city)
    
    if "error" in weather_data:
        return f"申し訳ありません。天気情報の取得に失敗しました: {weather_data['error']}"
    
    # 天気情報を自然な文章に変換するためのプロンプト
    weather_info = {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"]
    }
    
    format_prompt = f"""以下の天気情報を自然な日本語の文章に変換してください：
    {json.dumps(weather_info, ensure_ascii=False, indent=2)}
    """

    # 天気情報を自然な文章に変換
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは天気情報を自然な日本語の文章に変換するアシスタントです。"},
            {"role": "user", "content": format_prompt}
        ],
        temperature=0
    )
    
    return response.choices[0].message.content

# 使用例
if __name__ == "__main__":
    question = "ワシントンの今日の天気はどうですか？"
    response = get_weather_info(question)
    print(response) 