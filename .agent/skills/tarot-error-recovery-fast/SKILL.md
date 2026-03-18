---
name: tarot-error-recovery-fast
description: 快速修復占卜歷史中 AI 解牌失敗 (error) 的紀錄，使用 AI 重新生成解讀
---

# 🔮 Tarot Error Recovery Fast — AI 解牌救援技能

## 功能說明

修復 `history/` 資料夾中 `ai_status` 為 `"error"` 的占卜紀錄。根據該次紀錄中的使用者提問、牌陣和抽牌結果，重新呼叫 Gemini API 生成解讀。

## 使用時機

- 使用者回報 AI 解牌失敗
- 在 Streamlit 歷史紀錄頁面看到 ❌ 標記的紀錄
- 批次修復所有 error 紀錄

## SOP 操作步驟

### 步驟 1：確認環境

檢查 `.env` 檔中python環境 `PYTHON_PATH`，`CONDA_ENV`。

```bash
cat .env | grep PYTHON_PATH
cat .env | grep CONDA_ENV
```


### 步驟 2：查看 error 紀錄

使用修復腳本查看所有 error 紀錄：

```bash
conda activate toby
python tools/repair_readings.py --list
```

這會列出所有 AI 狀態為 error 的紀錄，包含日期、ID、問題和牌面。

### 步驟 3：修復特定紀錄

找狀態為 error 的紀錄，就根據紀錄中的 `ai_prompt` 重新生成解讀，並更新 `ai_interpretation`。

### 步驟 4：生成語音

當有網路連線時，`ai_interpretation`轉換為語音，優先使用 edge-tts (台灣口音女聲 zh-TW-HsiaoChenNeural) 產生高品質的語音。
若偵測到無網路連線，將自動 fallback 到離線的 pyttsx3，確保功能隨時可用。
生成的語音檔案會儲存於 `history/audio` 資料夾中，並且給出隨機名稱，並更新紀錄中的 `ai_interpretation_audio_path`。

### 步驟 5：驗證修復結果

修復後的紀錄 `ai_status` 都會變成 `"recovered"`，並加上 `recovered_at` 時間戳。

在 Streamlit 歷史頁面中：
- ✅ = 原始成功
- 🔄 = 已修復
- ❌ = 尚未修復

## 相關檔案

| 檔案 | 用途 |
|------|------|
| `tools/repair_readings.py` | 修復腳本 |
| `core/history.py` | History 紀錄管理 |
| `core/tts.py` | TTS 語音生成 |
| `core/interpreter.py` | Gemini 提示詞建構 |
| `history/*.json` | 占卜紀錄檔案 |

## 提示詞邏輯

修復時使用與正常占卜完全相同的提示詞模板（`core/interpreter.py` 中的 `build_interpretation_prompt`），確保解讀品質一致。差別在於資料來源從即時抽牌結果改為從 history JSON 中讀取。
