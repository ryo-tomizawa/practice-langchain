from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
# APIキーの設定
OPENAI_KEY = os.environ["OPEN_AI_KEY"]
OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]

@tool
def get_weather(city: str) -> dict:
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
        model="gpt-4",
        api_key=OPENAI_KEY,
        temperature=0
    )
    
    # ツールの設定
    tools = [get_weather]
    
    # ツールをモデルに紐づけ
    model_with_tools = llm.bind_tools(tools)
    
    # 最初のLLM呼び出し
    response = model_with_tools.invoke(
        [
            {"role": "system", "content": "あなたは天気情報を取得するアシスタントです。ユーザーの質問から都市名(英名)を抽出し、その都市の天気情報を取得してください。"},
            {"role": "user", "content": question}
        ]
    )
    
    # ツール呼び出しの処理
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        function_name = tool_call["name"]
        function_args = tool_call["args"]
        
        if function_name == "get_weather":
            weather_data = get_weather.invoke(function_args["city"])
            
            if "error" in weather_data:
                return f"申し訳ありません。天気情報の取得に失敗しました: {weather_data['error']}"
            
            # 天気情報を自然な文章に変換
            weather_info = {
                "city": function_args["city"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"]
            }
            
            # 天気情報を自然な文章に変換するためのLLM呼び出し
            format_response = model_with_tools.invoke(
                [
                    {"role": "system", "content": "あなたは天気情報を自然な日本語の文章に変換するアシスタントです。"},
                    {"role": "user", "content": question},
                    response,
                    {"role": "tool", "tool_call_id": tool_call["id"], "name": "get_weather", "content": json.dumps(weather_info, ensure_ascii=False)}
                ]
            )
            
            return format_response.content
    
    return "申し訳ありません。天気情報を取得できませんでした。"

# 使用例
if __name__ == "__main__":
    question = "東京の本日の天気はどうですか？"
    response = get_weather_info(question)
    print(response) 