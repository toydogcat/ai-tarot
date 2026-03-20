# 背景音樂生成指南（Suno AI）

本專案提供給使用者的冥想背景音樂，是透過 [Suno](https://suno.com/) AI 平台所生成。如果你希望擴充或自己生成新的 BGM 放入 `assets/music/`，請參考以下官方建議的設定與提示詞（Prompt）格式。

---

## 冥想與占卜氛圍（通用版）

這組提示詞能夠穩定產出富有東方禪意、適合靜心占卜的純背景音樂。

### 基本設定
- **Music Style**：純音樂（Instrumental）
- **Lyrics（歌詞）**：空白（請勿填寫任何歌詞）

### 核心提示詞 (Styles / 風格)
請將以下內容貼入 Suno 的 **Style of Music** 欄位：

```text
ambient healing, deep singing bowls, soft guqin, warm pads, slow tempo, zen meditation, atmospheric
```

#### 參數解析：
- **ambient healing**（氛圍療癒）：定調為放鬆、非干擾性的背景音樂。
- **deep singing bowls**（深沉頌缽）：加入沉穩的頌缽共鳴，幫助使用者沈澱心靈。
- **soft guqin**（輕柔古琴）：點綴東方古典樂器，帶出易經與塔羅交織的神祕禪意。
- **warm pads**（溫暖合成器墊音）：填補背景空間，讓聲音更豐滿、溫潤。
- **slow tempo**（慢板節奏）：放慢心跳，適合靜心冥想與深度思考。
- **zen meditation**（禪宗冥想）：強化安定心神的環境感。
- **atmospheric**（充滿氛圍感）：讓音樂具有空間迴蕩感，彷彿置身於神聖的占卜空間。

---

## 擴充音樂檔案

當你在 Suno 上生成並下載滿意的音樂後，請依照以下步驟匯入專案：

1. 將檔案轉換或存為 `.mp3` 格式。
2. 將檔案放入專案的 `assets/music/` 資料夾內。
3. 遵循命名規則，例如 `background3.mp3`、`background4.mp3`。
4. 在 `app.py` 的「管理介面」區塊中，將對應的選項加入至下拉選單：
   ```python
   bgm_options = {"BGM 1": 1, "BGM 2": 2, "BGM 3": 3}
   ```
5. 完成後重新啟動專案，即可在側邊欄看到新的背景音樂選項。
