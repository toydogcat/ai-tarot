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
from core.tts import generate_audio
from core.logger import get_logger

logger = get_logger("repair")


def build_repair_prompt(record: dict) -> str:
    """從 history 紀錄建構 Gemini 提示詞"""
    record_type = record.get("type", "tarot")
    
    if record_type == "iching":
        from core.iching.interpreter import build_interpretation_prompt as build_iching_prompt
        # For older I-Ching records without saved prompt, we rebuild it.
        # We might not have search_context in history, so we pass empty string.
        return build_iching_prompt(record["question"], record["result"], "")
    
    # Tarot fallback
    else:
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

    ai_status = target.get("ai_status", {})
    if isinstance(ai_status, str):
        ai_status = {"interpretation": ai_status, "audio": "error"}

    if ai_status.get("interpretation") != "error":
        print(f"⏭ 紀錄 {record_id} 狀態為 '{ai_status.get('interpretation')}'，非 error，跳過")
        return False

    print(f"🔄 正在修復紀錄 {record_id}...")
    print(f"   類型：{target.get('type', 'tarot')}")
    print(f"   問題：{target['question'][:50]}...")

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
            model="gemini-3.1-flash-lite-preview",
            contents=prompt,
        )
        interpretation = response.text

        print("   🎵 正在生成語音...")
        audio_path = generate_audio(interpretation, record_id)
        if audio_path:
            print("   ✅ 語音生成成功")

        success = update_record_interpretation(date, record_id, interpretation, audio_path)
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


def get_missing_audio_records(date: str | None = None) -> list[dict]:
    """取得已成功解讀但缺少語音路徑的紀錄"""
    missing = []
    if date:
        dates = [date]
    else:
        dates = get_history_dates()

    for d in dates:
        records = load_history(d)
        for r in records:
            ai_status = r.get("ai_status", {})
            if isinstance(ai_status, str):
                ai_status = {"interpretation": ai_status, "audio": "error"}
                
            if ai_status.get("interpretation") in ("success", "recovered") and not r.get("ai_interpretation_audio_path"):
                r["_date"] = d
                missing.append(r)
    return missing


def fix_audio_single(date: str, record_id: str) -> bool:
    """為單筆紀錄補件語音"""
    records = load_history(date)
    target = None
    for r in records:
        if r["id"] == record_id:
            target = r
            break

    if not target:
        return False

    interpretation = target.get("ai_interpretation")
    if not interpretation or interpretation == "error":
        return False

    print(f"🎵 正在為紀錄 {record_id} 生成語音...")
    audio_path = generate_audio(interpretation, record_id)
    if audio_path:
        # 這裡借用 update_record_interpretation 的邏輯，但只更新 audio_path
        return update_record_interpretation(date, record_id, interpretation, audio_path)
    return False


def main():
    parser = argparse.ArgumentParser(description="修復 AI 解牌失敗或缺少語音的歷史紀錄")
    parser.add_argument("--list", action="store_true", help="列出所有 error 紀錄")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--id", type=str, help="指定紀錄 ID")
    parser.add_argument("--all", action="store_true", help="修復所有 error 紀錄")
    parser.add_argument("--fix-audio", action="store_true", help="修復缺少語音的紀錄")

    args = parser.parse_args()

    if args.list:
        errors = get_error_records(args.date)
        missing_audio = get_missing_audio_records(args.date)
        
        if not errors and not missing_audio:
            print("🎉 沒有任何需要修復的紀錄！")
            return

        if errors:
            print(f"找到 {len(errors)} 筆 error 紀錄：\n")
            for e in errors:
                date = e.get("_date", "unknown")
                print(f"  ❌ [{date}] ID={e['id']}  {e['question'][:50]}...")
            print()

        if missing_audio:
            print(f"找到 {len(missing_audio)} 筆缺少語音的紀錄：\n")
            for m in missing_audio:
                date = m.get("_date", "unknown")
                print(f"  🎵 [{date}] ID={m['id']}  {m['question'][:50]}...")
            print()
        return

    if args.fix_audio:
        missing = get_missing_audio_records(args.date)
        if not missing:
            print("🎉 沒有任何紀錄需要補件語音！")
            return

        print(f"🔧 準備為 {len(missing)} 筆紀錄生成語音...\n")
        success_count = 0
        for m in missing:
            date = m.get("_date", "unknown")
            if fix_audio_single(date, m["id"]):
                success_count += 1
        
        print(f"完成！成功補件 {success_count}/{len(missing)} 筆語音紀錄")
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
