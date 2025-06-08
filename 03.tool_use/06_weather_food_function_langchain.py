from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
import requests
import json
import wikipedia
from dotenv import load_dotenv

load_dotenv()
# APIキーの設定
OPENAI_KEY = os.environ["OPEN_AI_KEY"]
OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]

def convert_to_english_city_name(city: str) -> str:
    """日本語の都市名を英語に変換"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=OPENAI_KEY,
        temperature=0
    )
    
    prompt = f"""以下の日本語の都市名を英語に変換してください。
都市名のみを回答してください。例：東京 → Tokyo

都市名: {city}"""
    
    response = llm.invoke(prompt)
    return response.content.strip()

@tool
def get_weather(city: str) -> dict:
    """OpenWeather APIを使用して実際の天気情報を取得"""
    # 日本語の都市名を英語に変換
    english_city = convert_to_english_city_name(city)
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": english_city,
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

@tool
def get_food_info(city: str) -> dict:
    """Wikipediaから指定した街発祥の料理情報を取得"""
    try:
        # 検索クエリを構築（より柔軟な検索）
        search_queries = [
            f"{city} 料理",
            f"{city} 名物",
            f"{city} 郷土料理",
            f"{city} 発祥 料理"
        ]
        
        search_results = []
        for query in search_queries:
            results = wikipedia.search(query, results=3)
            search_results.extend(results)
        
        # 重複を除去
        search_results = list(set(search_results))
        
        if not search_results:
            return {"error": "料理情報が見つかりませんでした。"}
        
        # 検索結果から最も関連性の高いページを選択
        # 1. まず「料理」「名物」「郷土料理」を含むページを探す
        food_pages = [result for result in search_results if any(keyword in result for keyword in ["料理", "名物", "郷土料理"])]
        
        if food_pages:
            selected_page = food_pages[0]
        else:
            # 2. 料理ページが見つからない場合は最初の結果を使用
            selected_page = search_results[0]
        
        # 選択したページの情報を取得
        page = wikipedia.page(selected_page)
        
        # 料理情報を抽出（最初の500文字）
        content = page.content[:500]
        
        # 料理に関連する部分を抽出
        food_related_sections = []
        current_section = ""
        
        for line in content.split('\n'):
            if any(keyword in line for keyword in ["料理", "名物", "郷土料理", "特産", "食"]):
                if current_section:
                    food_related_sections.append(current_section)
                current_section = line
            elif current_section:
                current_section += "\n" + line
        
        if current_section:
            food_related_sections.append(current_section)
        
        # 料理関連の情報が見つかった場合はそれを使用、なければ全体を使用
        final_content = "\n".join(food_related_sections) if food_related_sections else content
        
        return {
            "title": page.title,
            "content": final_content,
            "url": page.url
        }
    except wikipedia.exceptions.DisambiguationError as e:
        # 曖昧さ回避ページの場合は、料理に関連する可能性の高いオプションを選択
        food_options = [opt for opt in e.options if any(keyword in opt for keyword in ["料理", "名物", "郷土料理"])]
        selected_option = food_options[0] if food_options else e.options[0]
        
        try:
            page = wikipedia.page(selected_option)
            content = page.content[:1000]
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

def process_query(question: str) -> str:
    # LLMの初期化
    llm = ChatOpenAI(
        model="gpt-4",
        api_key=OPENAI_KEY,
        temperature=0
    )
    
    # ツールの設定
    tools = [get_weather, get_food_info]
    
    # ツールをモデルに紐づけ
    model_with_tools = llm.bind_tools(tools)
    
    # 最初のLLM呼び出し
    response = model_with_tools.invoke(
        [
            {"role": "system", "content": "あなたは天気情報と料理情報を取得するアシスタントです。ユーザーの質問から適切な情報を取得してください。天気情報を取得する場合は、日本語の都市名をそのまま渡してください。内部で英語に変換されます。"},
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
                "city": function_args["city"],  # 日本語の都市名を保持
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
            
        elif function_name == "get_food_info":
            food_info = get_food_info.invoke(function_args["city"])
            
            if "error" in food_info:
                return f"申し訳ありません。料理情報の取得に失敗しました: {food_info['error']}"
            
            # 料理情報を自然な文章に変換するためのLLM呼び出し
            format_response = model_with_tools.invoke(
                [
                    {"role": "system", "content": "あなたは料理情報を自然な日本語の文章に変換するアシスタントです。"},
                    {"role": "user", "content": question},
                    response,
                    {"role": "tool", "tool_call_id": tool_call["id"], "name": "get_food_info", "content": json.dumps(food_info, ensure_ascii=False)}
                ]
            )
            
            return format_response.content
    
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