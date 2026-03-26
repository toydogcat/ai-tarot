import os
import time
from google import genai
from google.genai import errors
from core.logger import get_logger
from core.config_manager import config_manager

logger = get_logger("interpreter")

def get_gemini_client() -> genai.Client | None:
    """取得 Gemini 客戶端"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def build_interpretation_prompt(question: str, result: dict, search_context: str = "", language: str = "繁體中文") -> str:
    """
    根據使用者問題、本卦與變卦，建構 Gemini 提示詞
    """
    has_moving = result["has_moving_lines"]
    orig_hex = result["original_hexagram"]
    changed_hex = result["changed_hexagram"]
    
    prompt = f"使用者問題：{question}\n\n"
    if search_context:
        prompt += f"{search_context}\n\n"
        
    prompt += "卜卦結果：\n"
    prompt += f"本卦：{orig_hex['name']} ({orig_hex['description']})\n"
    
    moving_lines = []
    for i, line in enumerate(result["lines_info"]):
        if line["moving"]:
            moving_lines.append(f"第 {i+1} 爻: {orig_hex['lines'][i]}")
            
    if has_moving:
        prompt += f"動爻：\n" + "\n".join(moving_lines) + "\n"
        prompt += f"變卦：{changed_hex['name']} ({changed_hex['description']})\n"
    else:
        prompt += "無動爻。\n"
        
    conf = config_manager.get()
    final_prompt = f"{conf.prompts.iching_system}\n\n"
    final_prompt += prompt
    final_prompt += f"\n## 解讀要求\n{conf.prompts.iching_requirements}\n\n"
    final_prompt += f"## 回覆語言\n請務必使用【{language}】身分與語言進行解讀與回覆。\n"
    return final_prompt

def get_ai_interpretation(question: str, result: dict, search_context: str = "", language: str = "繁體中文") -> str:
    """
    呼叫 Gemini API 取得 AI 解卦
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ 請先在 .env 中設定 GEMINI_API_KEY 才能使用 AI 解卦功能。"

    conf = config_manager.get()
    MODEL_ID = conf.ai_models.divination_model
    prompt = build_interpretation_prompt(question, result, search_context, language)

    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((errors.ServerError, errors.ClientError)),
        reraise=True
    )
    def _generate_with_retry():
        logger.info(f"Calling {MODEL_ID} for Iching interpretation...")
        return client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
        )

    try:
        response = _generate_with_retry()
        return response.text
    except errors.ClientError as e:
        if e.code == 429:
            return "❌ 目前 API 使用量已至上限，請稍後再試。"
        return "⚠️ AI 解卦暫時不可用，請稍後再試。 (ClientError)"
    except Exception as e:
        logger.error(f"Iching API Error: {e}")
        return "⚠️ 目前 AI 導師正忙於處理大量請求，請稍候片刻再試。 (Error: 503/Timeout)"
