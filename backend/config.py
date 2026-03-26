from pathlib import Path
from core.constants import BASE_DIR
from core.config_manager import config_manager

# 取得目前設定
conf = config_manager.get()

# 資料路徑
TAROT_DATA_DIR = BASE_DIR / conf.paths.data_dir / "tarot"
MAJOR_ARCANA_FILE = TAROT_DATA_DIR / "major_arcana.json"
MINOR_ARCANA_FILE = TAROT_DATA_DIR / "minor_arcana.json"

ICHING_DATA_DIR = BASE_DIR / conf.paths.data_dir / "iching"

# 圖片路徑
TAROT_ASSETS_DIR = BASE_DIR / conf.paths.assets_dir / "tarot"
CARD_BACK_IMAGE = TAROT_ASSETS_DIR / "card_back.png"
MAJOR_IMAGES_DIR = TAROT_ASSETS_DIR / "major"
MINOR_IMAGES_DIR = TAROT_ASSETS_DIR / "minor"

ICHING_ASSETS_DIR = BASE_DIR / conf.paths.assets_dir / "iching"

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
PAGE_TITLE = "🌟 AI 智慧占卜"
PAGE_ICON = "🌟"
PAGE_LAYOUT = "wide"
