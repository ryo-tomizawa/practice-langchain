from src.agents.base_agent import BaseAgent
from src.agents.weather_agent import WeatherAgent
from src.agents.food_agent import FoodAgent
from src.prompts.coordinator_prompts import COORDINATOR_SYSTEM_PROMPT
from src.utils.logger import CustomLogger
from src.tools.weather_tools import get_weather
from src.tools.food_tools import get_food_info
import re
import os
from langchain_openai import ChatOpenAI

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        tools = [get_weather, get_food_info]
        super().__init__(
            tools=tools,
            system_prompt=COORDINATOR_SYSTEM_PROMPT,
            model_name="gpt-4",
            temperature=0.7,
            verbose=False
        )
        self.logger = CustomLogger(self.__class__.__name__)
        self.weather_agent = WeatherAgent()
        self.food_agent = FoodAgent()
        self.logger.info("CoordinatorAgent initialized")

    def _extract_city(self, query: str) -> str:
        """クエリから都市名を抽出（OpenAI APIを利用）"""
        try:
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=os.environ["OPEN_AI_KEY"],
                temperature=0
            )
            prompt = f"""次の日本語の質問文から都市名だけを抽出してください。都市名が複数ある場合は最も関連性が高いものを1つだけ返してください。都市名以外は一切含めず、都市名が見つからない場合は「東京」とだけ返してください。

質問文: {query}
都市名:"""
            response = llm.invoke(prompt)
            city = response.content.strip()
            self.logger.debug(f"Extracted city (via API): {city}")
            return city
        except Exception as e:
            self.logger.error("Error extracting city via API", exc_info=e)
            return "東京"

    def process_query(self, query: str) -> str:
        try:
            self.logger.info(f"Processing query: {query}")
            
            # 都市名の抽出
            city = self._extract_city(query)
            self.logger.info(f"Extracted city: {city}")
            
            # 必要な情報の取得
            weather_info = ""
            food_info = ""
            
            # 天気情報が必要か判断
            if any(keyword in query for keyword in ["天気", "気温", "温度", "降水", "雨", "晴れ"]):
                self.logger.info("Weather information requested")
                weather_info = self.weather_agent.get_weather_info(city)
            
            # 料理情報が必要か判断
            if any(keyword in query for keyword in ["料理", "食べ物", "名物", "郷土料理", "食"]):
                self.logger.info("Food information requested")
                food_info = self.food_agent.get_food_info(city)
            
            # 情報の組み合わせ
            combined_info = []
            if weather_info:
                combined_info.append(f"天気情報:\n{weather_info}")
            if food_info:
                combined_info.append(f"料理情報:\n{food_info}")
            
            if not combined_info:
                self.logger.warning("No specific information requested")
                return "申し訳ありません。具体的な情報の種類を指定してください。"
            
            # 情報を自然な文章にまとめる
            final_response = "\n\n".join(combined_info)
            self.logger.info("Query processed successfully")
            
            return final_response
            
        except Exception as e:
            self.logger.error("Error processing query", exc_info=e)
            return f"申し訳ありません。エラーが発生しました: {str(e)}" 