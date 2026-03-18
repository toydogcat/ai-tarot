"""History 系統 — 紀錄每次占卜到 history/ 資料夾"""
import json
import uuid
from datetime import datetime
from pathlib import Path

from config import BASE_DIR
from core.models import SpreadResult
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
    question: str,
    result: SpreadResult,
    interpretation: str | None,
    ai_prompt: str | None = None,
    ai_interpretation_audio_path: str | None = None,
) -> str:
    """
    儲存一次占卜紀錄

    Args:
        question: 使用者問題
        result: 抽牌結果
        interpretation: AI 解牌（None 或 'error' 如果失敗）
        ai_prompt: 送給 Gemini 的提示詞

    Returns:
        紀錄 ID
    """
    record_id = str(uuid.uuid4())[:8]
    now = datetime.now()

    # 組合牌面資料
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

    # 判斷 AI 狀態
    ai_status = "success"
    if interpretation is None:
        ai_status = "error"
        interpretation = "error"
    elif interpretation.startswith("⚠️"):
        ai_status = "error"
        interpretation = "error"

    record = {
        "id": record_id,
        "timestamp": now.isoformat(),
        "time_display": now.strftime("%H:%M:%S"),
        "question": question,
        "spread": {
            "id": result.spread.id,
            "name": result.spread.name,
            "card_count": result.spread.card_count,
        },
        "cards": cards_data,
        "ai_prompt": ai_prompt or "",
        "ai_interpretation": interpretation,
        "ai_status": ai_status,
        "ai_interpretation_audio_path": ai_interpretation_audio_path,
    }

    records = _load_today_records()
    records.append(record)
    _save_records(records)

    logger.info(
        f"占卜紀錄已儲存 [ID={record_id}] "
        f"問題='{question[:30]}...' "
        f"牌陣={result.spread.name} "
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
            if r.get("ai_status") == "error":
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
            record["ai_interpretation"] = interpretation
            record["ai_status"] = "recovered"
            record["recovered_at"] = datetime.now().isoformat()
            if audio_path:
                record["ai_interpretation_audio_path"] = audio_path
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
            if r.get("ai_status") in ("success", "recovered") and r.get("ai_interpretation"):
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

