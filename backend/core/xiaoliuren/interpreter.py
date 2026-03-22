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

    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling {selected_model} for Xiao Liu Ren interpretation (Attempt {attempt + 1})...")
            response = client.models.generate_content(
                model=selected_model,
                contents=prompt,
            )
            return response.text
        except errors.ClientError as e:
            if e.code == 429:
                wait_time = (attempt + 1) * 5
                time.sleep(wait_time)
                continue
            logger.error(f"Xiao Liu Ren API expected error: {e}")
            return "error"
        except Exception as e:
            logger.error(f"Unexpected error in XiaoLiuRen interpretation: {e}")
            return "error"
    return "error"
