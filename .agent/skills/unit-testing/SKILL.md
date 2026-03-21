---
name: ai-tarot-unit-testing
description: 教導 AI 助理如何執行、擴充與維護本專案的 Pytest 單元測試，確保 WebSocket、API 與設定檔邏輯不會遭到破壞。
---

# AI Tarot & I-Ching 單元測試指南 (Unit Testing Guide)

本技能介紹如何執行並維護 `/backend/tests/` 目錄下的測試程式，確保核心系統穩定與向後相容。

## 1. 執行測試的方法

所有測試皆位於 `backend/tests/` 資料夾，並使用 `pytest` 作為測試框架。
請在終端機進入 `backend` 目錄並啟動對應的 Python 環境 (預設為 `toby`) 並執行以下指令：

```bash
cd backend
# pip install pytest pytest-asyncio httpx websockets

# 執行所有測試
PYTHONPATH=. pytest -v tests/

# 執行單一測試檔案
PYTHONPATH=. pytest -v tests/test_websocket_manager.py
```

## 2. 目前已完成的測試項目

為了保障即時推演架構的穩定，本專案已建構了以下四大核心模組 14 項以上的自動化測試：

### A. WebSocket 即時通管理員 (`test_websocket_manager.py`)
- **角色連線隔離**：測試導師 `toby` 與一般客戶 `client` 連線的獨佔機制。
- **防止重複登入**：驗證當 `toby` 或相同 `client` 已上線時，後續的連線會被系統自動拒絕或踢除。
- **廣播功能機制**：確保推播的 `broadcast` 能夠成功抵達所有允許的在線連線。

### B. 動態設定管理 (`test_config_manager.py`)
- **多設定檔載入**：測試系統能正確認知並載入 `default.yaml` 與 `customer1.yaml`，進行 `OmegaConf` 設定層級覆蓋。
- **單點存檔功能**：驗證當後台 (Streamlit) 修改各類占卜提示詞 (Prompts) 後，系統是否能無損地把更新寫回對應的客戶設定檔中，而不覆蓋到其他的欄位。

### C. 歷史紀錄 API (`test_history_api.py`)
- **客戶名稱篩選 (Client Filtering)**：測試 FastAPI 根據 Query Parameter `client_name` 取出歷史紀錄時，系統是否能成功過濾掉其他客戶的紀錄，僅回傳該名客戶專屬的占卜資料。
- **API 路由驗證**：確認 `/api/history` 路由是否如預期正常回傳無錯誤。

### D. AI 推演引擎與解析器 (`test_interpreters.py`)
- **Prompt 同步測試**：以 `Mock` 技術攔截 Gemini Client 的生成函式，驗證在諸葛神算與大六壬推演時，系統是否確實把 `zhuge_system` 或 `daliuren_requirements` 等客製化提示詞組裝到傳送給 LLM 的 payload 中。
- **同步與回傳格式驗證**：確保 `interpret_zhuge` 等核心函數正確處理回應，返回字串形式而非 Async 物件。

## 3. 開發規範 (如何新增測試)

如果未來 Agent 需要開發新功能或修復大 Core Bug，請遵守以下單元測試的擴充規範：

1. **Mock 外部資源機制**：
   當牽涉到呼叫 LLM (如 Gemini) 或網路搜尋 (如 Tavily) 時，切記不要發送真實 API 請求！
   請務必利用 `monkeypatch.setattr("google.genai.Client", mock_client)` 與自訂的 `MockModels` 進行攔截。讓測試不需耗費連線時間或真實的 Token。
2. **共用隔離夾具 (Fixtures)**：
   測試檔案讀寫（如 `core.history` 或 `core.config_manager`）時，請使用 `pytest.fixture` 中的 `tmp_path`，將檔案寫在 `/tmp/` 目錄中。
   請絕對避免在測試過程中去覆蓋或刪除正式系統的上線資料 (`history/*.json` 或 `config/*.yaml`)。
3. **異步測試**：
   如有測試到具有 `async def` 字眼的 FastAPI 路由函數或其他引擎推演函數，請加上 `@pytest.mark.asyncio` 修飾詞。

---
**Agent 提醒與防護方針：**
未來如果對核心系統進行了重大的修改（例如改變了 `models.py` 的 Pydantic Schemas，或是改變 WebSocket 的生命週期），請務必主動執行 `PYTHONPATH=. pytest -v tests/` 進行回歸測試。一旦有 Failures 出現，應優先修復向後相容性，再進行其他擴充。
