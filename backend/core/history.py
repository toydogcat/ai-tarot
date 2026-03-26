"""History 系統 — 紀錄每次占卜到 PostgreSQL"""
import uuid
import json
from datetime import datetime
from typing import Optional

from sqlalchemy import select, insert, delete, update, desc, or_, func

from core.logger import get_logger
from core.db import engine, readings, init_db
from config import config_manager

logger = get_logger("history")

# 初始化資料庫表格 (如果不存在)
init_db()

def _dict_to_record(row) -> dict:
    """轉換 SQLAlchemy Row 為前端/依賴端相容的字典"""
    if not row:
        return {}
    r = dict(row._mapping)
    # 將 datetime 轉回 string
    r['timestamp'] = r['created_at'].isoformat() if r['created_at'] else None
    if r.get('recovered_at'):
        r['recovered_at'] = r['recovered_at'].isoformat()
    # 相容舊版，補充一些固定 key
    r['type'] = r['record_type']
    
    # tarot 的相容性
    if r['type'] == 'tarot' and isinstance(r.get('result'), dict):
        r['spread'] = r['result'].get('spread', {})
        r['cards'] = r['result'].get('cards', [])
        
    return r

def save_reading(
    record_type: str,
    question: str,
    result: any,
    interpretation: str | None,
    ai_prompt: str | None = None,
    ai_interpretation_audio_path: str | None = None,
    search_success: bool = True,
    mentor_id: str = "toby",
    client_id: str = "toby",
    is_multiuser: bool = True,
) -> str:
    """
    儲存一次占卜/卜卦紀錄到 PostgreSQL
    """
    record_id = str(uuid.uuid4())[:8]
    now = datetime.now()

    # 組合紀錄結果資料
    result_data = {}
    if record_type == "tarot" and not isinstance(result, dict):
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
    elif record_type == "iching" and "tosses" in (result if isinstance(result, dict) else {}):
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
            "poem": result.get("poem"),
            "interp1": result.get("interp1"),
            "interp2": result.get("interp2")
        }
    elif record_type == "daliuren":
        result_inner = result if isinstance(result, dict) else {}
        result_data = {
            "jieqi": result_inner.get("jieqi") or result_inner.get("節氣"),
            "date": result_inner.get("date") or result_inner.get("日期"),
            "pattern": result_inner.get("pattern") or result_inner.get("格局"),
            "san_chuan": result_inner.get("san_chuan") or result_inner.get("三傳"),
            "si_ke": result_inner.get("si_ke") or result_inner.get("四課")
        }
    else:
        result_data = result if isinstance(result, dict) else {}

    # === [核心實作] 單人模式 (Trial 版) AI 限縮邏輯 ===
    
    if not is_multiuser:
        # 單人試用版，強制關閉 AI 服務
        interpretation = "error"
        ai_interpretation_audio_path = None
        search_success = False
        ai_status = {
            "interpretation": "error",
            "audio": "error",
            "search": "error"
        }
    else:
        # 多人版正常判斷
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

    # 新增寫入 PostgreSQL
    stmt = insert(readings).values(
        id=record_id,
        record_type=record_type,
        created_at=now,
        time_display=now.strftime("%H:%M:%S"),
        mentor_id=mentor_id,
        client_id=client_id,
        question=question,
        result=result_data,
        ai_prompt=ai_prompt or "",
        ai_interpretation=interpretation,
        ai_status=ai_status,
        audio_path=ai_interpretation_audio_path,
        recovered_at=None
    )
    
    with engine.begin() as conn:
        conn.execute(stmt)

    logger.info(
        f"占卜紀錄已儲存至 DB [ID={record_id}] [{record_type}] "
        f"問題='{question[:30]}...' "
        f"Mentor={mentor_id} Client={client_id} AI={ai_status}"
    )

    return record_id

async def save_complete_reading(
    record_type: str,
    question: str,
    result: any,
    get_interpretation_func,
    build_prompt_func,
    search_func,
    generate_audio_func,
    mentor_id: str = "toby",
    client_id: str = "toby",
) -> tuple[str, str]:
    """
    一站式處理：外部搜尋 -> 提示詞建立 -> AI 解讀 -> 存入資料庫 -> 語音合成 -> 更新紀錄
    回傳: (record_id, interpretation)
    """
    # 1. 執行外部搜尋
    search_context, search_success = "", True
    if search_func:
        try:
            search_context, search_success = search_func(question)
        except Exception as e:
            logger.error(f"外部搜尋異常: {e}")
            search_success = False

    # 2. 建立 AI 提示詞 (用於紀錄，方便後續修復)
    ai_prompt = ""
    if build_prompt_func:
        try:
            ai_prompt = build_prompt_func(question, result, search_context)
        except Exception as e:
            logger.error(f"建立提示詞失敗: {e}")

    # 3. 取得 AI 解讀
    interpretation = "error"
    try:
        interpretation = get_interpretation_func(question, result, search_context)
    except Exception as e:
        logger.error(f"AI 解讀失敗: {e}")
        interpretation = f"⚠️ 解讀發生異常: {e}"

    # 4. 初始儲存紀錄
    record_id = save_reading(
        record_type=record_type,
        question=question,
        result=result,
        interpretation=interpretation,
        ai_prompt=ai_prompt,
        search_success=search_success,
        mentor_id=mentor_id,
        client_id=client_id
    )

    # 5. 產生語音 (如果解讀成功)
    if interpretation and not interpretation.startswith(("⚠️", "error", "❌")):
        try:
            audio_path = await generate_audio_func(interpretation, record_id)
            if audio_path:
                update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation, audio_path)
        except Exception as e:
            logger.error(f"語音合成或更新失敗: {e}")

    return record_id, interpretation

def get_history_dates(mentor_id: str | None = None) -> list[str]:
    """取得所有有紀錄的日期（降序） - 基於 created_at"""
    # 這裡我們用 date_trunc 取得不重複日期
    with engine.begin() as conn:
        query = select(func.date(readings.c.created_at).label("d")).distinct()
        if mentor_id:
            query = query.where(readings.c.mentor_id == mentor_id)
        query = query.order_by(desc("d"))
        
        results = conn.execute(query).fetchall()
        return [str(r[0]) for r in results if r[0]]

def load_history(date_str: str, mentor_id: str | None = None) -> list[dict]:
    """載入特定日期的紀錄"""
    with engine.begin() as conn:
        query = select(readings).where(func.date(readings.c.created_at) == date_str)
        if mentor_id:
            query = query.where(readings.c.mentor_id == mentor_id)
        query = query.order_by(desc(readings.c.created_at))
        
        rows = conn.execute(query).fetchall()
        # 兼容原本 json 的格式
        records = [_dict_to_record(row) for row in rows]
        for r in records:
            r["_date"] = date_str
        return records

def get_error_records(date_str: str | None = None, mentor_id: str | None = None) -> list[dict]:
    """取得 AI 狀態為 error 的紀錄"""
    with engine.begin() as conn:
        # MySQL/PostgreSQL json extraction: ai_status->>'interpretation' == 'error'
        query = select(readings).where(
            readings.c.ai_interpretation == "error"
        )
        if date_str:
            query = query.where(func.date(readings.c.created_at) == date_str)
        if mentor_id:
            query = query.where(readings.c.mentor_id == mentor_id)
            
        rows = conn.execute(query).fetchall()
        
        records = []
        for row in rows:
            r = _dict_to_record(row)
            if r['timestamp']:
                r['_date'] = r['timestamp'][:10]
            records.append(r)
        return records

def update_record_interpretation(date_str: str, record_id: str, interpretation: str, audio_path: str | None = None) -> bool:
    """更新特定紀錄的 AI 解讀（用於修復 error）"""
    with engine.begin() as conn:
        # First check if exists
        query = select(readings).where(readings.c.id == record_id)
        row = conn.execute(query).fetchone()
        if not row:
            return False
            
        ai_status = row.ai_status if row.ai_status else {}
        
        if interpretation:
            ai_status["interpretation"] = "success"
        if audio_path:
            ai_status["audio"] = "success"
            
        stmt = update(readings).where(readings.c.id == record_id).values(
            ai_interpretation=interpretation,
            ai_status=ai_status,
            audio_path=audio_path if audio_path else row.audio_path,
            recovered_at=datetime.now()
        )
        res = conn.execute(stmt)
        
        logger.info(f"紀錄 {record_id} AI 解讀已修復")
        return res.rowcount > 0

def search_history_records(query_str: str, mentor_id: str | None = None, limit: int = 10) -> list[dict]:
    """資料庫全文/模糊搜尋"""
    if not query_str.strip():
        return []

    with engine.begin() as conn:
        # 使用 PostgreSQL 原生 full-text search (FTS)
        # 用 coalesce 確保如果 question 或 ai_interpretation 有 NULL 不會讓整個字串變 NULL
        vector_col = func.to_tsvector(
            'simple', 
            func.coalesce(readings.c.question, '') + ' ' + func.coalesce(readings.c.ai_interpretation, '')
        )
        # 使用 plainto_tsquery 會自動將輸入字串轉為查詢格式 (自動插入 &)
        ts_query = func.plainto_tsquery('simple', query_str)
        
        query = select(readings).where(vector_col.op('@@')(ts_query))
        
        if mentor_id:
            query = query.where(readings.c.mentor_id == mentor_id)
            
        query = query.order_by(desc(readings.c.created_at)).limit(limit)
        
        rows = conn.execute(query).fetchall()
        records = []
        for row in rows:
            r = _dict_to_record(row)
            if r['created_at']:
                r['_date'] = r['created_at'].isoformat()[:10]
            r['_search_score'] = 100 # ILIKE 固定分數
            records.append(r)
            
        return records

def delete_record(date_str: str, record_id: str) -> bool:
    """刪除單筆紀錄"""
    with engine.begin() as conn:
        stmt = delete(readings).where(readings.c.id == record_id)
        res = conn.execute(stmt)
        if res.rowcount > 0:
            logger.info(f"已從資料庫刪除紀錄 {record_id}")
            return True
        return False

def delete_records_batch(records_to_delete: list[dict]) -> int:
    """大量刪除紀錄"""
    if not records_to_delete:
        return 0
        
    ids_to_delete = [r["id"] for r in records_to_delete if "id" in r]
    if not ids_to_delete:
        return 0
        
    with engine.begin() as conn:
        stmt = delete(readings).where(readings.c.id.in_(ids_to_delete))
        res = conn.execute(stmt)
        logger.info(f"已從資料庫批次刪除 {res.rowcount} 筆紀錄")
        return res.rowcount
