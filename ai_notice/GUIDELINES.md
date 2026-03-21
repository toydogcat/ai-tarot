# 🌟 AI 智慧占卜 (Tarot & I-Ching) 專案開發注意事項

## 環境設定
- **Python 環境**：使用 Conda `toby` 環境 (啟用方式：`conda activate toby`)
- **環境變數**：複製 `.env.example` 為 `.env` 並填入 `GEMINI_API_KEY`、`TAVILY_API_KEY` 與 `NGROK_AUTHTOKEN`。
- **依賴安裝**：`pip install -r requirements.txt`，確保包含 `tavily-python`, `SpeechRecognition`, `pydub`, `streamlit-mic-recorder`, `fastapi`, `uvicorn`, `hydra-core` 等套件。

## 專案結構規範
| 目錄 | 用途 |
|------|------|
| `api/` | FastAPI 後端路由與 Pydantic 結構定義。 |
| `config/` | Hydra 動態設定檔 (default.yaml, customer1/2.yaml)，管理模型與 BGM。 |
| `data/` | 靜態資料庫 (包含塔羅牌意與易經六十四卦 JSON)。 |
| `assets/images/` | 牌面與卦象圖片資源。 |
| `assets/music/` | 背景音樂檔案 (`background1.mp3`, `background2.mp3`)。 |
| `core/` | 核心邏輯 (包含：抽牌引擎、金錢卦計算、設定檔管理、AI 解析、搜尋、語音處理、歷史狀態)。 |
| `tools/` | 輔助工具 (修復腳本與結構轉換腳本)。 |
| `history/` | 使用者歷史紀錄 JSON 以及生成的音訊 mp3。 |
| `ui/` | Streamlit UI 元件與管理介面。 |
| `.agent/skills/` | 給 AI Agent 使用的專屬技能操作說明 (`SKILL.md`)。 |
| `frontend/` | (位於專案根目錄) Vite + Vanilla JS 打造的高質感響應式前端使用者介面。 |

## 核心配置與背景音樂 (BGM)
- **設定檔載入**：使用 `core/config_manager.py` (Singleton)，預設讀取 `customer1.yaml`，可於 Streamlit 左側「設定管理」選單動態修改模型、Prompt 與首頁背景音樂。
- **音樂播放**：Streamlit 將自動播放 `config/` 所選的背景音樂 (BGM 1 或 2)。

## 四大系統核心邏輯 (Quad-System Logic)
### 1. 塔羅占卜 (Tarot)
- 支援 6 種以上牌陣與正逆位。
- 牌意資料存放於 `data/cards/`，抽牌引擎在 `core/tarot/engine.py`。
### 2. 易經卜卦 (I-Ching)
- 模擬 6 次擲幣產生初爻至上爻，正面(陽)=3，反面(陰)=2。6(老陰)、9(老陽)為動爻，進一步產生變卦。
- 卦象資料存放於 `data/hexagrams/64_hexagrams.json`。
### 3. 諸葛神算 (Zhuge Shensuan)
- 提供 384 籤，搭配傳統詩文與籤意解釋。
- 籤詩庫位於 `data/zhuge/zhuge_data.json`，抽籤引擎在 `core/zhuge/engine.py`。
### 4. 大六壬 (Da Liu Ren)
- 基於時辰隨機起課，涵蓋節氣、時局、格局、三傳、四課等深度命理資訊。
- 排盤引擎位於 `core/daliuren/engine.py` (整合 `kinliuren` 套件)。

## UI 與前端開發規範
- 後台管理端：`streamlit run app.py` (預設啟動於 8501 Port)。
- 使用者前端：在 `frontend/` 下執行 `npm run dev`，畫面包含四個主頁籤：塔羅占卜、易經卜卦、諸葛神算、大六壬，並支援多國語系 (i18n) 以及手機版 RWD 響應式排版。
- 圖片統一以 `backend/assets/images/` 為準。

## FastAPI 與 AI Skill 整合
- 執行指令：在 `backend/` 下執行 `python run_api.py` (獨立於 Streamlit，預設啟動於 8000)。
- 作為外部介面，API 端點 (如 `/api/tarot/draw`, `/api/iching/cast`, `/api/zhuge/draw`, `/api/daliuren/cast`) 讓 AI Agent 能夠免寫爬蟲直接取用。
- AI Agent 可直接閱讀 `.agent/skills/ai-divination-api/SKILL.md` 的說明文件了解操作方法，大幅提升專案的擴展性。

## 未來擴充
- RAG（檢索增強生成）：導入專屬的易經/塔羅文獻向量庫，豐富 AI 解答的歷史與典故厚度。
- AI Agent 互動對話：設計對話代理人，引導使用者收斂問題、靜心卜卦。
