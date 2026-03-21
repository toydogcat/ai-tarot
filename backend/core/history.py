"""History 系統 — 紀錄每次占卜到 history/ 資料夾"""
import json
import uuid
from datetime import datetime
from pathlib import Path

from config import BASE_DIR
from core.tarot.models import SpreadResult
from core.logger import get_logger

HISTORY_DIR = BASE_DIR / "history"
HISTORY_DIR.mkdir(exist_ok=True)

logger = get_logger("history")


def _get_today_file() -> Path:
    """取得今天的 history JSON 檔案路徑"""
    today = datetime.now().strftime("%Y-%m-%d")
    return HISTORY_DIR / f"{today}.json"


def _load_today_records() -> list[dict]:
    """載入今天的紀錄"""
    filepath = _get_today_file()
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_records(records: list[dict], filepath: Path | None = None):
    """儲存紀錄"""
    if filepath is None:
        filepath = _get_today_file()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def save_reading(
    record_type: str,
    question: str,
    result: any,
    interpretation: str | None,
    ai_prompt: str | None = None,
    ai_interpretation_audio_path: str | None = None,
    search_success: bool = True,
) -> str:
    """
    儲存一次占卜/卜卦紀錄

    Args:
        record_type: 'tarot' 或是 'iching'
        question: 使用者問題
        result: 抽牌或卜卦結果 (SpreadResult 或 Dict)
        interpretation: AI 解讀（None 或 'error' 如果失敗）
        ai_prompt: 送給大語言模型的提示詞

    Returns:
        紀錄 ID
    """
    record_id = str(uuid.uuid4())[:8]
    now = datetime.now()

    # 組合紀錄結果資料
    result_data = {}
    if record_type == "tarot":
        cards_data = []
        for i, drawn_card in enumerate(result.drawn_cards):
            pos = result.spread.positions[i]
            cards_data.append({
                "position": pos.name,
                "position_desc": pos.description,
                "card_id": drawn_card.card.id,
                "card_name": drawn_card.card.name,
                "card_name_zh": drawn_card.card.name_zh,
                "is_reversed": drawn_card.is_reversed,
                "orientation": "逆位" if drawn_card.is_reversed else "正位",
                "keywords": drawn_card.current_meaning.keywords,
                "meaning": drawn_card.current_meaning.meaning,
            })
        result_data = {
            "spread": {
                "id": result.spread.id,
                "name": result.spread.name,
                "card_count": result.spread.card_count,
            },
            "cards": cards_data
        }
    elif record_type == "iching":
        result_data = {
            "tosses": result["tosses"],
            "original_hexagram": result["original_hexagram"]["name"] if result["original_hexagram"] else None,
            "changed_hexagram": result["changed_hexagram"]["name"] if result["changed_hexagram"] else None,
            "has_moving_lines": result["has_moving_lines"],
            "lines_info": [{"moving": l["moving"], "symbol": l["symbol"], "value": l["value"]} for l in result["lines_info"]]
        }
    elif record_type == "zhuge":
        result_data = {
            "id": result.get("id"),
            "poem": result.get("poem")
        }
    elif record_type == "daliuren":
        result_data = {
            "jieqi": result.get("jieqi"),
            "date": result.get("date"),
            "pattern": result.get("pattern"),
            "san_chuan": result.get("san_chuan"),
            "si_ke": result.get("si_ke")
        }

    # 判斷 AI 狀態
    ai_status = {
        "interpretation": "success",
        "audio": "error",
        "search": "success" if search_success else "error"
    }
    
    if interpretation is None or interpretation == "error" or interpretation.startswith("⚠️") or interpretation.startswith("❌"):
        ai_status["interpretation"] = "error"
        interpretation = "error"
    elif ai_interpretation_audio_path:
        ai_status["audio"] = "success"

    record = {
        "id": record_id,
        "type": record_type,
        "timestamp": now.isoformat(),
        "time_display": now.strftime("%H:%M:%S"),
        "question": question,
        "result": result_data,
        "ai_prompt": ai_prompt or "",
        "ai_interpretation": interpretation,
        "ai_status": ai_status,
        "ai_interpretation_audio_path": ai_interpretation_audio_path,
    }

    # 歷史向下相容：如果是 tarot，加上舊有第一層的欄位
    if record_type == "tarot":
        record["spread"] = result_data["spread"]
        record["cards"] = result_data["cards"]

    records = _load_today_records()
    records.append(record)
    _save_records(records)

    logger.info(
        f"占卜紀錄已儲存 [ID={record_id}] [{record_type}] "
        f"問題='{question[:30]}...' "
        f"AI={ai_status}"
    )

    return record_id


def get_history_dates() -> list[str]:
    """取得所有有紀錄的日期（降序）"""
    files = sorted(HISTORY_DIR.glob("*.json"), reverse=True)
    return [f.stem for f in files]


def load_history(date: str) -> list[dict]:
    """載入特定日期的紀錄"""
    filepath = HISTORY_DIR / f"{date}.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_error_records(date: str | None = None) -> list[dict]:
    """
    取得指定日期（或全部）中 AI 狀態為 error 的紀錄

    Args:
        date: 指定日期，None 則搜尋全部
    """
    errors = []
    if date:
        dates = [date]
    else:
        dates = get_history_dates()

    for d in dates:
        records = load_history(d)
        for r in records:
            ai_status = r.get("ai_status", {})
            if isinstance(ai_status, str):
                if ai_status == "error":
                    r["_date"] = d
                    errors.append(r)
            elif ai_status.get("interpretation") == "error":
                r["_date"] = d
                errors.append(r)
    return errors


def update_record_interpretation(date: str, record_id: str, interpretation: str, audio_path: str | None = None) -> bool:
    """
    更新特定紀錄的 AI 解讀（用於修復 error）

    Args:
        date: 紀錄日期
        record_id: 紀錄 ID
        interpretation: 新的 AI 解讀

    Returns:
        是否成功更新
    """
    filepath = HISTORY_DIR / f"{date}.json"
    if not filepath.exists():
        return False

    records = load_history(date)
    for record in records:
        if record["id"] == record_id:
            # 確保 ai_status 是字典
            if isinstance(record.get("ai_status"), str) or "ai_status" not in record:
                record["ai_status"] = {"interpretation": "error", "audio": "error", "search": "skipped"}
                
            if interpretation:
                record["ai_interpretation"] = interpretation
                record["ai_status"]["interpretation"] = "success"
            
            if audio_path:
                record["ai_interpretation_audio_path"] = audio_path
                record["ai_status"]["audio"] = "success"
                
            record["recovered_at"] = datetime.now().isoformat()
            
            _save_records(records, filepath)
            logger.info(f"紀錄 {record_id} AI 解讀已修復")
            return True

    return False

def search_history_records(query: str, limit: int = 10) -> list[dict]:
    """使用 thefuzz 進行歷史紀錄語意搜尋"""
    if not query.strip():
        return []

    try:
        from thefuzz import process
    except ImportError:
        logger.error("thefuzz 套件未安裝，無法進行搜尋")
        return []

    dates = get_history_dates()
    all_records = []
    
    for d in dates:
        records = load_history(d)
        for r in records:
            ai_status = r.get("ai_status", {})
            is_valid = False
            if isinstance(ai_status, str):
                is_valid = ai_status in ("success", "recovered")
            else:
                is_valid = ai_status.get("interpretation") == "success"
                
            if is_valid and r.get("ai_interpretation"):
                r["_date"] = d
                all_records.append(r)

    if not all_records:
        return []

    choices = {i: r["ai_interpretation"] for i, r in enumerate(all_records)}
    
    results = process.extract(query, choices, limit=limit)
    
    matched_records = []
    for match_str, score, key in results:
        if score > 30: # fuzzy 門檻
            record = all_records[key].copy()
            record["_search_score"] = score
            matched_records.append(record)
            
    return matched_records

