"""
カスタムロガーの実装
"""

import logging
import os
from datetime import datetime
from typing import Optional

class CustomLogger:
    def __init__(self, name: str):
        """
        カスタムロガーの初期化
        
        Args:
            name: ロガーの名前
        """
        self.logger = logging.getLogger(name)
        
        # ロガーが既に設定されている場合は、新しいハンドラを追加しない
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            
            # ログディレクトリの作成
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # ファイルハンドラの設定
            log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # コンソールハンドラの設定
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # フォーマッタの設定
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # ハンドラの追加
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
            # 親ロガーへの伝播を防止
            self.logger.propagate = False
    
    def debug(self, message: str, **kwargs):
        """デバッグレベルのログを出力"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """情報レベルのログを出力"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告レベルのログを出力"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """エラーレベルのログを出力"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """致命的なエラーレベルのログを出力"""
        self.logger.critical(message, **kwargs)

    def error(self, message: str, exc_info: Optional[Exception] = None):
        if exc_info:
            self.logger.error(f"{message} - Error: {str(exc_info)}", exc_info=True)
        else:
            self.logger.error(message) 