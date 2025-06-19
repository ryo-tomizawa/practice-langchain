import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.coordinator_agent import CoordinatorAgent
from src.utils.logger import CustomLogger
from dotenv import load_dotenv

def main():
    # 環境変数の読み込み
    load_dotenv()
    
    # ロガーの初期化
    logger = CustomLogger("main")
    logger.info("Starting application")
    
    try:
        # 調整役エージェントの初期化
        coordinator = CoordinatorAgent()
        
        # 対話ループ
        print("天気情報と料理情報を取得するアシスタントです。")
        print("終了するには 'quit' または 'exit' と入力してください。")
        
        while True:
            user_input = input("\n質問を入力してください: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                logger.info("Application terminated by user")
                break
            
            if not user_input:
                continue
            
            # クエリの処理
            response = coordinator.process_query(user_input)
            print("\n回答:", response)
            
    except KeyboardInterrupt:
        logger.info("Application terminated by keyboard interrupt")
        print("\nアプリケーションを終了します。")
    except Exception as e:
        logger.error("Application error", exc_info=e)
        print(f"\nエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 