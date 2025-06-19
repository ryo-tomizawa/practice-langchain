class AgentError(Exception):
    """エージェント関連の基本例外クラス"""
    pass

class ToolError(Exception):
    """ツール関連の基本例外クラス"""
    pass

class WeatherToolError(ToolError):
    """天気情報取得ツールの例外クラス"""
    pass

class FoodToolError(ToolError):
    """料理情報取得ツールの例外クラス"""
    pass

class AgentExecutionError(AgentError):
    """エージェント実行時の例外クラス"""
    pass

class AgentInitializationError(AgentError):
    """エージェント初期化時の例外クラス"""
    pass 