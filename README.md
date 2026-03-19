# 🔮 AI 塔羅占卜

AI 驅動的塔羅牌占卜 Web 應用，使用 Streamlit 打造。

## 功能特色

- 📦 完整 78 張塔羅牌（22 張大阿爾克那 + 56 張小阿爾克那）
- 🔄 支援正位與逆位
- 🃏 6 種經典牌陣：單牌、三牌、時間之流、二擇一、馬蹄形、凱爾特十字
- 📖 每張牌附有繁體中文牌意解讀
- 🗣️ **語音輸入提問**：支援麥克風語音轉文字辨識，並可於輸入框手動微調
- 🔍 **Tavily 外部時事搜尋**：自動從網路搜尋最新話題/時事背景（由 Gemma 3 整理摘要）
- 🤖 **Gemini AI 解牌**：結合牌陣與外部時事，透過最新 Gemini 3.1 Flash Lite 引擎做深入推演
- 💾 **歷史紀錄與修復**：以複合狀態（Dictionary）完整紀錄解牌與語音狀態，支援 CLI 技能補件

## 快速開始

### 1. 環境準備

```bash
# 使用 Conda 啟用 toby 環境
conda activate toby

# 安裝依賴
pip install -r requirements.txt
```

### 2. 環境變數設定

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
├── data/cards/             # 牌意資料 (JSON)
│   ├── major_arcana.json   # 大阿爾克那 22 張
│   └── minor_arcana.json   # 小阿爾克那 56 張
├── assets/images/          # 牌面圖片
│   ├── major/              # 大阿爾克那圖片
│   └── minor/              # 小阿爾克那圖片 (wands/cups/swords/pentacles)
├── core/                   # 核心邏輯
│   ├── models.py           # 資料模型
│   ├── deck.py             # 牌組管理
│   ├── engine.py           # 抽牌引擎
│   ├── spreads.py          # 牌陣定義
│   ├── interpreter.py      # Gemini 解析器
│   ├── search.py           # Tavily 搜尋與 Gemma 摘要
│   ├── history.py          # 歷史紀錄管理
│   ├── tts.py              # 語音合成生成
│   └── audio_input.py      # 語音輸入與轉換處理
├── tools/                  # 工具腳本
│   ├── repair_readings.py  # 補件與修復程式
│   └── migrate_history_status.py # 狀態格式轉換程式
├── ui/                     # UI 元件
│   └── components.py       # Streamlit 元件
└── ai_notice/              # 開發指南
    ├── GUIDELINES.md        # 專案規範
    └── IMAGE_GUIDE.md       # 圖片生成指南
```

## 圖片資源

牌面圖片放在 `assets/images/` 目錄下。詳見 [IMAGE_GUIDE.md](ai_notice/IMAGE_GUIDE.md) 了解檔名格式與生成提示詞。

## License

MIT

