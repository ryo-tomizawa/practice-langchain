"""
基本的なエージェントの実装
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool
from typing import List, Optional
from src.utils.logger import CustomLogger
from src.utils.exceptions import AgentError
import os

class BaseAgent:
    def __init__(
        self,
        tools: List[BaseTool],
        system_prompt: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        verbose: bool = False
    ):
        """
        基本的なエージェントの初期化
        
        Args:
            tools: エージェントが使用するツールのリスト
            system_prompt: システムプロンプト
            model_name: 使用するモデルの名前
            temperature: 生成時の温度パラメータ
            verbose: 詳細なログ出力を行うかどうか
        """
        self.logger = CustomLogger(self.__class__.__name__)
        self.logger.info(f"BaseAgent initialized with model: {model_name}")
        
        # モデルの初期化
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=os.environ["OPEN_AI_KEY"]
        )
        
        # プロンプトの設定
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # エージェントの作成
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=tools,
            prompt=self.prompt
        )
        
        # エージェントエグゼキューターの作成
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            verbose=verbose,
            handle_parsing_errors=True
        )
        
        self.logger.info("Agent created successfully")
    
    def process_query(self, query: str, chat_history: Optional[List] = None) -> str:
        """
        クエリを処理する
        
        Args:
            query: 処理するクエリ
            chat_history: チャット履歴（オプション）
            
        Returns:
            str: 処理結果
        """
        try:
            # チャット履歴がNoneの場合は空のリストを使用
            if chat_history is None:
                chat_history = []
                
            # エージェントの実行
            response = self.agent_executor.invoke({
                "input": query,
                "chat_history": chat_history
            })
            
            return response["output"]
            
        except Exception as e:
            self.logger.error(f"Error processing query - Error: {str(e)}", exc_info=e)
            raise AgentError(f"Error processing query: {str(e)}") 