import json
import os

def generate_zhuge():
    os.makedirs('data/zhuge', exist_ok=True)
    all_lots = []
    
    for i in range(1, 385):
        if i == 1:
            all_lots.append({
                "id": str(i),
                "poem": "天門一掛榜，預定奪標人，馬嘶芳草地，秋高聽鹿鳴。"
            })
        elif i == 384:
            all_lots.append({
                "id": str(i),
                "poem": "人非孔顏鮮能無過，過而能改仍復無過，開花不足憑，結果方為准，放開懷抱意欣欣。"
            })
        else:
            all_lots.append({
                "id": str(i),
                "poem": f"諸葛神算第{i}籤詩文（建置中，請更新真實文本）"
            })
            
    with open('data/zhuge/zhuge_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_lots, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(all_lots)} mock lots for Zhuge.")

if __name__ == "__main__":
    generate_zhuge()
