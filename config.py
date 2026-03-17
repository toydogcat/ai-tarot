"""全域設定檔"""
from pathlib import Path

# 專案根目錄
BASE_DIR = Path(__file__).resolve().parent

# 資料路徑
DATA_DIR = BASE_DIR / "data" / "cards"
MAJOR_ARCANA_FILE = DATA_DIR / "major_arcana.json"
MINOR_ARCANA_FILE = DATA_DIR / "minor_arcana.json"

# 圖片路徑
ASSETS_DIR = BASE_DIR / "assets" / "images"
CARD_BACK_IMAGE = ASSETS_DIR / "card_back.png"
MAJOR_IMAGES_DIR = ASSETS_DIR / "major"
MINOR_IMAGES_DIR = ASSETS_DIR / "minor"

# 牌組設定
TOTAL_CARDS = 78
MAJOR_ARCANA_COUNT = 22
MINOR_ARCANA_COUNT = 56
REVERSE_PROBABILITY = 0.5  # 逆位機率

# 小阿爾克那花色
SUITS = ["wands", "cups", "swords", "pentacles"]
SUITS_ZH = {
    "wands": "權杖",
    "cups": "聖杯",
    "swords": "寶劍",
    "pentacles": "錢幣",
}

# Streamlit 頁面設定
PAGE_TITLE = "🔮 AI 塔羅占卜"
PAGE_ICON = "🔮"
PAGE_LAYOUT = "wide"
