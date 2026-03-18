import os
from google import genai
from core.models import SpreadResult
from core.logger import get_logger

logger = get_logger("interpreter")


def get_gemini_client() -> genai.Client | None:
    """取得 Gemini 客戶端"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def build_interpretation_prompt(question: str, result: SpreadResult) -> str:
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

    prompt = f"""你是一位經驗豐富、溫暖而睿智的塔羅牌解讀師。
請根據以下塔羅牌占卜結果，為求問者提供深入且具有洞察力的解讀。

## 求問者的問題
{question}

## 使用的牌陣
{spread.name}（共 {spread.card_count} 張牌）
說明：{spread.description}

## 抽牌結果
{cards_text}

## 解讀要求
1. 先簡要概述整體牌面的能量與氛圍
2. 逐一解讀每個位置的牌面含義，並連結到求問者的問題
3. 特別注意牌與牌之間的關聯性和故事線
4. 如果有逆位的牌，請特別說明它的提醒意義
5. 最後給出整體建議與行動指引
6. 語氣溫暖、專業、有同理心，使用繁體中文
7. 不要使用任何 markdown 格式符號（如 #, *, ** 等），用純文字呈現
8. 段落之間用空行分隔，讓閱讀更舒適
"""
    return prompt


def get_ai_interpretation(question: str, result: SpreadResult) -> str:
    """
    呼叫 Gemini API 取得 AI 解牌

    Args:
        question: 使用者問題
        result: 抽牌結果

    Returns:
        AI 解牌文字，若失敗則回傳 "error"
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ 請先在 .env 中設定 GEMINI_API_KEY 才能使用 AI 解牌功能。"

    prompt = build_interpretation_prompt(question, result)

    try:
        logger.info("Calling Gemini API for interpretation...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return "error"
