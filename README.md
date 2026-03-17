# 🔮 AI 塔羅占卜

AI 驅動的塔羅牌占卜 Web 應用，使用 Streamlit 打造。

## 功能特色

- 📦 完整 78 張塔羅牌（22 張大阿爾克那 + 56 張小阿爾克那）
- 🔄 支援正位與逆位
- 🃏 6 種經典牌陣：單牌、三牌、時間之流、二擇一、馬蹄形、凱爾特十字
- 📖 每張牌附有繁體中文牌意解讀

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
# 編輯 .env 填入你的設定
```

### 3. 啟動應用

```bash
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`

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
│   └── spreads.py          # 牌陣定義
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

