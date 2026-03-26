import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def heal_zhuge():
    if not api_key:
        print("No GEMINI_API_KEY found")
        return

    client = genai.Client(api_key=api_key)
    file_path = 'data/zhuge/zhuge_data.json'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    missing_ids = [item['id'] for item in data if not item.get('poem')]
    print(f"Found {len(missing_ids)} lots with missing poems.")
    
    if not missing_ids:
        return

    # Process in small batches to avoid context limits or errors
    batch_size = 30
    for i in range(0, len(missing_ids), batch_size):
        batch = missing_ids[i:i+batch_size]
        print(f"Healing batch {i//batch_size + 1}: {batch[0]} to {batch[-1]}")
        
        prompt = f"""
你是一個精通諸葛神算（諸葛神數）的專家。
請提供以下籤號的「原始籤詩」文本。請務必精準，提供最標準的 384 籤版本。
籤號：{', '.join(map(str, batch))}

請回傳 JSON 對照表，格式如下：
{{
  "籤號": "原始籤詩內容",
  ...
}}
只回傳純 JSON，不要 Markdown。
"""
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].strip()
                
            updates = json.loads(text)
            
            # Apply updates
            count = 0
            for item in data:
                sid = str(item['id'])
                if sid in updates:
                    item['poem'] = updates[sid]
                    count += 1
                elif str(sid) in updates:
                    item['poem'] = updates[str(sid)]
                    count += 1
            
            print(f"Updated {count} poems.")
            
            # Save progress after each batch
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error in batch: {e}")
            if "429" in str(e):
                print("Quota exceeded. Waiting 40 seconds...")
                time.sleep(40)
                # We'll retry this specific batch next loop iteration by not incrementing index
                # But our current loop uses range(0, len, batch_size) which is hard to backtrack.
                # Actually, since it checks 'if not item.get("poem")', 
                # a simple rerun or continuing is fine.
        
        time.sleep(1)

if __name__ == "__main__":
    heal_zhuge()
