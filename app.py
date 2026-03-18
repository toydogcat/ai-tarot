"""🔮 AI 塔羅占卜 — Streamlit 主程式"""
import streamlit as st
from dotenv import load_dotenv

from datetime import datetime

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT
from core.engine import DrawEngine
from core.interpreter import get_ai_interpretation, build_interpretation_prompt
from core.spreads import ALL_SPREADS, get_spread_by_id
from core.logger import get_logger
from core.history import save_reading, update_record_interpretation, search_history_records
from core.tts import generate_audio
from ui.components import inject_custom_css, render_spread_result, render_ai_interpretation

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
    st.markdown("# 🔮 AI 塔羅占卜")
    st.markdown("---")

    # 頁面切換
    page = st.radio(
        "📄 頁面",
        ["🔮 占卜", "📜 歷史紀錄"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    if page == "🔮 占卜":
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

        # 圖片格式選擇
        st.markdown("### 🖼️ 圖片格式")
        prefer_format = st.radio(
            label="圖片格式",
            options=["jpg", "png"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state["prefer_image_format"] = prefer_format

        st.markdown("---")

        # 抽牌按鈕
        draw_button = st.button(
            "🃏 開始抽牌",
            width="stretch",
            type="primary",
        )

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
            "✨ 靜心冥想你的問題<br>然後點擊抽牌 ✨"
            "</p>",
            unsafe_allow_html=True,
        )

# === 占卜頁面 ===
if page == "🔮 占卜":
    # 使用者提問輸入框
    user_question = st.text_area(
        "🔮 請輸入你想問塔羅牌的問題",
        placeholder="例如：我最近的感情運勢如何？/ 我該不該換工作？/ 這段關係的未來走向是什麼？",
        height=80,
        key="user_question",
    )

    if draw_button and selected_spread:
        if not user_question.strip():
            st.warning("請先輸入你想問的問題再抽牌 🙏")
        else:
            logger.info(f"使用者提問：{user_question.strip()}")
            logger.info(f"牌陣：{selected_spread.name}")

            # 抽牌
            result = engine.draw_spread(selected_spread, allow_reversed)
            st.session_state["last_result"] = result
            st.session_state["last_question"] = user_question.strip()

            logger.info(f"抽牌完成：{[dc.display_name for dc in result.drawn_cards]}")

            # 產生 AI 提示詞
            from core.interpreter import build_interpretation_prompt
            ai_prompt = build_interpretation_prompt(user_question.strip(), result)

            # AI 解牌
            interpretation = None
            with st.spinner("🔮 AI 正在解讀你的塔羅牌..."):
                interpretation = get_ai_interpretation(user_question.strip(), result)

            if interpretation and not interpretation.startswith("⚠️"):
                logger.info("AI 解牌成功")
            else:
                logger.error(f"AI 解牌失敗: {interpretation}")

            st.session_state["last_interpretation"] = interpretation

            # 儲存 history（含 prompt）
            record_id = save_reading(user_question.strip(), result, interpretation, ai_prompt=ai_prompt)
            st.session_state["last_record_id"] = record_id
            logger.info(f"紀錄已儲存 [ID={record_id}]")

            # 產生語音
            if interpretation and not interpretation.startswith("⚠️"):
                with st.spinner("🎵 正在生成語音..."):
                    audio_path = generate_audio(interpretation, record_id)
                if audio_path:
                    update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation, audio_path)
                    st.session_state["last_audio_path"] = audio_path
                else:
                    st.session_state["last_audio_path"] = None
        
    # 顯示結果
    if "last_result" in st.session_state:
        render_spread_result(st.session_state["last_result"])

        # 顯示 AI 解讀
        if "last_interpretation" in st.session_state and st.session_state["last_interpretation"]:
            interpretation = st.session_state["last_interpretation"]
            if interpretation == "error" or (isinstance(interpretation, str) and interpretation.startswith("⚠️")):
                st.error("AI 解牌過程中發生錯誤，此次紀錄已標記為 error，可使用 Gemini CLI 技能修復。")
            else:
                if st.session_state.get("last_audio_path"):
                    st.audio(st.session_state["last_audio_path"])
                render_ai_interpretation(interpretation)
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
                在上方輸入你的提問，選擇牌陣，<br>
                然後點擊「開始抽牌」。<br>
                AI 將為你深度解讀塔羅牌的指引。
            </p>
            <div style="margin-top: 30px; color: #666; font-size: 0.9rem;">
                ✦ 支援 6 種牌陣 ✦ 78 張完整塔羅牌 ✦ Gemini AI 解讀 ✦
            </div>
        </div>
        """, unsafe_allow_html=True)

# === 歷史紀錄頁面 ===
elif page == "📜 歷史紀錄":
    from core.history import get_history_dates, load_history

    st.markdown("# 📜 占卜歷史紀錄")
    st.markdown("---")

    def render_history_record(record, show_date=False):
        ai_status = record.get("ai_status", "unknown")
        status_icon = {"success": "✅", "error": "❌", "recovered": "🔄"}.get(ai_status, "❓")
        date_str = f"[{record.get('_date', '')} " if show_date and "_date" in record else "["
        title_time = f"{date_str}{record['time_display']}] "
        score_str = f" (相似度: {record.get('_search_score', 0)}%)" if "_search_score" in record else ""
        
        title = f"{status_icon} {title_time}{record['question'][:40]}..." if len(record['question']) > 40 else f"{status_icon} {title_time}{record['question']}"
        title += score_str
        
        with st.expander(title):
            st.markdown(f"**問題：** {record['question']}")
            st.markdown(f"**牌陣：** {record['spread']['name']}（{record['spread']['card_count']} 張）")
            st.markdown(f"**ID：** `{record['id']}`")
            st.markdown(f"**AI 狀態：** {status_icon} {ai_status}")

            st.markdown("---")
            st.markdown("**🃏 牌面：**")
            for card in record["cards"]:
                orient_color = "🟢" if card["orientation"] == "正位" else "🔴"
                st.markdown(
                    f"- {orient_color} **{card['position']}**：{card['card_name_zh']}（{card['orientation']}）"
                    f" — {', '.join(card['keywords'][:3])}"
                )

            st.markdown("---")
            if record["ai_interpretation"] == "error":
                st.error("AI 解牌失敗。可使用 Gemini CLI 技能修復此紀錄。")
                st.code(f"修復指令參考：\n日期: {record.get('_date', 'YYYY-MM-DD')}\nID: {record['id']}", language="text")
            else:
                if record.get("recovered_at"):
                    st.success(f"已於 {record['recovered_at']} 修復")
                if record.get("ai_interpretation_audio_path"):
                    st.audio(record.get("ai_interpretation_audio_path"))
                st.markdown(f"**AI 解讀：**\n\n{record['ai_interpretation']}")

    search_query = st.text_input("🔍 搜尋歷史解讀（輸入關鍵字）", "")
    st.markdown("---")
    
    if search_query:
        records = search_history_records(search_query)
        if not records:
            st.info("找不到符合的紀錄。")
        else:
            st.markdown(f"找到 **{len(records)}** 筆相關紀錄，依關聯度排序：")
            for record in records:
                render_history_record(record, show_date=True)
    else:
        dates = get_history_dates()

        if not dates:
            st.info("目前尚無任何占卜紀錄。去占卜一次吧！🔮")
        else:
            selected_date = st.selectbox("選擇日期", dates)
            records = load_history(selected_date)

            if not records:
                st.info(f"{selected_date} 沒有任何紀錄。")
            else:
                st.markdown(f"共 **{len(records)}** 筆紀錄")
                for record in reversed(records):
                    record["_date"] = selected_date
                    render_history_record(record)
