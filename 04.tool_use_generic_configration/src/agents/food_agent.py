from src.agents.base_agent import BaseAgent
from src.tools.food_tools import get_food_info
from src.prompts.food_prompts import FOOD_SYSTEM_PROMPT
from src.utils.logger import CustomLogger

class FoodAgent(BaseAgent):
    def __init__(self):
        tools = [get_food_info]
        super().__init__(
            tools=tools,
            system_prompt=FOOD_SYSTEM_PROMPT,
            model_name="gpt-4",
            temperature=0.7,
            verbose=False
        )
        self.logger = CustomLogger(self.__class__.__name__)
        self.logger.info("FoodAgent initialized")

    def get_food_info(self, city: str) -> str:
        try:
            self.logger.info(f"Getting food info for city: {city}")
            query = f"{city}の料理情報を教えてください"
            result = self.process_query(query)
            self.logger.info("Food info retrieved successfully")
            return result
        except Exception as e:
            self.logger.error("Error getting food info", exc_info=e)
            return f"料理情報の取得に失敗しました: {str(e)}" 