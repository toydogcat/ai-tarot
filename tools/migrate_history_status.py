import sys
import json
from pathlib import Path

# 加入專案根目錄到 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.history import get_history_dates, load_history, _save_records, HISTORY_DIR

def migrate_status(record: dict) -> bool:
    ai_status = record.get("ai_status", "error")
    
    # 如果已經是 dict 代表可能已經 migrate 過，檢查有沒有 search 鍵
    if isinstance(ai_status, dict):
        if "search" not in ai_status:
            ai_status["search"] = "skipped"
            return True
        return False

    new_status = {"interpretation": "error", "audio": "error", "search": "skipped"}
    
    # 以往的成功字串
    if ai_status in ("success", "recovered"):
        new_status["interpretation"] = "success"
        if record.get("ai_interpretation_audio_path"):
            new_status["audio"] = "success"
    
    # 二度檢查 interpretation 內容
    interpretation = record.get("ai_interpretation")
    if not interpretation or isinstance(interpretation, str) and (
        interpretation == "error" or interpretation.startswith("⚠️") or interpretation.startswith("❌")
    ):
        new_status["interpretation"] = "error"
        new_status["audio"] = "error"
        
    record["ai_status"] = new_status
    return True

def main():
    dates = get_history_dates()
    total_migrated = 0
    
    print(f"🔍 掃描到 {len(dates)} 天的歷史紀錄...")
    for d in dates:
        filepath = HISTORY_DIR / f"{d}.json"
        records = load_history(d)
        changed = False
        
        for r in records:
            if migrate_status(r):
                changed = True
                total_migrated += 1
                
        if changed:
            _save_records(records, filepath)
            print(f"✅ 已成功遷徙: {filepath.name}")

    print(f"🎉 遷徙完成！總共更新了 {total_migrated} 筆紀錄的 ai_status 格式。")

if __name__ == "__main__":
    main()
