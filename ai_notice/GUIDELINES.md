# AI Tarot 專案開發注意事項

## 環境設定
- **Python 環境**：使用 Conda `toby` 環境
  - 路徑：`/home/toymsi/miniconda3/envs/toby/bin/python`
  - 啟用方式：`conda activate toby`
- **環境變數**：複製 `.env.example` 為 `.env` 並填入實際值
- **依賴安裝**：`pip install -r requirements.txt`

## 專案結構規範
| 目錄 | 用途 |
|------|------|
| `data/cards/` | 塔羅牌意 JSON 資料（大小阿爾克那） |
| `assets/images/` | 牌面圖片資源 |
| `core/` | 核心邏輯（牌組、引擎、牌陣） |
| `ui/` | Streamlit UI 元件與頁面 |

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
- 所有敏感資訊（API Key 等）放入 `.env`，禁止 commit
- 新增模組時遵循現有資料夾結構

## 未來擴充
- AI 解牌功能（接入 LLM API）
- 牌意資料庫擴充（更詳細的解釋、故事背景）
- 使用者占卜紀錄
