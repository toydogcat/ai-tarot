import pytest
from unittest.mock import MagicMock, patch
from core.history import save_reading

def test_save_reading_signatures():
    """
    測試 save_reading 在各種占卜類型下的呼叫參數是否正確。
    這能確保在開發階段就發現 TypeError: got an unexpected keyword argument。
    """
    # 我們不實際寫入資料庫，Mock 掉 SQLAlchemy 的 insert/execute
    with patch("core.history.engine.begin") as mock_engine:
        # 1. 測試 塔羅 (Tarot) 的參數結構
        try:
            save_reading(
                record_type="tarot",
                question="測試問題", 
                result={"dummy": "data"}, 
                interpretation="解讀內容", 
                ai_prompt="prompt", 
                search_success=True,
                client_id="toby_guide" # 正確參數
            )
        except TypeError as e:
            pytest.fail(f"塔羅儲存參數錯誤: {e}")

        # 2. 測試 易經 (Iching)
        try:
            save_reading(
                record_type="iching",
                question="測試問題", 
                result={"dummy": "data"}, 
                interpretation="解讀內容", 
                ai_prompt="prompt", 
                search_success=True,
                client_id="toby_guide"
            )
        except TypeError as e:
            pytest.fail(f"易經儲存參數錯誤: {e}")

        # 3. 測試 諸葛神算 (Zhuge)
        try:
            save_reading(
                "zhuge", 
                "測試問題", 
                {"dummy": "data"}, 
                "解讀內容", 
                client_id="toby_guide"
            )
        except TypeError as e:
            pytest.fail(f"諸葛神算儲存參數錯誤: {e}")

        # 4. 測試 小六壬 (Xiaoliuren)
        try:
            save_reading(
                "xiaoliuren", 
                "測試問題", 
                {"dummy": "data"}, 
                "解讀內容", 
                client_id="toby_guide"
            )
        except TypeError as e:
            pytest.fail(f"小六壬儲存參數錯誤: {e}")

        # 5. 測試 大六壬 (Daliuren)
        try:
            save_reading(
                "daliuren", 
                "測試問題", 
                {"dummy": "data"}, 
                "解讀內容", 
                client_id="toby_guide"
            )
        except TypeError as e:
            pytest.fail(f"大六壬儲存參數錯誤: {e}")

def test_save_reading_failure_on_wrong_param():
    """
    驗證錯誤參數（例如 client_id）確實會觸發 TypeError。
    這樣可以確保我們的 Unit Test 具備偵測錯誤的能力。
    """
    with pytest.raises(TypeError) as excinfo:
        save_reading(
            record_type="tarot",
            question="測試問題", 
            result={}, 
            interpretation="解讀",
            client_id="wrong_param" # 這是故意打錯的
        )
    assert "unexpected keyword argument 'client_id'" in str(excinfo.value)
