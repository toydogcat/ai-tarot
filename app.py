"""🔮 AI 塔羅占卜 — Streamlit 主程式"""
import streamlit as st

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT
from core.engine import DrawEngine
from core.spreads import ALL_SPREADS, get_spread_by_id
from ui.components import inject_custom_css, render_spread_result


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
    st.markdown("# 🔮 AI 塔羅占卜")
    st.markdown("---")

    # 牌陣選擇
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

    # 正逆位設定
    allow_reversed = st.checkbox("允許逆位", value=True)

    st.markdown("---")

    # 抽牌按鈕
    draw_button = st.button(
        "🃏 開始抽牌",
        use_container_width=True,
        type="primary",
    )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
        "✨ 靜心冥想你的問題<br>然後點擊抽牌 ✨"
        "</p>",
        unsafe_allow_html=True,
    )

# === 主區域 ===
if draw_button and selected_spread:
    # 抽牌
    result = engine.draw_spread(selected_spread, allow_reversed)

    # 儲存到 session state
    st.session_state["last_result"] = result

# 顯示結果
if "last_result" in st.session_state:
    render_spread_result(st.session_state["last_result"])
else:
    # 歡迎畫面
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 5rem; margin-bottom: 20px;">🔮</div>
        <h1 style="color: #E8D5B7; font-family: 'Noto Serif TC', serif;">
            AI 塔羅占卜
        </h1>
        <p style="color: #B8A88A; font-size: 1.2rem; max-width: 500px; margin: 20px auto; line-height: 1.8;">
            靜下心來，專注於你心中的問題。<br>
            從左側選擇牌陣，然後點擊「開始抽牌」。<br>
            塔羅牌將為你揭示宇宙的指引。
        </p>
        <div style="margin-top: 30px; color: #666; font-size: 0.9rem;">
            ✦ 支援 6 種牌陣 ✦ 78 張完整塔羅牌 ✦ 正逆位解讀 ✦
        </div>
    </div>
    """, unsafe_allow_html=True)
