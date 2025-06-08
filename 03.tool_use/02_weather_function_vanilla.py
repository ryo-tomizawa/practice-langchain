from openai import OpenAI
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
# APIキーの設定
OPENAI_KEY = os.environ["OPEN_AI_KEY"]
OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]

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

client = OpenAI(api_key=OPENAI_KEY)
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "指定した街の天気・温度情報を取得",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "街の英名"
                },
            },
            "required": ["city"],
            "additionalProperties": False
        },
    },
    "strict": True
}]

question = "東京の本日の天気はどうですか？"
input_messages = [{"role": "user", "content": question}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    tools=tools,
)
print(f'response_info: {response}')

message = response.choices[0].message

print(f'message_info: {message}')

if message.tool_calls:
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if function_name == "get_weather":
        weather_data = get_weather(function_args["city"])
        
        if "error" in weather_data:
            f"申し訳ありません。天気情報の取得に失敗しました: {weather_data['error']}"
        
        else:
            # 天気情報を整形
            weather_info = {
                "city": function_args["city"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"]
            }

            # 天気情報を自然な文章に変換
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "あなたは天気情報を自然な日本語の文章に変換するアシスタントです。"},
                    {"role": "user", "content": question},
                    message,
                    {"role": "tool", "tool_call_id": tool_call.id, "name": "get_weather", "content": json.dumps(weather_info, ensure_ascii=False)},
                ]
            )
            
            print(second_response.choices[0].message.content)
else:
    "申し訳ありません。天気情報を取得できませんでした。"

