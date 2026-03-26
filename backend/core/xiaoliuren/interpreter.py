import os
import google.genai as genai
from google.genai import types, errors
from core.logger import get_logger
import time

logger = get_logger("xiaoliuren_interpreter")

def interpret_xiaoliuren(question: str, result_data: dict, language: str = "繁體中文", selected_model: str = "gemini-3.1-flash-lite-preview", system_prompt: str = "") -> str:
    """呼叫 Gemini 進行小六壬解讀"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    
    # Extract data
    num1, num2, num3 = result_data.get("numbers", [0, 0, 0])
    s1, s2, s3 = result_data.get("small_six_states", ["", "", ""])
    final_state = result_data.get("final_state", "")
    details = result_data.get("details", {})
    
    prompt = f"""
你是一位深諳中華傳統民俗占卜「小六壬」的智者。請根據以下起卦結果，為求問者進行解惑。

## 求問者的問題
{question}

## 起卦數字與結果
- 隨機數：{num1}, {num2}, {num3}
- 三階段狀態：初傳【{s1}】 -> 中傳【{s2}】 -> 終傳【{s3}】
- 最終定局：【{final_state}】

## 卦象傳統解曰
- 總結：{details.get("description", "")}
- 關鍵字：{details.get("keywords", "")}
- 籤詩：{details.get("poem", "")}
- 斷曰：{details.get("resolution", "")}

## 解讀要求
1. 請以溫暖、專業、具有同理心的語氣進行解說。
2. 結合初傳到終傳的變化軌跡（{s1}變{s2}變{s3}）來解釋事情的發展過程。
3. 重點解讀最終定局【{final_state}】，並與求問者的問題相連結。
4. 給出針對性的行動建議或心理建設。
5. 使用 {language} 回覆，請直接輸出解讀內容，不要使用 markdown 語法如 #, *, **，段落間用空行分隔。
"""

    if system_prompt:
        prompt = f"系統設定：\n{system_prompt}\n\n" + prompt

    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((errors.ServerError, errors.ClientError)),
        reraise=True
    )
    def _generate_with_retry():
        logger.info(f"Calling {selected_model} for Xiao Liu Ren interpretation...")
        return client.models.generate_content(
            model=selected_model,
            contents=prompt,
        )

    try:
        response = _generate_with_retry()
        return response.text
    except errors.ClientError as e:
        if e.code == 429:
            return "❌ 目前 API 使用量已至上限，請稍後再試。"
        return "⚠️ AI 解讀暫時不可用，請稍後再試。 (ClientError)"
    except Exception as e:
        logger.error(f"XiaoLiuRen API Error: {e}")
        return "⚠️ 目前 AI 導師正忙於處理大量請求，請稍候片刻再試。 (Error: 503/Timeout)"
