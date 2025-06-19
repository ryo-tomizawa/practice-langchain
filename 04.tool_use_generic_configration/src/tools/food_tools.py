from langchain_core.tools import tool
import wikipedia
from src.utils.logger import CustomLogger
from src.utils.exceptions import FoodToolError
from src.tools.weather_tools import convert_to_english_city_name

logger = CustomLogger(__name__)

@tool
def get_food_info(city: str) -> dict:
    """Wikipediaから指定した街発祥の料理情報を取得"""
    try:
        logger.info(f"Getting food info for city: {city}")
        
        # city名が日本語かどうか判定し、英語に変換
        import re
        if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', city):
            english_city = convert_to_english_city_name(city)
        else:
            english_city = city
        logger.debug(f"English city name: {english_city}")
        
        import wikipedia
        wikipedia.set_lang('en')
        
        # 検索クエリを構築（英語で検索）
        search_queries = [
            f"{english_city} cuisine",
            f"{english_city} food",
            f"{english_city} specialty",
            f"{english_city} local food"
        ]
        
        search_results = []
        for query in search_queries:
            results = wikipedia.search(query, results=3)
            search_results.extend(results)
        
        # 重複を除去
        search_results = list(set(search_results))
        logger.debug(f"Search results: {search_results}")
        
        if not search_results:
            logger.warning("No search results found")
            raise FoodToolError("料理情報が見つかりませんでした。")
        
        # 検索結果から最も関連性の高いページを選択
        food_pages = [result for result in search_results if any(keyword in result for keyword in ["料理", "名物", "郷土料理"])]
        logger.debug(f"Food-related pages: {food_pages}")
        
        if food_pages:
            selected_page = food_pages[0]
        else:
            selected_page = search_results[0]
        
        logger.info(f"Selected page: {selected_page}")
        
        # 選択したページの情報を取得
        page = wikipedia.page(selected_page)
        
        # 料理情報を抽出（最初の500文字）
        content = page.content[:500]
        
        # 料理に関連する部分を抽出
        food_related_sections = []
        current_section = ""
        
        for line in content.split('\n'):
            if any(keyword in line for keyword in ["料理", "名物", "郷土料理", "特産", "食"]):
                if current_section:
                    food_related_sections.append(current_section)
                current_section = line
            elif current_section:
                current_section += "\n" + line
        
        if current_section:
            food_related_sections.append(current_section)
        
        # 料理関連の情報が見つかった場合はそれを使用、なければ全体を使用
        final_content = "\n".join(food_related_sections) if food_related_sections else content
        
        result = {
            "title": page.title,
            "content": final_content,
            "url": page.url
        }
        
        logger.debug(f"Food info retrieved: {result}")
        return result
        
    except wikipedia.exceptions.DisambiguationError as e:
        logger.warning(f"Disambiguation error: {str(e)}")
        # 曖昧さ回避ページの場合は、料理に関連する可能性の高いオプションを選択
        food_options = [opt for opt in e.options if any(keyword in opt for keyword in ["料理", "名物", "郷土料理"])]
        selected_option = food_options[0] if food_options else e.options[0]
        
        try:
            page = wikipedia.page(selected_option)
            content = page.content[:500]
            return {
                "title": page.title,
                "content": content,
                "url": page.url
            }
        except Exception as sub_e:
            logger.error(f"Error processing disambiguation page: {str(sub_e)}")
            raise FoodToolError(f"ページの取得に失敗しました: {str(sub_e)}")
            
    except wikipedia.exceptions.PageError as e:
        logger.error(f"Page not found: {str(e)}")
        raise FoodToolError(f"ページが見つかりませんでした: {str(e)}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise FoodToolError(f"予期せぬエラーが発生しました: {str(e)}") 