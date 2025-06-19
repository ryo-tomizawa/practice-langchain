"""
高度な使用例を示すスクリプト
- エラーハンドリング
- カスタム設定
- 非同期処理
"""

import os
import sys
from pathlib import Path

# srcディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
src_path = str(project_root / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 必要なモジュールのインポート
from src.agents.coordinator_agent import CoordinatorAgent
from src.agents.weather_agent import WeatherAgent
from src.agents.food_agent import FoodAgent
from src.utils.logger import CustomLogger
from src.utils.exceptions import AgentError, ToolError
from dotenv import load_dotenv
import asyncio
import time

class AdvancedExample:
    def __init__(self):
        # 環境変数の読み込み
        load_dotenv()
        
        # ロガーの初期化
        self.logger = CustomLogger("advanced_example")
        self.logger.info("Initializing advanced example")
        
        # エージェントの初期化
        self.coordinator = CoordinatorAgent()
        self.weather_agent = WeatherAgent()
        self.food_agent = FoodAgent()

    async def process_query_async(self, query: str) -> str:
        """非同期でクエリを処理"""
        try:
            self.logger.info(f"Processing query asynchronously: {query}")
            # 実際の処理は同期的ですが、非同期処理の例として実装
            await asyncio.sleep(0.1)  # 非同期処理のシミュレーション
            return self.coordinator.process_query(query)
        except Exception as e:
            self.logger.error("Error in async processing", exc_info=e)
            raise

    def handle_errors(self, query: str) -> str:
        """エラーハンドリングの例"""
        try:
            self.logger.info(f"Processing query with error handling: {query}")
            return self.coordinator.process_query(query)
        except AgentError as e:
            self.logger.error("Agent error", exc_info=e)
            return f"エージェントエラー: {str(e)}"
        except ToolError as e:
            self.logger.error("Tool error", exc_info=e)
            return f"ツールエラー: {str(e)}"
        except Exception as e:
            self.logger.error("Unexpected error", exc_info=e)
            return f"予期せぬエラー: {str(e)}"

    def measure_performance(self, query: str) -> tuple:
        """パフォーマンス計測の例"""
        start_time = time.time()
        try:
            response = self.coordinator.process_query(query)
            end_time = time.time()
            return response, end_time - start_time
        except Exception as e:
            self.logger.error("Error in performance measurement", exc_info=e)
            return f"エラー: {str(e)}", time.time() - start_time

async def main():
    example = AdvancedExample()
    
    # 高度な使用例
    examples = [
        # 基本的なクエリ
        "東京の天気は？",
        # 複合クエリ
        "大阪の天気と名物料理を教えて",
        # エラーを引き起こす可能性のあるクエリ
        "存在しない都市の天気を教えて",
        # 複雑なクエリ
        "名古屋の天気と名物料理について、特に歴史的な背景も含めて教えて"
    ]
    
    print("\n=== 非同期処理の例 ===")
    for query in examples:
        try:
            response = await example.process_query_async(query)
            print(f"\n質問: {query}")
            print(f"回答: {response}")
        except Exception as e:
            print(f"エラー: {str(e)}")
    
    print("\n=== エラーハンドリングの例 ===")
    for query in examples:
        response = example.handle_errors(query)
        print(f"\n質問: {query}")
        print(f"回答: {response}")
    
    print("\n=== パフォーマンス計測の例 ===")
    for query in examples:
        response, execution_time = example.measure_performance(query)
        print(f"\n質問: {query}")
        print(f"回答: {response}")
        print(f"実行時間: {execution_time:.2f}秒")

if __name__ == "__main__":
    asyncio.run(main()) 