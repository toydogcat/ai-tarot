# AI Tarot 專案開發注意事項

## 環境設定
- **Python 環境**：使用 Conda `toby` 環境
  - 路徑：`/home/toymsi/miniconda3/envs/toby/bin/python`
  - 啟用方式：`conda activate toby`
- **環境變數**：複製 `.env.example` 為 `.env` 並填入你的 `GEMINI_API_KEY` 與 `TAVILY_API_KEY`
- **依賴安裝**：`pip install -r requirements.txt` (請確認套件含 `tavily-python`, `SpeechRecognition`, `pydub`, `streamlit-mic-recorder` 等最新相依套件)

## 專案結構規範
| 目錄 | 用途 |
|------|------|
| `data/cards/` | 塔羅牌意 JSON 資料（大小阿爾克那） |
| `assets/images/` | 牌面圖片資源 |
| `core/` | 核心邏輯（包含：引擎、牌陣、AI 解析器、Tavily 搜尋、語音處理、歷史狀態） |
| `tools/` | 輔助工具（例如佔卜狀態修復腳本與結構轉換腳本） |
| `history/` | 使用者歷史紀錄 JSON 以及生成的音訊 |
| `ui/` | Streamlit UI 元件與主要頁面 |

## 圖片資源
- 圖片放置於 `assets/images/` 下，分為 `major/` 與 `minor/` 子資料夾
- 小阿爾克那再依花色分：`wands/`、`cups/`、`swords/`、`pentacles/`
- 命名規則：
  - 大阿爾克那：`{編號}_{英文名}.png`，例如 `00_the_fool.png`
  - 小阿爾克那：`{英文名}.png`，例如 `ace_of_wands.png`
- 目前使用程式生成的佔位圖，可直接替換為真實牌圖（保持相同檔名）

## 牌意資料格式
- 使用 JSON 格式，存放於 `data/cards/`
- 每張牌包含：`id`、`name`、`name_zh`、`image`、`upright`、`reversed`
- 牌意以**繁體中文**撰寫

## 開發規範
- 執行 Streamlit：`streamlit run app.py`
- 所有的環境變數與敏感資訊（`GEMINI_API_KEY`、`TAVILY_API_KEY`、`NGROK_AUTHTOKEN`）放入 `.env`，禁止 commit
- 核心邏輯需模組化（例如搜尋交給 `search.py`、音訊交給 `audio_input.py`）
- 在操作 `history`（`ai_status`）時，務必確保使用的是 Dictionary (`{"interpretation": "...", "audio": "...", "search": "..."}`) 而非舊式字串

## 未來擴充
- 進一步強化牌意資料庫（加入逆位特化情境或故事背景）
- 支援使用者自定義牌陣或問題分類
- RAG（檢索增強生成）：讓 AI 自動回顧使用者過往的測算紀錄並給出綜合建言
