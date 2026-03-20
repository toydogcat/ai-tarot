import os
import time
from google import genai
from google.genai import errors
from core.tarot.models import SpreadResult
from core.logger import get_logger
from core.config_manager import config_manager

logger = get_logger("interpreter")


def get_gemini_client() -> genai.Client | None:
    """取得 Gemini 客戶端"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def build_interpretation_prompt(question: str, result: SpreadResult, search_context: str = "", language: str = "繁體中文") -> str:
    """
    根據使用者問題、牌陣與抽牌結果，建構 Gemini 提示詞

    Args:
        question: 使用者的提問
        result: 抽牌結果
    """
    spread = result.spread
    drawn = result.drawn_cards

    # 組合牌面資訊
    cards_info = []
    for i, drawn_card in enumerate(drawn):
        pos = spread.positions[i]
        card = drawn_card.card
        orientation = "逆位" if drawn_card.is_reversed else "正位"
        meaning = drawn_card.current_meaning

        cards_info.append(
            f"  位置【{pos.name}】（{pos.description}）\n"
            f"  牌面：{card.name_zh}（{card.name}）— {orientation}\n"
            f"  關鍵詞：{', '.join(meaning.keywords)}\n"
            f"  牌意：{meaning.meaning}"
        )

    cards_text = "\n\n".join(cards_info)
    conf = config_manager.get()

    prompt = f"{conf.prompts.tarot_system}\n\n"
    prompt += f"## 求問者的問題\n{question}\n"
    if search_context:
        prompt += f"{search_context}\n\n"
    prompt += f"## 使用的牌陣\n{spread.name}（共 {spread.card_count} 張牌）\n說明：{spread.description}\n\n"
    prompt += f"## 抽牌結果\n{cards_text}\n\n"
    prompt += f"## 解讀要求\n{conf.prompts.tarot_requirements}\n\n"
    prompt += f"## 回覆語言\n請務必使用【{language}】身分與語言進行解讀與回覆。\n"

    return prompt


def get_ai_interpretation(question: str, result: SpreadResult, search_context: str = "", max_retries: int = 3, language: str = "繁體中文") -> str:
    """
    呼叫 Gemini API 取得 AI 解牌

    Args:
        question: 使用者問題
        result: 抽牌結果
        max_retries: 最大重試次數

    Returns:
        AI 解牌文字，若失敗則回傳 "error"
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ 請先在 .env 中設定 GEMINI_API_KEY 才能使用 AI 解牌功能。"

    conf = config_manager.get()
    MODEL_ID = conf.ai_models.divination_model
    
    prompt = build_interpretation_prompt(question, result, search_context, language)

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling {MODEL_ID} for interpretation (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
            )
            return response.text
            
        except errors.ClientError as e:
            # 偵測是否為配額已滿 (HTTP 429)
            if e.code == 429:
                wait_time = (attempt + 1) * 10
                logger.warning(f"⚠️ 配額已滿 (429 Error)。將在 {wait_time} 秒後重試...")
                
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("API quota exceeded after max retries.")
                    return "❌ 目前 API 使用量已達上限 (Quota Exceeded)，請稍後再試。"
            
            # 其他 Client 錯誤
            logger.error(f"Gemini Client Error: {e}")
            return "error"

        except Exception as e:
            # 系統性錯誤
            logger.error(f"Unexpected error: {e}")
            return "error"

    return "error"
