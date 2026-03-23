import google.genai as genai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("No GEMINI_API_KEY found")
    exit(1)

client = genai.Client(api_key=api_key)

os.makedirs('backend/data/zhuge', exist_ok=True)
all_lots = []

# 分批生成，每次要求 96 籤，共 4 批
batches = [
    (1, 96),
    (97, 192),
    (193, 288),
    (289, 384)
]

print("Starting to fetch real Zhuge Shensuan poems using Gemini...")

for start_idx, end_idx in batches:
    print(f"Fetching lots {start_idx} to {end_idx}...")
    prompt = f"""
你是一個精通中華傳統命理與經典文獻的學者。
請提供諸葛神算（諸葛神數）第 {start_idx} 籤到第 {end_idx} 籤的「原始籤詩」文本，以及對應的「傳統籤意解說」。
請務必精確，不要自己發明或竄改，提供網路上廣為流傳的諸葛神算標準版本與經典解釋。
回傳格式必須是 JSON array，包含 {end_idx - start_idx + 1} 個 item，每個 item 包含 "id" (字串形式的數字)、"poem" (完整的籤詩字串) 以及 "explanation" (該籤的傳統籤解/意解字串)。
範例：
[
    {{"id": "1", "poem": "天門一掛榜，預定奪標人，馬嘶芳草地，秋高聽鹿鳴。", "explanation": "大吉大利，功名有望。秋冬之際將有捷報，凡事順遂，貴人相助。"}},
    {{"id": "2", "poem": "...", "explanation": "..."}}
]
只回傳純 JSON，不要任何 Markdown 標記，不要使用 ```json 包裹。
"""
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.1
            )
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        all_lots.extend(data)
        print(f"Got {len(data)} lots.")
    except Exception as e:
        print(f"Error fetching batch {start_idx}-{end_idx}: {e}")
    time.sleep(2)

if len(all_lots) > 0:
    for item in all_lots:
        item["id"] = str(item["id"])
    with open('backend/data/zhuge/zhuge_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_lots, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {len(all_lots)} lots to backend/data/zhuge/zhuge_data.json")
else:
    print("Failed to fetch data.")
