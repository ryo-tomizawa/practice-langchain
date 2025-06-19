"""
基本的な使用例を示すスクリプト
"""


import os
import sys
from pathlib import Path
# srcディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agents.coordinator_agent import CoordinatorAgent
from src.utils.logger import CustomLogger
from dotenv import load_dotenv


def main():
    # 環境変数の読み込み
    load_dotenv()
    
    # ロガーの初期化
    logger = CustomLogger("basic_example")
    logger.info("Starting basic example")
    
    try:
        # 調整役エージェントの初期化
        coordinator = CoordinatorAgent()
        
        # 基本的な使用例
        examples = [
            "東京の天気は？",
            # "大阪の名物料理を教えて",
            # "名古屋の天気と名物料理を教えて"
        ]
        
        for query in examples:
            print(f"\n質問: {query}")
            response = coordinator.process_query(query)
            print(f"回答: {response}")
            
    except Exception as e:
        logger.error("Error in basic example", exc_info=e)
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 