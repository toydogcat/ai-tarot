---
name: tarot-iching-error-recovery-fast
description: 快速修復占卜歷史中 AI 解讀失敗 (error) 的紀錄，支援所有占卜類型，使用 AI 重新生成解讀
---

# 🔮 全能 Error Recovery Fast — AI 解讀快速救援技能

## 功能說明

修復 `backend/history/` 資料夾中 `ai_status.interpretation` 為 `"error"` 的占卜紀錄。根據該次紀錄中的使用者提問、占卜類型和結果，重新呼叫 Gemini API 生成解讀。

## 使用時機

- 使用者回報 AI 占卜解讀失敗
- 在 Streamlit 歷史紀錄頁面看到 ❌ 標記的紀錄
- 批次修復所有 error 紀錄

## SOP 操作步驟

### 步驟 1：確認環境

檢查 `backend/.env` 檔中python環境 `PYTHON_PATH`，`CONDA_ENV`。

```bash
cat backend/.env | grep PYTHON_PATH
cat backend/.env | grep CONDA_ENV
```


### 步驟 2：查看 error 紀錄

使用修復腳本查看所有 error 紀錄：

```bash
conda activate toby
cd backend
python tools/repair_readings.py --list
```

這會列出所有文字解牌 (`interpretation`) 或語音 (`audio`) 錯誤的紀錄，包含日期、ID、問題和牌面。

### 步驟 3：修復特定紀錄

找 `ai_status.interpretation` 為 error 的紀錄，就根據紀錄中的 `ai_prompt` 重新生成解讀，並更新 `ai_interpretation`。

### 步驟 4：生成語音

當有網路連線時，`ai_interpretation`轉換為語音，優先使用 edge-tts (台灣口音女聲 zh-TW-HsiaoChenNeural) 產生高品質的語音。
若偵測到無網路連線，將自動 fallback 到離線的 pyttsx3，確保功能隨時可用。
生成的語音檔案會儲存於 `backend/history/audio` 資料夾中，並且給出隨機名稱，並更新紀錄中的 `ai_interpretation_audio_path`。

### 步驟 5：驗證修復結果

修復後的紀錄 `ai_status.interpretation` 皆會更新為 `"success"`（若語音也成功則 `ai_status.audio` 為 `"success"`），並加上 `recovered_at` 時間戳。

在 Streamlit 歷史頁面中：
- ✅ = 原始成功
- 🔄 = 已修復
- ❌ = 尚未修復

## 相關檔案

| 檔案 | 用途 |
|------|------|
| `backend/tools/repair_readings.py` | 修復腳本 |
| `backend/core/history.py` | History 紀錄管理 |
| `backend/core/tts.py` | TTS 語音生成 |
| `backend/core/interpreter.py` | Gemini 提示詞建構 |
| `backend/history/*.json` | 占卜紀錄檔案 |

## 提示詞邏輯

修復時使用與正常占卜完全相同的提示詞模板（`backend/core/interpreter.py` 中的 `build_interpretation_prompt`），確保解讀品質一致。差別在於資料來源從即時抽牌結果改為從 history JSON 中讀取。
