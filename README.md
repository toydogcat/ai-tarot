# 🔮 AI Tarot & ☯️ I-Ching

AI 驅動的塔羅牌與易經卜卦 Web 應用，使用 Streamlit 打造。

## 功能特色

- 🔮 **塔羅占卜**：完整 78 張塔羅牌、6 種經典牌陣、正逆位支援、詳細牌意。
- ☯️ **易經卜卦**：模擬傳統金錢六爻卜卦，自動呈現本卦、變卦及動爻指示。
- 🗣️ **語音輸入提問**：支援麥克風語音轉文字辨識，並可於輸入框手動微調。
- 🔍 **Tavily 外部時事搜尋**：自動從網路搜尋最新話題/時事背景（由 Gemma 3 整理摘要）。
- 🤖 **Gemini AI 深度解析**：結合牌陣/卦象與外部時事，透過最新 Gemini 3.1 Flash/Pro 引擎做深入推演。
- 💾 **統一歷史紀錄與修復**：完整紀錄解讀與語音狀態，支援 CLI 技能修復塔羅與易經的失敗紀錄。
- ⚙️ **Hydra 動態設定管理**：透過 YAML 設定檔 (Customer1, Customer2) 隨時切換 AI 模型、修改提示詞範本並還原出廠預設值。
- 🎨 **自訂圖片格式**：支援 JPG/PNG 精美 AI 生成圖無縫切換。

## 快速開始

### 1. 環境準備

```bash
# 使用 Conda 啟用 toby 環境
conda activate toby

# 安裝依賴
pip install -r requirements.txt
```

### 2. 下載圖片資源

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

#### Ngrok 外網遠端分享啟動
若需要將 Tarot App 分享給外網使用者，專案內建整合了 Ngrok：
1. 前往 Ngrok 註冊並獲取 [Auth Token](https://dashboard.ngrok.com/get-started/your-authtoken)
2. 將 Token 寫入 `.env` 檔案中：`NGROK_AUTHTOKEN=你的token`
3. 執行統一啟動腳本：
   ```bash
   python run.py
   ```
4. 終端機會印出類似 `Ngrok 隧道開啟成功！遠端存取請前往: https://1234abcd.ngrok-free.app` 的網址，將該隨機網址分享給他人即可。

## 專案結構

```
ai-tarot/
├── app.py                  # Streamlit 主程式
├── config.py               # 全域設定
├── requirements.txt        # 依賴套件
├── data/                     # 靜態資料 (JSON)
│   ├── tarot/                # 塔羅牌資料
│   └── iching/               # 易經 64 卦資料
├── assets/images/            # 圖片資源
│   ├── tarot/                # 塔羅牌圖片
│   └── iching/hexagrams/     # 易經意境圖片
├── core/                     # 核心邏輯
│   ├── tarot/                # 塔羅相關邏輯 (引擎、牌陣、解析)
│   ├── iching/               # 易經相關邏輯 (引擎、解析)
│   ├── search.py             # Tavily 搜尋與 Gemma 摘要
│   ├── history.py            # 歷史紀錄管理 (統一 Tarot & I-Ching)
│   ├── tts.py                # 語音合成生成
│   └── audio_input.py        # 語音輸入與轉換處理
├── tools/                  # 工具腳本
│   ├── repair_readings.py  # 補件與修復程式
│   └── migrate_history_status.py # 狀態格式轉換程式
├── ui/                     # UI 元件
│   ├── tarot_ui.py         # 塔羅專用元件
│   └── iching_ui.py        # 易經專用元件
├── config/                 # Hydra YAML 設定檔目錄
│   ├── default.yaml        # 出廠預設值設定檔
│   ├── customer1.yaml      # 客戶 1 動態設定
│   └── customer2.yaml      # 客戶 2 動態設定
└── ai_notice/              # 開發指南
    ├── GUIDELINES.md       # 專案規範 (整合版)
    ├── IMAGE_GUIDE.md      # 圖片生成指南 (整合版)
    └── ToDo.md             # 待辦事項
```

## 圖片資源

牌面圖片放在 `assets/images/` 目錄下。詳見 [IMAGE_GUIDE.md](ai_notice/IMAGE_GUIDE.md) 了解檔名格式與生成提示詞。

## License

MIT

