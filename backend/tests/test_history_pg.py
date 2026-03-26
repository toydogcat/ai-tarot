import pytest
from core.history import (
    save_reading,
    load_history,
    get_history_dates,
    delete_record,
    search_history_records,
    get_error_records,
    update_record_interpretation
)
from datetime import datetime

# 這是一個整合測試，需要實際連到已經架設好的 PostgreSQL 進行。

@pytest.fixture
def mock_record():
    return {
        "record_type": "tarot",
        "question": "測試用問題 PG Integration Test",
        "result": {"dummy": "data"},
        "interpretation": "測試解讀成功",
        "ai_prompt": "prompt test",
        "ai_interpretation_audio_path": None,
        "search_success": True,
        "mentor_id": "test_mentor_pg",
        "client_id": "test_client_pg"
    }

def test_save_and_load_reading(mock_record):
    # 儲存
    record_id = save_reading(**mock_record)
    assert record_id is not None
    assert len(record_id) > 0

    # 確認今天日期
    today = datetime.now().strftime("%Y-%m-%d")

    # 載入
    records = load_history(today, mentor_id="test_mentor_pg")
    # 找尋剛剛建立的 record
    found = next((r for r in records if r["id"] == record_id), None)
    
    assert found is not None
    assert found["question"] == mock_record["question"]
    assert found["ai_interpretation"] == mock_record["interpretation"]
    assert found["client_id"] == "test_client_pg"

    # 清除
    success = delete_record(today, record_id)
    assert success is True

def test_single_user_trial_mode():
    """測試單人模式下強制的 error 設定 (透過傳遞 is_multiuser=False)"""

    record_id = save_reading(
        record_type="iching",
        question="測試單人模式 Trial Error",
        result={"dummy": "data"},
        interpretation="這段應該被蓋過變成 error",
        mentor_id="test_trial",
        client_id="test_trial",
        is_multiuser=False
    )

    today = datetime.now().strftime("%Y-%m-%d")
    records = load_history(today, mentor_id="test_trial")
    found = next((r for r in records if r["id"] == record_id), None)
    
    assert found is not None
    assert found["ai_interpretation"] == "error"
    assert found["ai_status"]["interpretation"] == "error"
    assert found["ai_status"]["search"] == "error"
    assert found["ai_status"]["audio"] == "error"

    # 必須能被 get_error_records 抓到
    error_records = get_error_records(date_str=today, mentor_id="test_trial")
    error_found = next((r for r in error_records if r["id"] == record_id), None)
    assert error_found is not None

    # 清除
    delete_record(today, record_id)

def test_update_interpretation_and_search():
    # 儲存一個錯誤紀錄
    record_id = save_reading(
        record_type="zhuge",
        question="問題：明天天氣？",
        result={"dummy": "data"},
        interpretation="error",
        mentor_id="test_update",
        client_id="test_update"
    )
    today = datetime.now().strftime("%Y-%m-%d")

    # 更新解讀
    success = update_record_interpretation(today, record_id, "這是修復後的解讀 晴天！")
    assert success is True

    # 搜尋！
    results = search_history_records("晴天", mentor_id="test_update")
    assert len(results) > 0
    assert any(r["id"] == record_id for r in results)

    # 清理
    delete_record(today, record_id)
