# 塔羅牌圖片生成指南（Nano Banana）

## 圖片存放位置

所有圖片放在 `assets/images/` 下：

```
assets/images/
├── card_back.png                  # 牌背（1 張）
├── major/                         # 大阿爾克那（22 張）
│   ├── 00_the_fool.png
│   ├── 01_the_magician.png
│   ├── 02_the_high_priestess.png
│   ├── 03_the_empress.png
│   ├── 04_the_emperor.png
│   ├── 05_the_hierophant.png
│   ├── 06_the_lovers.png
│   ├── 07_the_chariot.png
│   ├── 08_strength.png
│   ├── 09_the_hermit.png
│   ├── 10_wheel_of_fortune.png
│   ├── 11_justice.png
│   ├── 12_the_hanged_man.png
│   ├── 13_death.png
│   ├── 14_temperance.png
│   ├── 15_the_devil.png
│   ├── 16_the_tower.png
│   ├── 17_the_star.png
│   ├── 18_the_moon.png
│   ├── 19_the_sun.png
│   ├── 20_judgement.png
│   └── 21_the_world.png
└── minor/                         # 小阿爾克那（56 張）
    ├── wands/                     # 權杖
    │   ├── ace_of_wands.png
    │   ├── two_of_wands.png
    │   ├── three_of_wands.png
    │   ├── four_of_wands.png
    │   ├── five_of_wands.png
    │   ├── six_of_wands.png
    │   ├── seven_of_wands.png
    │   ├── eight_of_wands.png
    │   ├── nine_of_wands.png
    │   ├── ten_of_wands.png
    │   ├── page_of_wands.png
    │   ├── knight_of_wands.png
    │   ├── queen_of_wands.png
    │   └── king_of_wands.png
    ├── cups/                      # 聖杯
    │   ├── ace_of_cups.png
    │   ├── two_of_cups.png
    │   ├── ... (同上格式)
    │   └── king_of_cups.png
    ├── swords/                    # 寶劍
    │   ├── ace_of_swords.png
    │   ├── ... (同上格式)
    │   └── king_of_swords.png
    └── pentacles/                 # 錢幣
        ├── ace_of_pentacles.png
        ├── ... (同上格式)
        └── king_of_pentacles.png
```

## 圖片規格要求

| 項目 | 要求 |
|------|------|
| **格式** | PNG（建議）或 JPG |
| **尺寸** | 寬 400px × 高 700px（比例約 4:7，標準塔羅牌比例） |
| **方向** | 直式（Portrait） |
| **背景** | 實色或透明皆可，建議統一風格 |
| **解析度** | 72~150 DPI 即可（Web 用途） |
| **檔案大小** | 建議每張 < 500KB |

> **重要**：所有牌面圖片必須是**正位**的，逆位會由程式自動旋轉 180° 顯示。

---

## Nano Banana 範例提示詞

### 統一風格前綴（建議每張都加）

```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
rich jewel-tone colors, detailed symbolic imagery, portrait orientation 4:7 ratio,
dark mystical background with subtle starfield
```

### 大阿爾克那範例

#### 0 - 愚者 The Fool
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"The Fool" tarot card, a young figure in colorful clothes standing at the edge
of a cliff, holding a white rose, a small white dog at their feet, bright sun
in background, a bindle over shoulder, carefree expression, rich jewel-tone colors,
Roman numeral "0" at top, detailed symbolic imagery, dark mystical background
```

#### I - 魔術師 The Magician
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"The Magician" tarot card, a robed figure standing before a table with a cup,
sword, pentacle and wand, one hand pointing to sky, other to ground, infinity
symbol above head, red and white robes, roses and lilies, Roman numeral "I" at top,
rich jewel-tone colors, detailed symbolic imagery
```

#### II - 女祭司 The High Priestess
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"The High Priestess" tarot card, a serene woman seated between two pillars marked
B and J, holding a scroll labeled TORA, crescent moon at her feet, blue robes,
a veil with pomegranates behind her, Roman numeral "II" at top, rich jewel-tone colors,
mysterious atmosphere
```

#### XIII - 死神 Death
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"Death" tarot card, a skeleton knight in black armor riding a white horse,
carrying a flag with a white rose, figures of all ages before the horse,
a sun rising between two towers in background, Roman numeral "XIII" at top,
rich jewel-tone colors, transformation symbolism
```

#### XXI - 世界 The World
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"The World" tarot card, a figure dancing inside a large laurel wreath,
holding two wands, surrounded by four creatures in corners (angel, eagle, lion, bull),
ribbons wrapping the wreath, celestial feeling, Roman numeral "XXI" at top,
rich jewel-tone colors, sense of completion and harmony
```

### 小阿爾克那範例

#### 權杖 Ace — Ace of Wands
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"Ace of Wands" tarot card, a hand emerging from a cloud holding a sprouting
wooden wand with fresh green leaves, a castle on a distant hill, rolling landscape
below, rich jewel-tone colors, fire element energy, new beginnings symbolism
```

#### 聖杯 King — King of Cups
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"King of Cups" tarot card, a mature king seated on a throne amid turbulent seas,
holding a golden cup in one hand and a scepter in the other, a ship and dolphin
in background, calm expression despite stormy waters, blue and gold robes,
water element symbolism, rich jewel-tone colors
```

#### 寶劍 Ten — Ten of Swords
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"Ten of Swords" tarot card, a figure lying face down with ten swords in their back,
dark sky above transitioning to golden dawn on horizon, calm water in background,
dramatic but symbolic scene, air element, rich jewel-tone colors, ending and
new dawn symbolism
```

#### 錢幣 Page — Page of Pentacles
```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"Page of Pentacles" tarot card, a young figure standing in a lush green field,
holding up a single golden pentacle with both hands, gazing at it with focus
and wonder, flowers at feet, mountains in distance, earth element energy,
rich jewel-tone colors, study and dedication symbolism
```

### 牌背
```
Tarot card back design, mystical art nouveau style, ornate golden border frame,
intricate mandala-like pattern, celestial symbols (stars, moon, sun), deep
midnight blue and gold color scheme, symmetrical sacred geometry design,
mysterious and elegant, no text, rich jewel-tone accents
```

---

## 提示詞公式

可以依照這個公式自行生成每張牌：

```
Tarot card illustration, mystical art nouveau style, ornate golden border frame,
"[牌名英文]" tarot card, [主要場景描述], [主要人物/物件], [背景元素],
[象徵物件], Roman numeral "[對應羅馬數字]" at top, rich jewel-tone colors,
[對應元素] element symbolism, detailed symbolic imagery
```

### 元素對應
- 權杖 Wands → fire element（火）
- 聖杯 Cups → water element（水）
- 寶劍 Swords → air element（風）
- 錢幣 Pentacles → earth element（土）
