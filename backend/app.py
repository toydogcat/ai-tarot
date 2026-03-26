"""🔮 AI 塔羅占卜 — Streamlit 主程式"""
import streamlit as st
import os
from dotenv import load_dotenv

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT
from core.tarot.engine import DrawEngine
from core.tarot.spreads import ALL_SPREADS, get_spread_by_id
from core.logger import get_logger
from ui.tarot_ui import inject_custom_css
from core.config_manager import config_manager

# 匯入各分頁模組
from ui.pages.tarot import render_tarot_page
from ui.pages.iching import render_iching_page
from ui.pages.zhuge import render_zhuge_page
from ui.pages.xlr import render_xlr_page
from ui.pages.dlr import render_dlr_page
from ui.pages.history import render_history_page
from ui.pages.settings import render_settings_page
from ui.pages.approval import render_approval_page

# 載入 .env
load_dotenv()
logger = get_logger("app")

# === 頁面設定 ===
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded",
)

# === 注入樣式 ===
inject_custom_css()

# === 初始化引擎（快取） ===
@st.cache_resource
def get_engine():
    return DrawEngine()

engine = get_engine()

# === 側邊欄 ===
with st.sidebar:
    st.markdown("# 🌟 AI 智慧占卜")
    
    remaining_usage = config_manager.get_remaining_usage()
    st.metric("剩餘可用次數", remaining_usage)
    
    st.markdown("---")

    # 頁面切換
    page = st.radio(
        "📄 頁面",
        ["🔮 塔羅占卜", "☯️ 易經卜卦", "🎋 諸葛神算", "🎲 小六壬", "🌌 大六壬", "📜 歷史紀錄", "⚙️ 設定管理", "🌐 即時觀測", "🛡️ 帳號核准"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # 側邊欄按鈕/控制項初始化
    draw_button = False
    selected_spread = None
    allow_reversed = True
    zhuge_draw_button = False
    xlr_draw_button = False
    dlr_draw_button = False
    iching_draw_button = False

    if page == "🔮 塔羅占卜":
        st.markdown("### 選擇牌陣")
        spread_options = {s.id: f"{s.icon} {s.name}（{s.card_count} 張）" for s in ALL_SPREADS}
        selected_id = st.radio(
            label="選擇牌陣",
            options=list(spread_options.keys()),
            format_func=lambda x: spread_options[x],
            label_visibility="collapsed",
        )
        selected_spread = get_spread_by_id(selected_id)
        if selected_spread:
            st.markdown(f"📝 *{selected_spread.description}*")
        st.markdown("---")
        allow_reversed = st.checkbox("允許逆位", value=True)
        
        st.markdown("### 🖼️ 圖片格式")
        prefer_format = st.radio("圖片格式", ["jpg", "png"], index=0, horizontal=True, label_visibility="collapsed", key="tarot_fmt")
        st.session_state["prefer_image_format"] = prefer_format
        st.markdown("---")
        draw_button = st.button("🃏 開始抽牌", use_container_width=True, type="primary")

    elif page == "🎋 諸葛神算":
        st.info("系統將為您隨機抽取三八四籤之一，並由 AI 進行解籤。")
        zhuge_draw_button = st.button("🎋 開始抽籤", use_container_width=True, type="primary")

    elif page == "🎲 小六壬":
        st.info("系統將隨機產生三個數字，推演小六壬初傳、中傳、終傳，定局吉凶。")
        xlr_draw_button = st.button("🎲 開始起卦", use_container_width=True, type="primary")

    elif page == "🌌 大六壬":
        st.info("系統將隨機產生大六壬課象（四課三傳），並由 AI 解讀吉凶。")
        dlr_draw_button = st.button("🌌 開始起課", use_container_width=True, type="primary")

    elif page == "☯️ 易經卜卦":
        st.info("系統將模擬六次金錢卦擲爻，由下而上產生本卦與變卦。")
        st.markdown("---")
        st.markdown("### 🖼️ 圖片格式")
        prefer_format_iching = st.radio("圖片格式", ["jpg", "png"], index=0, horizontal=True, label_visibility="collapsed", key="iching_fmt")
        st.session_state["prefer_image_format"] = prefer_format_iching
        st.markdown("---")
        iching_draw_button = st.button("🎲 開始卜卦", use_container_width=True, type="primary")

    # 背景音樂
    conf = config_manager.get()
    bgm_id = conf.app.get("bgm_id", 1)
    bgm_path = f"assets/music/background{bgm_id}.mp3"
    if os.path.exists(bgm_path):
        st.markdown("---")
        st.markdown("<p style='text-align:center; color:#B8A88A; margin-bottom:-10px;'>🎵 背景音樂</p>", unsafe_allow_html=True)
        st.audio(bgm_path, format="audio/mp3", autoplay=True, loop=True)

# === 路由分發 ===
if page == "🔮 塔羅占卜":
    render_tarot_page(engine, selected_spread, draw_button, allow_reversed)
elif page == "☯️ 易經卜卦":
    render_iching_page(iching_draw_button)
elif page == "🎋 諸葛神算":
    render_zhuge_page(zhuge_draw_button)
elif page == "🎲 小六壬":
    render_xlr_page(xlr_draw_button)
elif page == "🌌 大六壬":
    render_dlr_page(dlr_draw_button)
elif page == "📜 歷史紀錄":
    render_history_page()
elif page == "⚙️ 設定管理":
    render_settings_page()
elif page == "🛡️ 帳號核准":
    render_approval_page()
elif page == "🌐 即時觀測":
    from ui.observation_ui import render_observation_ui
    render_observation_ui()
