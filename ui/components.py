"""UI 元件 — 牌面展示、牌陣佈局"""
import streamlit as st
from pathlib import Path
from PIL import Image

from config import ASSETS_DIR, CARD_BACK_IMAGE
from core.models import DrawnCard, SpreadResult


def inject_custom_css():
    """注入自定義 CSS 樣式"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;700&display=swap');

    .stApp {
        font-family: 'Noto Serif TC', serif;
    }

    .card-container {
        text-align: center;
        padding: 10px;
        transition: transform 0.3s ease;
    }
    .card-container:hover {
        transform: scale(1.05);
    }

    .card-name {
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 8px;
        color: #E8D5B7;
    }

    .card-orientation {
        font-size: 0.85rem;
        padding: 2px 12px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
    }
    .upright {
        background: linear-gradient(135deg, #4a6741, #6b8f5e);
        color: white;
    }
    .reversed {
        background: linear-gradient(135deg, #8b4557, #a85a6e);
        color: white;
    }

    .position-label {
        font-size: 0.9rem;
        color: #B8A88A;
        font-style: italic;
        margin-bottom: 4px;
    }

    .meaning-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(232,213,183,0.2);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }

    .keyword-tag {
        display: inline-block;
        background: rgba(232,213,183,0.15);
        border: 1px solid rgba(232,213,183,0.3);
        border-radius: 16px;
        padding: 3px 12px;
        margin: 3px;
        font-size: 0.8rem;
        color: #E8D5B7;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem;
    }

    .spread-title {
        text-align: center;
        font-size: 1.8rem;
        color: #E8D5B7;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)


def load_card_image(
    image_path: str, is_reversed: bool = False, prefer_format: str = "jpg"
) -> Image.Image | None:
    """
    載入牌面圖片，支援 JPG/PNG 優先順序
    
    Args:
        image_path: 相對圖片路徑（如 major/00_the_fool.png）
        is_reversed: 是否逆位（旋轉 180°）
        prefer_format: 優先格式 'jpg' 或 'png'
    """
    base_path = ASSETS_DIR / image_path
    stem = base_path.stem
    parent = base_path.parent
    
    # 依照偏好格式建立搜尋順序
    if prefer_format == "jpg":
        candidates = [
            parent / f"{stem}.jpg",
            parent / f"{stem}.jpeg",
            parent / f"{stem}.png",
        ]
    else:
        candidates = [
            parent / f"{stem}.png",
            parent / f"{stem}.jpg",
            parent / f"{stem}.jpeg",
        ]
    
    for candidate in candidates:
        if candidate.exists():
            img = Image.open(candidate)
            if is_reversed:
                img = img.rotate(180)
            return img
    
    return None


def render_card(drawn_card: DrawnCard, position_name: str = "", show_meaning: bool = True):
    """渲染單張牌"""
    card = drawn_card.card
    orientation = "逆位 ↓" if drawn_card.is_reversed else "正位 ↑"
    css_class = "reversed" if drawn_card.is_reversed else "upright"

    # 位置標籤
    if position_name:
        st.markdown(f'<div class="position-label">【{position_name}】</div>', unsafe_allow_html=True)

    # 嘗試載入圖片（使用 session state 中的格式偏好）
    prefer_format = st.session_state.get("prefer_image_format", "jpg")
    img = load_card_image(card.image, drawn_card.is_reversed, prefer_format)
    if img:
        st.image(img, width="stretch")
    else:
        # 無圖片時顯示文字佔位
        bg_color = "#8b4557" if drawn_card.is_reversed else "#4a6741"
        st.markdown(f"""
        <div style="
            background: {bg_color};
            border: 2px solid #E8D5B7;
            border-radius: 8px;
            padding: 30px 10px;
            text-align: center;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        ">
            <div style="font-size: 2rem;">🔮</div>
            <div style="font-size: 1.1rem; color: #E8D5B7; font-weight: bold; margin-top: 8px;">
                {card.name_zh}
            </div>
            <div style="font-size: 0.8rem; color: #B8A88A; margin-top: 4px;">
                {card.name}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 牌名與正逆位
    st.markdown(f'<div class="card-name">{card.name_zh}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card-orientation {css_class}">{orientation}</div>', unsafe_allow_html=True)

    # 牌意
    if show_meaning:
        meaning = drawn_card.current_meaning
        keywords_html = "".join(f'<span class="keyword-tag">{kw}</span>' for kw in meaning.keywords)
        st.markdown(f"""
        <div class="meaning-box">
            <div style="margin-bottom: 8px;">{keywords_html}</div>
            <div style="font-size: 0.9rem; color: #ccc; line-height: 1.6;">
                {meaning.meaning}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_spread_result(result: SpreadResult):
    """根據牌陣類型渲染結果"""
    spread = result.spread
    drawn = result.drawn_cards

    st.markdown(f'<div class="spread-title">{spread.icon} {spread.name}</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#B8A88A;'>{spread.description}</p>", unsafe_allow_html=True)
    st.divider()

    if spread.id == "single":
        # 單牌：置中顯示
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            render_card(drawn[0], spread.positions[0].name)

    elif spread.id == "three_card":
        # 三牌：三欄
        cols = st.columns(3)
        for i, col in enumerate(cols):
            with col:
                render_card(drawn[i], spread.positions[i].name)

    elif spread.id == "time_flow":
        # 時間之流：五欄
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                render_card(drawn[i], spread.positions[i].name)

    elif spread.id == "two_options":
        # 二擇一：現況居中，兩個選項分左右
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            render_card(drawn[0], spread.positions[0].name)

        st.divider()
        st.markdown("<h3 style='text-align:center; color:#E8D5B7;'>⬅️ 選項 A　vs　選項 B ➡️</h3>", unsafe_allow_html=True)

        col_a1, col_a2, spacer, col_b1, col_b2 = st.columns([1, 1, 0.3, 1, 1])
        with col_a1:
            render_card(drawn[1], spread.positions[1].name)
        with col_a2:
            render_card(drawn[2], spread.positions[2].name)
        with col_b1:
            render_card(drawn[3], spread.positions[3].name)
        with col_b2:
            render_card(drawn[4], spread.positions[4].name)

    elif spread.id == "horseshoe":
        # 馬蹄形：弧形排列（用兩行模擬）
        cols_top = st.columns(7)
        for i, col in enumerate(cols_top):
            with col:
                render_card(drawn[i], spread.positions[i].name)

    elif spread.id == "celtic_cross":
        # 凱爾特十字：經典佈局
        # 第一行：潛意識(2) | 現況(0)+挑戰(1) | 頂部(4)
        st.markdown("### 🔮 核心牌組", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_card(drawn[3], spread.positions[3].name)  # 過去
        with c2:
            render_card(drawn[0], spread.positions[0].name)  # 現況
            render_card(drawn[1], spread.positions[1].name, show_meaning=False)  # 挑戰（橫跨）
        with c3:
            render_card(drawn[5], spread.positions[5].name)  # 近期未來
        with c4:
            render_card(drawn[2], spread.positions[2].name)  # 潛意識

        st.markdown("### 📊 指引之柱", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#B8A88A;'>最佳結果：見下方第一張</p>", unsafe_allow_html=True)
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            render_card(drawn[4], spread.positions[4].name)  # 頂部
        with c6:
            render_card(drawn[6], spread.positions[6].name)  # 你的態度
        with c7:
            render_card(drawn[7], spread.positions[7].name)  # 外在環境
        with c8:
            render_card(drawn[8], spread.positions[8].name)  # 希望與恐懼

        st.divider()
        st.markdown("### 🎯 最終結果", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns([1, 1, 1])
        with rc2:
            render_card(drawn[9], spread.positions[9].name)


def render_ai_interpretation(interpretation: str):
    """渲染 AI 解牌結果"""
    st.divider()
    st.markdown(
        '<div class="spread-title">🤖 AI 塔羅解讀</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(232,213,183,0.15);
            border-radius: 16px;
            padding: 24px 28px;
            margin: 16px auto;
            max-width: 800px;
            color: #ccc;
            line-height: 2;
            font-size: 1rem;
            white-space: pre-wrap;
        ">{interpretation}</div>
        """,
        unsafe_allow_html=True,
    )
