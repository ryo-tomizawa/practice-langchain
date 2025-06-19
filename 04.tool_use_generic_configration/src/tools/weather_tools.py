from langchain_core.tools import tool
import requests
import os
from src.utils.logger import CustomLogger
from src.utils.exceptions import WeatherToolError

logger = CustomLogger(__name__)

def convert_to_english_city_name(city: str) -> str:
    """日本語の都市名を英語に変換"""
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.environ["OPEN_AI_KEY"],
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
    try:
        logger.info(f"Getting weather for city: {city}")
        
        # 日本語の都市名を英語に変換
        english_city = convert_to_english_city_name(city)
        logger.debug(f"Converted city name: {english_city}")
        
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": english_city,
            "appid": os.environ["OPENWEATHER_KEY"],
            "units": "metric",  # 摂氏温度を使用
            "lang": "ja"  # 日本語で天気情報を取得
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        weather_data = response.json()
        logger.debug(f"Weather data retrieved: {weather_data}")
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting weather data: {str(e)}")
        raise WeatherToolError(f"天気情報の取得に失敗しました: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise WeatherToolError(f"予期せぬエラーが発生しました: {str(e)}") 