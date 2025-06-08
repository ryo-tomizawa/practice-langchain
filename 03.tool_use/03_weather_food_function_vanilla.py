from openai import OpenAI
import os
import requests
import json
from dotenv import load_dotenv
import wikipedia

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

def get_food_info(city: str) -> dict:
    """Wikipediaから指定した街発祥の料理情報を取得"""
    try:
        # 検索クエリを構築
        search_query = f"{city} 発祥 料理"
        search_results = wikipedia.search(search_query, results=5)
        
        if not search_results:
            return {"error": "料理情報が見つかりませんでした。"}
        
        # 検索結果から最も関連性の高いページを選択
        # 1. まず「料理」を含むページを探す
        food_pages = [result for result in search_results if "料理" in result]
        if food_pages:
            selected_page = food_pages[0]
        else:
            # 2. 料理ページが見つからない場合は最初の結果を使用
            selected_page = search_results[0]
        
        # 選択したページの情報を取得
        page = wikipedia.page(selected_page)
        
        # 料理情報を抽出（最初の500文字）
        content = page.content[:500]
        
        return {
            "title": page.title,
            "content": content,
            "url": page.url
        }
    except wikipedia.exceptions.DisambiguationError as e:
        # 曖昧さ回避ページの場合は、最初のオプションを使用
        try:
            page = wikipedia.page(e.options[0])
            content = page.content[:500]
            return {
                "title": page.title,
                "content": content,
                "url": page.url
            }
        except Exception as sub_e:
            return {"error": f"ページの取得に失敗しました: {str(sub_e)}"}
    except wikipedia.exceptions.PageError as e:
        return {"error": f"ページが見つかりませんでした: {str(e)}"}
    except Exception as e:
        return {"error": f"エラーが発生しました: {str(e)}"}

client = OpenAI(api_key=OPENAI_KEY)
tools = [
    {
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_food_info",
            "description": "指定した街発祥の世界的に人気の料理をWikipediaから取得",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "街の名前（日本語可）"
                    },
                },
                "required": ["city"],
                "additionalProperties": False
            },
        },
        "strict": True
    }
]

def process_query(question: str):
    """ユーザーの質問を処理して回答を生成"""
    input_messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=input_messages,
        tools=tools,
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        if function_name == "get_weather":
            weather_data = get_weather(function_args["city"])
            
            if "error" in weather_data:
                return f"申し訳ありません。天気情報の取得に失敗しました: {weather_data['error']}"
            
            weather_info = {
                "city": function_args["city"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"]
            }

            second_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは天気情報を自然な日本語の文章に変換するアシスタントです。"},
                    {"role": "user", "content": question},
                    message,
                    {"role": "tool", "tool_call_id": tool_call.id, "name": "get_weather", "content": json.dumps(weather_info, ensure_ascii=False)},
                ]
            )
            
            return second_response.choices[0].message.content

        elif function_name == "get_food_info":
            food_info = get_food_info(function_args["city"])
            
            if "error" in food_info:
                return f"申し訳ありません。料理情報の取得に失敗しました: {food_info['error']}"
            
            second_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは料理情報を自然な日本語の文章に変換するアシスタントです。"},
                    {"role": "user", "content": question},
                    message,
                    {"role": "tool", "tool_call_id": tool_call.id, "name": "get_food_info", "content": json.dumps(food_info, ensure_ascii=False)},
                ]
            )
            
            return second_response.choices[0].message.content
    else:
        return "申し訳ありません。情報を取得できませんでした。"

# 使用例
if __name__ == "__main__":
    # 天気情報の取得例
    weather_question = "東京の本日の天気はどうですか？"
    print("天気情報の取得:")
    print(process_query(weather_question))
    print("\n" + "="*50 + "\n")
    
    # 料理情報の取得例
    food_question = "東京発祥の有名な料理について教えてください。"
    print("料理情報の取得:")
    print(process_query(food_question)) 