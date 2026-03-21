# 🔮 AI Tarot & ☯️ I-Ching

[English](README.md) | [繁體中文](README_zh.md)

AI 驅動的塔羅牌與易經卜卦 Web 應用，提供直覺的占卜體驗與專業的管理後台。

### 🌟 一般使用者占卜介面 (Vite 前端)
<p align="center">
  <img src="sample/demo2.jpg" alt="AI Tarot & I-Ching UI" width="600">
  <img src="sample/demo2_android.jpg" alt="Mobile UI" height="350">
</p>

### ⚙️ 專業解讀與測試管理 (Streamlit 介面)
<p align="center">
  <img src="sample/demo1.jpg" alt="AI Tarot & I-Ching Backend" width="800">
</p>
## 功能特色

- 🔮 **塔羅占卜**：完整 78 張塔羅牌、6 種經典牌陣、正逆位支援、詳細牌意。
- ☯️ **易經卜卦**：模擬傳統金錢六爻卜卦，自動呈現本卦、變卦及動爻指示。
- 🎋 **諸葛神算**：提供 384 籤傳統詩文與解意，結合 AI 進行白話精準解析。
- 🌌 **大六壬**：基於時辰起課，提供三傳四課的簡易排盤與格局，讓 AI 根據時空能量為您解讀吉凶。
- 🗣️ **語音輸入提問**：支援麥克風語音轉文字辨識，並可於輸入框手動微調。
- 🔍 **Tavily 外部時事搜尋**：自動從網路搜尋最新話題/時事背景（由 Gemma 3 整理摘要）。
- 🤖 **Gemini AI 深度解析**：結合牌陣/卦象與外部時事，透過最新 Gemini 3.1 Flash/Pro 引擎做深入推演。
- 💾 **統一歷史紀錄與專屬過濾**：完整紀錄解讀與語音狀態，支援依「客戶名稱」在 Streamlit 後台直接下拉篩選歷史，並具備 CLI 技能修復失敗紀錄。
- ⚡ **WebSocket 即時多用戶通訊**：導入 WebSocket 雙向即時連線，完美隔離並同步「導師 (Toby)」與「客戶端」的即時抽牌體驗，確保畫面零時差且不互相干擾。
- ⚙️ **Hydra 動態設定管理**：透過 YAML 設定檔 (Customer1, Customer2) 隨時切換 AI 模型，並可由 Streamlit 後台一鍵自訂所有占卜系統（塔羅、易經、諸葛、大六壬）的專屬提示詞。
- 🎵 **背景音樂 (BGM)**：可於設定檔或管理介面無縫切換多種冥想背景音樂，增添占卜氛圍。
- 🎨 **自訂圖片格式**：支援 JPG/PNG 精美 AI 生成圖無縫切換。
- 🚀 **FastAPI 與 AI Agent Skill**：獨立的後端 API 端點 (`/api/tarot/draw` 等) 與 AI 技能說明文檔，讓未來的 AI Agent 也能自由幫你呼叫占卜服務。

## 快速開始

目前專案採用 **前後端分離 (Monorepo)** 架構：
- `backend/` 包含 FastAPI 後端、AI 邏輯與 Streamlit 測試管理介面。
- `frontend/` 包含 Vite 打包的極致客製化 HTML/CSS/JS 前端。

### 1. 啟動後端 API 與管理介面

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 啟動 FastAPI (預設 Port 8000)
python run_api.py

# (可選) 啟動 Streamlit 管理與測試介面 (預設 Port 8501)
streamlit run app.py
```

### 2. 啟動華麗的 Vite 前端

請另外開一個終端機：

```bash
cd frontend
npm install
npm run dev
```
接著在瀏覽器打開 `http://localhost:5173` 即可體驗極致的占卜 UI。

### 3. 下載圖片資源

由於圖片檔案過大，請從以下來源下載圖片壓縮檔 `ai-tarot-images.zip`：
[👉 點此下載圖片資源 (Google Drive)](https://drive.google.com/file/d/1e0_HGeluSyamB-rykJzBZsJj6w8Nln09/view?usp=sharing)

下載後，將 `ai-tarot-images.zip` 放入專案的 `assets/` 資料夾，並解壓縮出 `images/` 目錄。
最終結構應為：
```
assets/
└── images/
    ├── tarot/
    └── iching/
```
若在沒有圖片的情況下啟動，UI 會自動以無圖片的圖文方塊替代顯示，不會報錯。

### 3. 環境變數設定

```bash
# 複製 .env 範例檔
cp .env.example .env

# 編輯 .env 填入必要的 API Keys:
# GEMINI_API_KEY=your_gemini_key
# TAVILY_API_KEY=your_tavily_key
```

### 3. 啟動應用

本專案支援 **本機啟動** (0.0.0.0) 以及 **Ngrok 遠端分享**。

#### 一般啟動 (本機 0.0.0.0 分享)
```bash
python run.py
# 或是直接使用 streamlit:
# streamlit run app.py --server.address=0.0.0.0
```
瀏覽器會自動開啟 `http://localhost:8501`。相同區域網路下的設備可以透過您的區域 IP 存取 (例如 `http://192.168.1.xxx:8501`)。

#### API 伺服器啟動 (供 AI Agent / 擴充使用)
若要啟動 FastAPI 背景服務，請另外開啟終端機執行：
```bash
python run_api.py
```
API 將預設運行於 `http://localhost:8000`。您可以透過 `http://localhost:8000/docs` 測試 Swagger UI。

#### Ngrok 外網遠端分享啟動
若需要將 Tarot App 分享給外網使用者，專案內建整合了 Ngrok：
1. 前往 Ngrok 註冊並獲取 [Auth Token](https://dashboard.ngrok.com/get-started/your-authtoken)
2. 將 Token 寫入 `.env` 檔案中：`NGROK_AUTHTOKEN=你的token`
3. 執行統一啟動腳本：
   ```bash
   python run.py
   ```
4. 終端機會印出類似 `Ngrok 隧道開啟成功！遠端存取請前往: https://1234abcd.ngrok-free.app` 的網址，將該隨機網址分享給他人即可。

## 🧪 自動化測試 (Unit Testing)

本專案於 `backend/tests/` 提供了基於 `pytest` 的完整單元測試。涵蓋了以下核心模組：
- **WebSocket 通訊**：測試多連線隔離與「導師 (Toby) / 客戶」的獨立廣播機制。
- **動態設定 (ConfigManager)**：驗證 YAML 設定檔的讀寫與預設值備援。
- **歷史紀錄 (History API)**：驗證依據「客戶名稱」建立的歷史紀錄篩選機制。
- **AI 占卜解析引擎 (Interpreters)**：模擬並驗證即將傳入 Gemini 模型的推演 Prompt 架構是否正確載入系統設定。

**執行測試：**

```bash
cd backend
# 啟動虛擬環境 (或者您的 conda 環境)
source venv/bin/activate
pip install pytest pytest-asyncio httpx
PYTHONPATH=. pytest -v tests/
```

## 專案結構

```text
ai-tarot/
├── frontend/               # Vite 前端專案 (使用者介面)
│   ├── index.html          # 主頁面與多語系標籤
│   ├── src/main.js         # 前端核心邏輯與動態 UI
│   ├── public/             # 靜態公共資源
│   └── vite.config.js      # Vite 開發伺服器與 API 代理設定
├── backend/                # FastAPI / Streamlit 後端專案
│   ├── run_api.py          # FastAPI 啟動入口 (8000)
│   ├── app.py              # Streamlit 測試與管理後台 (8501)
│   ├── run.py              # 整合啟動程式
│   ├── api/                # FastAPI 路由與 schemas 定義
│   ├── core/               # 核心推演引擎 (塔羅、易經、AI解析、語音)
│   ├── config/             # Hydra 設定檔目錄 (default/customer YAML)
│   ├── assets/             # 塔羅/易經圖片資源與背景音樂
│   ├── data/               # 靜態定義庫 (JSON)
│   ├── history/            # 使用者占卜紀錄存放區
│   ├── tools/              # 錯誤修復與紀錄移轉腳本
│   └── ui/                 # Streamlit UI 專用元件
├── ai_notice/              # 開發指南與規範文檔
├── share_ngrok.py          # Ngrok 自動化外網分享腳本
├── .env.example            # 環境變數範例檔
└── README.md               # 專案總說明文件
```

## 圖片資源

牌面圖片放在 `assets/images/` 目錄下。詳見 [IMAGE_GUIDE.md](ai_notice/IMAGE_GUIDE.md) 了解檔名格式與生成提示詞。

## 致謝 (Credits)

本專案的完滿落成，特別感謝以下工具與團隊的強大支援：
- 🎵 **背景音樂 (Music)**：由 [Suno](https://suno.com/) AI 音樂平台生成。Suno 讓創作專屬氛圍的冥想音樂變得無比簡單，為占卜過程帶來絕佳的沉浸體驗。
- 🎨 **視覺圖像 (Images)**：牌面與卦象圖片是由強大的 [Nano Banana2](https://civitai.com/models/25995?modelVersionId=32988) 視覺基準模型生成，完美呈現了精妙的東方禪意與神祕學色彩。
- 💻 **協作工程師 (Programming)**：專案核心架構、API 整合與程式碼重構打磨，由 Google DeepMind 打造的 agentic AI 軟體工程師 **Antigravity** 共同協助開發完成。

## License

MIT

