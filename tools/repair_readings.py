"""修復 AI 解牌失敗的歷史紀錄"""
import argparse
import os
import sys
from pathlib import Path

# 確保可以 import 專案模組
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from google import genai
from core.history import get_error_records, load_history, update_record_interpretation, get_history_dates
from core.logger import get_logger

logger = get_logger("repair")


def build_repair_prompt(record: dict) -> str:
    """從 history 紀錄建構 Gemini 提示詞"""
    spread = record["spread"]
    cards = record["cards"]
    question = record["question"]

    cards_info = []
    for card in cards:
        cards_info.append(
            f"  位置【{card['position']}】（{card['position_desc']}）\n"
            f"  牌面：{card['card_name_zh']}（{card['card_name']}）— {card['orientation']}\n"
            f"  關鍵詞：{', '.join(card['keywords'])}\n"
            f"  牌意：{card['meaning']}"
        )

    cards_text = "\n\n".join(cards_info)

    return f"""你是一位經驗豐富、溫暖而睿智的塔羅牌解讀師。
請根據以下塔羅牌占卜結果，為求問者提供深入且具有洞察力的解讀。

## 求問者的問題
{question}

## 使用的牌陣
{spread['name']}（共 {spread['card_count']} 張牌）

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


def repair_single(date: str, record_id: str) -> bool:
    """修復單筆紀錄"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ 未設定 GEMINI_API_KEY，請檢查 .env 檔")
        return False

    records = load_history(date)
    target = None
    for r in records:
        if r["id"] == record_id:
            target = r
            break

    if not target:
        print(f"❌ 找不到紀錄 [日期={date}, ID={record_id}]")
        return False

    if target.get("ai_status") != "error":
        print(f"⏭ 紀錄 {record_id} 狀態為 '{target.get('ai_status')}'，非 error，跳過")
        return False

    print(f"🔄 正在修復紀錄 {record_id}...")
    print(f"   問題：{target['question'][:50]}...")
    print(f"   牌陣：{target['spread']['name']}")

    # 優先使用已儲存的 prompt，否則重新建構
    prompt = target.get("ai_prompt", "")
    if not prompt:
        print("   ⚠️ 紀錄中無 ai_prompt，重新建構...")
        prompt = build_repair_prompt(target)
    else:
        print("   ✅ 使用已儲存的 ai_prompt")
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        interpretation = response.text

        success = update_record_interpretation(date, record_id, interpretation)
        if success:
            print(f"✅ 紀錄 {record_id} 已成功修復！")
            logger.info(f"紀錄 {record_id} 已修復")
            return True
        else:
            print(f"❌ 寫入修復結果失敗")
            return False

    except Exception as e:
        print(f"❌ Gemini API 呼叫失敗：{e}")
        logger.error(f"修復紀錄 {record_id} 失敗: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="修復 AI 解牌失敗的歷史紀錄")
    parser.add_argument("--list", action="store_true", help="列出所有 error 紀錄")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--id", type=str, help="指定紀錄 ID")
    parser.add_argument("--all", action="store_true", help="修復所有 error 紀錄")

    args = parser.parse_args()

    if args.list:
        errors = get_error_records(args.date)
        if not errors:
            print("🎉 沒有任何 error 紀錄！")
            return

        print(f"找到 {len(errors)} 筆 error 紀錄：\n")
        for e in errors:
            date = e.get("_date", "unknown")
            print(f"  ❌ [{date}] ID={e['id']}  {e['question'][:50]}...")
            print(f"     牌陣：{e['spread']['name']}")
            cards_summary = ", ".join(
                f"{c['card_name_zh']}({c['orientation']})"
                for c in e["cards"]
            )
            print(f"     牌面：{cards_summary}")
            print()
        return

    if args.all:
        errors = get_error_records(args.date)
        if not errors:
            print("🎉 沒有任何 error 紀錄需要修復！")
            return

        print(f"🔧 準備修復 {len(errors)} 筆紀錄...\n")
        success_count = 0
        for e in errors:
            date = e.get("_date", "unknown")
            if repair_single(date, e["id"]):
                success_count += 1
            print()

        print(f"完成！成功修復 {success_count}/{len(errors)} 筆紀錄")
        return

    if args.date and args.id:
        repair_single(args.date, args.id)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
