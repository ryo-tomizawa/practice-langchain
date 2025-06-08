from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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
    # LLMの初期化
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=OPENAI_KEY,
        temperature=0
    )
    
    # 都市名抽出用のプロンプトテンプレート
    city_extract_prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは質問から都市名を抽出するアシスタントです。"),
        ("user", "以下の質問から都市名を抽出してください。\n質問: {question}\n都市名のみを英語に変換のうえ回答してください。")
    ])
    
    # 都市名抽出用のチェーン
    city_extract_chain = city_extract_prompt | llm | StrOutputParser()
    
    # 天気情報を自然な文章に変換するためのプロンプトテンプレート
    weather_format_prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは天気情報を自然な日本語の文章に変換するアシスタントです。"),
        ("user", "以下の天気情報を自然な日本語の文章に変換してください：\n{weather_info}")
    ])
    
    # 天気情報フォーマット用のチェーン
    weather_format_chain = weather_format_prompt | llm | StrOutputParser()
    
    # 都市名の抽出
    city = city_extract_chain.invoke({"question": question}).strip()
    
    # 実際の天気情報を取得
    weather_data = get_actual_weather(city)
    
    if "error" in weather_data:
        return f"申し訳ありません。天気情報の取得に失敗しました: {weather_data['error']}"
    
    # 天気情報を自然な文章に変換
    weather_info = {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"]
    }
    
    # 天気情報のフォーマット
    return weather_format_chain.invoke({
        "weather_info": json.dumps(weather_info, ensure_ascii=False, indent=2)
    })

# 使用例
if __name__ == "__main__":
    question = "ワシントンの今日の天気はどうですか？"
    response = get_weather_info(question)
    print(response) 