---
name: ai-divination-api
description: 教導 AI 助理如何透過本機啟動的 FastAPI 提供占卜服務，包括塔羅與易經。
---

# AI Divination API Integration Skill

這份文件教導身為 AI 助理的你，如何透過本機的 FastAPI 伺服器，直接呼叫塔羅與易經的占卜核心功能，而無需強制依賴 Streamlit 前端 UI。
這非常適合當人類要求你「幫我算塔羅」或是「幫我卜筮」時，你可以直接在背景使用 API 取得結果並回答人類！

## Prerequisites (前置作業)

使用此技能前，請確認後端 API 已啟動。你要使用你的 `run_command` 工具背景執行以下指令：
```bash
python run_api.py
```
> 指令預設會跑在 `http://127.0.0.1:8000`。你可以使用 `curl http://127.0.0.1:8000/` 確認 API 是否活著。

## 🔮 塔羅占卜 (Tarot) 流程

想要進行塔羅占卜，請呼叫 `/api/tarot/draw`。

**Endpoint:** `POST /api/tarot/draw`
**Request JSON Body:**
```json
{
  "spread_id": "single",
  "question": "（可選）使用者的問題"
}
```
*註：`spread_id` 支援 `single`, `three_card`, `time_flow`, `two_options`, `horseshoe`, `celtic_cross`。若不知道要用什麼牌陣，預設使用 `single`。*

**範例呼叫:**
```bash
curl -X POST "http://127.0.0.1:8000/api/tarot/draw" \
     -H "Content-Type: application/json" \
     -d '{"spread_id": "single", "question": "我今天的運氣如何？"}'
```
**回傳重點:** 
API 會回傳抽出牌的 JSON，並自動在背景呼叫 AI 進行解讀（如果有帶 `question` 的話）。請讀取回傳 JSON 裡的 `interpretation` 欄位展現給使用者看。若有生成語音，也會回傳 `audio_path`，可以提示使用者語音放在該路徑。

## ☯️ 易經卜卦 (I-Ching) 流程

**Endpoint:** `POST /api/iching/cast`
**Request JSON Body:**
```json
{
  "question": "（可選）使用者的問題"
}
```

**範例呼叫:**
```bash
curl -X POST "http://127.0.0.1:8000/api/iching/cast" \
     -H "Content-Type: application/json" \
     -d '{"question": "這份工作適合我嗎？"}'
```
**回傳重點:**
API 會自動幫你模擬六次擲骰，並回傳卦象 `hexagram_name`、`lines` 等。若你帶上了 `question`，回傳的 JSON 裡會有 `interpretation`。
你只需要把 `interpretation` 的內容整理後回報給使用者即可。

## 給 AI Agent 的重要原則
1. **先確認再執行**：如果你收到人類的模糊指令 (例如：「幫我占卜」)，請先問他想算塔羅還是易經，以及具體的問題。
2. **自己消化詮釋**：API 回傳的 `interpretation` 已經是我們這個系統的 AI 核心解讀結果。你不需要重新解讀，只需要直接展示或稍作整理回答人類即可。
