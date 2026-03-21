from pydantic import BaseModel, Field
import google.genai as genai
import os
import json
from core.config_manager import config_manager

class DaliurenReadingResult(BaseModel):
    reading: str = Field(description="大六壬解讀結果，以純文字回傳")

def interpret_daliuren(question: str, lesson_data: dict, language: str = "繁體中文", selected_model: str = "gemini-2.5-flash", system_prompt: str = "") -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    
    conf = config_manager.get()
    
    # 取代預設的提示詞
    sys_prompt = conf.prompts.get("daliuren_system", "你是一位精通「大六壬」的占卜與神算大師。")
    req_prompt = conf.prompts.get("daliuren_requirements", "請根據大六壬的基礎意涵，結合使用者的問題，給出有建設性的吉凶判斷與解讀。")
    
    # 組合 Prompt
    lesson_str = json.dumps(lesson_data, ensure_ascii=False, indent=2)
    prompt = f"""
{sys_prompt}

使用者想問的問題：{question}

這是隨機起出的大六壬課象結構（包含四課、三傳、格局等資訊）：
```json
{lesson_str}
```

{req_prompt}
請務必使用「{language}」語言來撰寫你的最終解讀回覆。
{system_prompt}
"""
    
    response = client.models.generate_content(
        model=selected_model,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DaliurenReadingResult,
            temperature=0.7
        )
    )
    
    try:
        result_dict = json.loads(response.text)
        return result_dict.get("reading", "")
    except:
         return response.text
