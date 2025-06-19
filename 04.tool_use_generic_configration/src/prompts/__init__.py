"""
Prompts package for weather and food information retrieval system.
"""

from .weather_prompts import WEATHER_SYSTEM_PROMPT, WEATHER_FORMAT_PROMPT
from .food_prompts import FOOD_SYSTEM_PROMPT, FOOD_FORMAT_PROMPT
from .coordinator_prompts import COORDINATOR_SYSTEM_PROMPT, COORDINATOR_FORMAT_PROMPT

__all__ = [
    'WEATHER_SYSTEM_PROMPT',
    'WEATHER_FORMAT_PROMPT',
    'FOOD_SYSTEM_PROMPT',
    'FOOD_FORMAT_PROMPT',
    'COORDINATOR_SYSTEM_PROMPT',
    'COORDINATOR_FORMAT_PROMPT'
] 