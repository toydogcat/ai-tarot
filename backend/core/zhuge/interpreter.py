from pydantic import BaseModel, Field
import google.genai as genai
import os
from core.config_manager import config_manager

class ZhugeReadingResult(BaseModel):
    reading: str = Field(description="諸葛神算解讀結果，以純文字回傳")

def interpret_zhuge(question: str, lot_data: dict, language: str = "繁體中文", selected_model: str = "gemini-3.1-flash-lite-preview", system_prompt: str = "") -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    
    conf = config_manager.get()
    
    # 取代預設的提示詞
    sys_prompt = conf.prompts.get("zhuge_system", "你是一位精通「諸葛神算」的占卜大師。")
    req_prompt = conf.prompts.get("zhuge_requirements", "請根據這支籤詩與傳統解說的意境，結合使用者的問題，給出有建設性的解讀。")
    
    # 組合 Prompt
    prompt = f"""
{sys_prompt}

使用者想問的問題：{question}

使用者抽到的籤詩：
第 {lot_data.get('id')} 籤：【{lot_data.get('poem')}】
傳統籤意解說：{lot_data.get('explanation', '無')}

{req_prompt}
請務必使用「{language}」語言來撰寫你的最終解讀回覆。
{system_prompt}
"""
    
    response = client.models.generate_content(
        model=selected_model,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ZhugeReadingResult,
            temperature=0.7
        )
    )
    
    try:
        import json
        result_dict = json.loads(response.text)
        return result_dict.get("reading", "")
    except:
         return response.text
