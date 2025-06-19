"""
天気情報を取得するエージェント
"""

from .base_agent import BaseAgent
from ..tools.weather_tools import get_weather
from ..prompts.weather_prompts import WEATHER_SYSTEM_PROMPT
from ..utils.logger import CustomLogger

class WeatherAgent(BaseAgent):
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        """
        天気エージェントの初期化
        
        Args:
            model_name: 使用するモデルの名前
            temperature: 生成時の温度パラメータ
        """
        self.logger = CustomLogger(self.__class__.__name__)
        
        # ツールの設定
        tools = [get_weather]
        
        # 親クラスの初期化
        super().__init__(
            tools=tools,
            system_prompt=WEATHER_SYSTEM_PROMPT,
            model_name=model_name,
            temperature=temperature,
            verbose=False
        )
        
        self.logger.info("WeatherAgent initialized")
    
    def get_weather_info(self, city: str) -> str:
        """
        指定された都市の天気情報を取得する
        
        Args:
            city: 天気情報を取得する都市名
            
        Returns:
            str: 天気情報
        """
        try:
            self.logger.info(f"Getting weather info for city: {city}")
            query = f"{city}の天気を教えてください"
            return self.process_query(query)
        except Exception as e:
            self.logger.error(f"Error getting weather info for {city}", exc_info=e)
            raise 