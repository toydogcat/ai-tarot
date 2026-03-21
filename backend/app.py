"""🔮 AI 塔羅占卜 — Streamlit 主程式"""
import streamlit as st
from dotenv import load_dotenv

from datetime import datetime

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT
from core.tarot.engine import DrawEngine
from core.tarot.interpreter import get_ai_interpretation, build_interpretation_prompt
from core.tarot.spreads import ALL_SPREADS, get_spread_by_id
from core.logger import get_logger
from core.history import save_reading, update_record_interpretation, search_history_records
from core.tts import generate_audio
from core.audio_input import process_transcription
from core.iching.engine import perform_divination
from core.iching.interpreter import get_ai_interpretation as get_iching_interp, build_interpretation_prompt as build_iching_prompt
from core.iching.interpreter import get_ai_interpretation as get_iching_interp, build_interpretation_prompt as build_iching_prompt
from ui.iching_ui import render_hexagram
from streamlit_mic_recorder import mic_recorder
from ui.tarot_ui import inject_custom_css, render_spread_result, render_ai_interpretation
from core.config_manager import config_manager

from core.zhuge.engine import ZhugeEngine
from core.zhuge.interpreter import interpret_zhuge
from core.daliuren.engine import DaliurenEngine
from core.daliuren.interpreter import interpret_daliuren


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
    st.markdown("---")

    # 頁面切換
    page = st.radio(
        "📄 頁面",
        ["🔮 塔羅占卜", "☯️ 易經卜卦", "🎋 諸葛神算", "🌌 大六壬", "📜 歷史紀錄", "⚙️ 設定管理"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    if page == "🔮 塔羅占卜":
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
        
    elif page == "🎋 諸葛神算":
        st.markdown("### 🎋 抽籤方式")
        st.info("系統將為您隨機抽取三八四籤之一，並由 AI 進行解籤。")
        st.markdown("---")
        zhuge_draw_button = st.button("🎋 開始抽籤", use_container_width=True, type="primary")

    elif page == "🌌 大六壬":
        st.markdown("### 🌌 起課方式")
        st.info("系統將為您隨機產生大六壬課象（四課三傳），並由 AI 解讀吉凶。")
        st.markdown("---")
        dlr_draw_button = st.button("🌌 開始起課", use_container_width=True, type="primary")

    elif page == "☯️ 易經卜卦":
        st.markdown("### 🎲 卜卦方式")
        st.info("系統將為您模擬六次金錢卦擲爻，由下而上產生本卦與變卦。")
        st.markdown("---")
        
        # 圖片格式選擇
        st.markdown("### 🖼️ 圖片格式")
        prefer_format_iching = st.radio(
            label="圖片格式",
            options=["jpg", "png"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key="iching_format"
        )
        st.session_state["prefer_image_format"] = prefer_format_iching

        st.markdown("---")
        
        iching_draw_button = st.button(
            "🎲 開始卜卦",
            use_container_width=True,
            type="primary",
        )
        st.markdown(
            "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
            "✨ 面北靜心冥想你的疑問<br>祈求吉凶禍福指示 ✨"
            "</p>",
            unsafe_allow_html=True,
        )

    # === 背景音樂 ===
    conf = config_manager.get()
    bgm_id = conf.app.get("bgm_id", 1)
    bgm_path = f"assets/music/background{bgm_id}.mp3"
    import os
    if os.path.exists(bgm_path):
        st.markdown("---")
        st.markdown("<p style='text-align:center; color:#B8A88A; margin-bottom:-10px;'>🎵 背景音樂</p>", unsafe_allow_html=True)
        st.audio(bgm_path, format="audio/mp3", autoplay=True, loop=True)

# === 塔羅占卜頁面 ===
if page == "🔮 塔羅占卜":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("🗣️ **語音輸入問題**")
        audio_record = mic_recorder(
            start_prompt="點擊開始錄音 🎤",
            stop_prompt="停止並辨識 ⏹️",
            key='recorder'
        )
        
        if audio_record:
            audio_bytes = audio_record['bytes']
            audio_hash = hash(audio_bytes)
            # 防止重新渲染時重複辨識
            if st.session_state.get("last_audio_hash") != audio_hash:
                result = process_transcription(audio_bytes, format_hint="webm")
                if result and not result.startswith(("⚠️", "❌")):
                    st.session_state["user_question_input"] = result
                    st.success("✅ 辨識成功！請在下方確認或修改。")
                else:
                    st.error(result)
                st.session_state["last_audio_hash"] = audio_hash

    # 使用者提問輸入框 (若語音辨識成功，會透過 key 自動帶入)
    user_question = st.text_area(
        "🔮 請輸入你想問塔羅牌的問題，或用語音輸入直接修改：",
        placeholder="例如：我最近的感情運勢如何？/ 我該不該換工作？/ 這段關係的未來走向是什麼？",
        height=80,
        key="user_question_input",
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

            # 執行外部搜尋
            from core.search import perform_tavily_search
            search_context, search_success = "", True
            with st.spinner("🔍 正在搜尋相關新聞/資料..."):
                search_context, search_success = perform_tavily_search(user_question.strip())
                if search_context:
                    st.success("成功搜尋到相關背景資訊！")
                elif not search_success:
                    st.warning("外部搜尋失敗，仍將根據牌面進行解讀。")

            # 產生 AI 提示詞
            from core.tarot.interpreter import build_interpretation_prompt
            ai_prompt = build_interpretation_prompt(user_question.strip(), result, search_context)

            # AI 解牌
            interpretation = None
            with st.spinner("🔮 AI 正在解讀你的塔羅牌..."):
                interpretation = get_ai_interpretation(user_question.strip(), result, search_context)

            if interpretation and not interpretation.startswith("⚠️"):
                logger.info("AI 解牌成功")
            else:
                logger.error(f"AI 解牌失敗: {interpretation}")

            st.session_state["last_interpretation"] = interpretation

            # 儲存 history（含 prompt）
            record_id = save_reading(
                record_type="tarot",
                question=user_question.strip(), 
                result=result, 
                interpretation=interpretation, 
                ai_prompt=ai_prompt, 
                search_success=search_success
            )
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

# === 易經卜卦頁面 ===
elif page == "☯️ 易經卜卦":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("🗣️ **語音輸入問題**")
        audio_record = mic_recorder(
            start_prompt="點擊開始錄音 🎤",
            stop_prompt="停止並辨識 ⏹️",
            key='iching_recorder'
        )
        
        if audio_record:
            audio_bytes = audio_record['bytes']
            audio_hash = hash(audio_bytes)
            if st.session_state.get("last_iching_audio_hash") != audio_hash:
                result = process_transcription(audio_bytes, format_hint="webm")
                if result and not result.startswith(("⚠️", "❌")):
                    st.session_state["iching_user_question_input"] = result
                    st.success("✅ 辨識成功！請在下方確認或修改。")
                else:
                    st.error(result)
                st.session_state["last_iching_audio_hash"] = audio_hash

    user_question = st.text_area(
        "☯️ 請輸入你想問易經的問題，或用語音輸入直接修改：",
        placeholder="例如：這個專案未來的發展如何？/ 這次投資順利嗎？",
        height=80,
        key="iching_user_question_input",
    )

    if "iching_draw_button" in locals() and iching_draw_button:
        if not user_question.strip():
            st.warning("請先輸入你想卜問的問題 🙏")
        else:
            logger.info(f"使用者提問(易經)：{user_question.strip()}")

            result = perform_divination()
            st.session_state["last_iching_result"] = result
            st.session_state["last_iching_question"] = user_question.strip()

            from core.search import perform_tavily_search
            search_context, search_success = "", True
            with st.spinner("🔍 正在搜尋相關新聞/資料..."):
                search_context, search_success = perform_tavily_search(user_question.strip())
                if search_context:
                    st.success("成功搜尋到相關背景資訊！")
                elif not search_success:
                    st.warning("外部搜尋失敗，仍將根據卦象進行解讀。")

            ai_prompt = build_iching_prompt(user_question.strip(), result, search_context)
            
            interpretation = None
            with st.spinner("☯️ AI 正在解讀你的卦象..."):
                interpretation = get_iching_interp(user_question.strip(), result, search_context)

            if interpretation and not interpretation.startswith("⚠️"):
                logger.info("易經 AI 解卦成功")
            else:
                logger.error(f"易經 AI 解卦失敗: {interpretation}")

            st.session_state["last_iching_interpretation"] = interpretation

            record_id = save_reading(
                record_type="iching",
                question=user_question.strip(), 
                result=result, 
                interpretation=interpretation, 
                ai_prompt=ai_prompt, 
                search_success=search_success
            )
            st.session_state["last_iching_record_id"] = record_id
            
            if interpretation and not interpretation.startswith("⚠️"):
                with st.spinner("🎵 正在生成語音..."):
                    audio_path = generate_audio(interpretation, record_id)
                if audio_path:
                    update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation, audio_path)
                    st.session_state["last_iching_audio_path"] = audio_path
                else:
                    st.session_state["last_iching_audio_path"] = None

    if "last_iching_result" in st.session_state:
        res = st.session_state["last_iching_result"]
        lines_binary = [l["original"] for l in res["lines_info"]]
        moving_indices = [i for i, l in enumerate(res["lines_info"]) if l["moving"]]
        
        st.markdown("---")
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("### 本卦 (Original)")
            render_hexagram(res["original_hexagram"], lines_binary, moving_indices)
            
        with cc2:
            if res["has_moving_lines"]:
                st.markdown("### 之卦 (Changed)")
                changed_binary = [l["changed"] for l in res["lines_info"]]
                render_hexagram(res["changed_hexagram"], changed_binary)
            else:
                st.info("無動爻，只有本卦")

        if "last_iching_interpretation" in st.session_state and st.session_state["last_iching_interpretation"]:
            interpretation = st.session_state["last_iching_interpretation"]
            if interpretation == "error" or (isinstance(interpretation, str) and interpretation.startswith("⚠️")):
                st.error("AI 錯誤。紀錄保留。")
            else:
                if st.session_state.get("last_iching_audio_path"):
                    st.audio(st.session_state["last_iching_audio_path"])
                render_ai_interpretation(interpretation, title="☯️ AI 易經解讀")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 5rem; margin-bottom: 20px;">☯️</div>
            <h1 style="color: #E8D5B7; font-family: 'Noto Serif TC', serif;">
                AI 易經卜卦
            </h1>
            <p style="color: #B8A88A; font-size: 1.2rem; max-width: 500px; margin: 20px auto; line-height: 1.8;">
                金錢卦模擬，AI 詳盡六十四卦解析。
            </p>
        </div>
        """, unsafe_allow_html=True)
# === 諸葛神算頁面 ===
elif page == "🎋 諸葛神算":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("🗣️ **語音輸入問題**")
        audio_record = mic_recorder(
            start_prompt="點擊開始錄音 🎤", stop_prompt="停止並辨識 ⏹️", key='zhuge_recorder'
        )
        if audio_record:
            audio_bytes = audio_record['bytes']
            audio_hash = hash(audio_bytes)
            if st.session_state.get("last_zg_audio_hash") != audio_hash:
                result = process_transcription(audio_bytes, format_hint="webm")
                if result and not result.startswith(("⚠️", "❌")):
                    st.session_state["zg_user_question_input"] = result
                    st.success("✅ 辨識成功！")
                st.session_state["last_zg_audio_hash"] = audio_hash

    user_question = st.text_area(
        "🎋 請輸入你想問神明的問題：",
        placeholder="例如：我該換工作嗎？/ 感情發展如何？",
        height=80, key="zg_user_question_input"
    )

    if "zhuge_draw_button" in locals() and zhuge_draw_button:
        if not user_question.strip():
            st.warning("請先輸入祈問的問題 🙏")
        else:
            engine_zg = ZhugeEngine()
            result = engine_zg.draw_lot()
            if result:
                st.session_state["last_zg_result"] = result
                st.session_state["last_zg_question"] = user_question.strip()
                
                with st.spinner("🎋 正在解籤..."):
                    interp = interpret_zhuge(user_question.strip(), result)
                    st.session_state["last_zg_interpretation"] = interp
                
                record_id = save_reading("zhuge", user_question.strip(), result, interp)
                
                if interp and not interp.startswith("⚠️"):
                    audio_path = generate_audio(interp, record_id)
                    update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interp, audio_path)
                    st.session_state["last_zg_audio"] = audio_path

    if "last_zg_result" in st.session_state:
        res = st.session_state["last_zg_result"]
        st.markdown("---")
        from ui.zhuge_ui import render_zhuge
        render_zhuge(res)
        
        interp = st.session_state.get("last_zg_interpretation")
        if interp:
            if st.session_state.get("last_zg_audio"):
                st.audio(st.session_state["last_zg_audio"])
            render_ai_interpretation(interp, title="🎋 AI 諸葛神算解讀")
    else:
        st.markdown("<div style='text-align: center; padding: 60px;'><h1>🎋 諸葛神算</h1></div>", unsafe_allow_html=True)

# === 大六壬頁面 ===
elif page == "🌌 大六壬":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("🗣️ **語音輸入問題**")
        audio_record = mic_recorder(
            start_prompt="點擊開始錄音 🎤", stop_prompt="停止並辨識 ⏹️", key='dlr_recorder'
        )
        if audio_record:
            audio_bytes = audio_record['bytes']
            audio_hash = hash(audio_bytes)
            if st.session_state.get("last_dlr_audio_hash") != audio_hash:
                result = process_transcription(audio_bytes, format_hint="webm")
                if result and not result.startswith(("⚠️", "❌")):
                    st.session_state["dlr_user_question_input"] = result
                    st.success("✅ 辨識成功！")
                st.session_state["last_dlr_audio_hash"] = audio_hash

    user_question = st.text_area(
        "🌌 請輸入你想測算的問題：", placeholder="例如：尋物 / 謀事結果如何？", height=80, key="dlr_user_question_input"
    )

    if "dlr_draw_button" in locals() and dlr_draw_button:
        if not user_question.strip():
            st.warning("請先輸入祈問的問題 🙏")
        else:
            with st.spinner("🌌 正在起課與推演天機..."):
                engine_dlr = DaliurenEngine()
                result = engine_dlr.draw_lesson()
                st.session_state["last_dlr_result"] = result
                st.session_state["last_dlr_question"] = user_question.strip()
                
                interp = interpret_daliuren(user_question.strip(), result)
                st.session_state["last_dlr_interpretation"] = interp
                
                record_id = save_reading("daliuren", user_question.strip(), result, interp)
                if interp and not interp.startswith("⚠️"):
                    audio_path = generate_audio(interp, record_id)
                    update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interp, audio_path)
                    st.session_state["last_dlr_audio"] = audio_path

    if "last_dlr_result" in st.session_state:
        res = st.session_state["last_dlr_result"]
        st.markdown("---")
        st.markdown(f"### 取得大六壬神課：")
        from ui.daliuren_ui import render_daliuren
        render_daliuren(res)
        
        interp = st.session_state.get("last_dlr_interpretation")
        if interp:
            if st.session_state.get("last_dlr_audio"):
                st.audio(st.session_state["last_dlr_audio"])
            render_ai_interpretation(interp, title="🌌 AI 大六壬解讀")
    else:
        st.markdown("<div style='text-align: center; padding: 60px;'><h1>🌌 大六壬神課</h1></div>", unsafe_allow_html=True)

elif page == "📜 歷史紀錄":
    from core.history import get_history_dates, load_history

    st.markdown("# 📜 占卜歷史紀錄")
    st.markdown("---")

    def render_history_record(record, show_date=False):
        ai_status = record.get("ai_status", {})
        if isinstance(ai_status, str):
            ai_status = {"interpretation": ai_status, "audio": "error"}
            
        text_status = ai_status.get("interpretation", "error")
        audio_status = ai_status.get("audio", "error")
        search_status = ai_status.get("search", "skipped")
        
        if text_status == "error":
            status_icon = "❌"
        elif audio_status == "error":
            status_icon = "⚠️"
        else:
            status_icon = "✅"

        date_str = f"[{record.get('_date', '')} " if show_date and "_date" in record else "["
        title_time = f"{date_str}{record['time_display']}] "
        score_str = f" (相似度: {record.get('_search_score', 0)}%)" if "_search_score" in record else ""
        
        title = f"{status_icon} {title_time}{record['question'][:40]}..." if len(record['question']) > 40 else f"{status_icon} {title_time}{record['question']}"
        title += score_str
        
        with st.expander(title):
            st.markdown(f"**問題：** {record['question']}")
            
            record_type = record.get("type", "tarot")
            if record_type == "tarot":
                spread = record.get('spread', {})
                st.markdown(f"**占卜類型：** 🔮 塔羅牌 ({spread.get('name', '')} {spread.get('card_count', '')}張)")
            else:
                st.markdown("**占卜類型：** ☯️ 易經")
                
            st.markdown(f"**ID：** `{record['id']}`")
            st.markdown(f"**AI 狀態：** {status_icon} (解讀: {text_status}, 語音: {audio_status}, 搜尋: {search_status})")

            st.markdown("---")
            if record_type == "tarot":
                st.markdown("**🃏 牌面：**")
                for card in record.get("cards", []):
                    orient_color = "🟢" if card.get("orientation") == "正位" else "🔴"
                    st.markdown(
                        f"- {orient_color} **{card.get('position')}**：{card.get('card_name_zh')}（{card.get('orientation')}）"
                        f" — {', '.join(card.get('keywords', [])[:3])}"
                    )
            elif record_type == "iching":
                res = record.get("result", {})
                st.markdown("**☯️ 卦象：**")
                st.markdown(f"- **本卦：** {res.get('original_hexagram')}")
                if res.get('has_moving_lines'):
                    st.markdown(f"- **之卦：** {res.get('changed_hexagram')}")
                    moving = [i+1 for i, v in enumerate(res.get('lines_info', [])) if v.get('moving')]
                    st.markdown(f"- **動爻：** 第 {', '.join(map(str, moving))} 爻")
            elif record_type == "zhuge":
                res = record.get("result", {})
                st.markdown("**🎋 籤詩：**")
                st.markdown(f"- **第 {res.get('id')} 籤**")
                st.markdown(f"- {res.get('poem')}")
            elif record_type == "daliuren":
                res = record.get("result", {})
                st.markdown("**🌌 課象：**")
                st.markdown(f"- **日期：** {res.get('date')} ({res.get('jieqi')})")
                st.markdown(f"- **格局：** {', '.join(res.get('pattern', []))}")

            st.markdown("---")
            if text_status == "error":
                st.error("AI 解牌失敗。可使用 Gemini CLI 技能修復此紀錄。")
                st.code(f"修復指令參考：\n日期: {record.get('_date', 'YYYY-MM-DD')}\nID: {record['id']}", language="text")
            else:
                if record.get("recovered_at"):
                    st.success(f"已於 {record['recovered_at']} 修復")
                if record.get("ai_interpretation_audio_path"):
                    import os
                    audio_file = record.get("ai_interpretation_audio_path")
                    if os.path.exists(audio_file):
                        st.audio(audio_file)
                    else:
                        st.warning("⚠️ 語音檔案遺失。")
                else:
                    st.warning("⚠️ 此紀錄缺少語音解讀。可使用補件功能修復。")
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

# === 設定管理頁面 ===
elif page == "⚙️ 設定管理":
    st.markdown("# ⚙️ 設定管理 (Configuration)")
    st.markdown("---")
    
    # 選擇目前使用的設定檔
    st.markdown("### 👤 選擇設定檔 (Profile)")
    st.caption("📝 **提示**：目前 `customer1` 為 Streamlit 後台管理的預設設定，而 `customer2` 為一般前端 (Vite/FastAPI) 預設使用的設定。")
    profiles = ["customer1", "customer2"]
    current_index = profiles.index(config_manager.active_profile) if config_manager.active_profile in profiles else 0
    
    selected_profile = st.selectbox("載入設定檔", profiles, index=current_index)
    
    # 若有切換，則更新設定管理器的設定並重新載入畫面
    if selected_profile != config_manager.active_profile:
        config_manager.set_active_profile(selected_profile)
        st.rerun()
        
    st.markdown("---")
    
    conf = config_manager.get()
    
    with st.form("config_form"):
        st.markdown("### 🖥️ 應用程式設定 (App config)")
        app_port = st.number_input("伺服器通訊埠 (Port)", value=int(conf.app.port), step=1)
        api_port = st.number_input("API 伺服器通訊埠 (API Port)", value=int(conf.app.get('api_port', 8000)), step=1)
        st.caption("提示：修改 Port 需要在啟動時套用 (或於 .streamlit/config.toml 設定)，這裡僅供狀態記錄與檢視。")

        bgm_options = {"BGM 1": 1, "BGM 2": 2}
        bgm_labels = list(bgm_options.keys())
        bgm_values = list(bgm_options.values())
        current_bgm = conf.app.get('bgm_id', 1)
        bgm_index = bgm_values.index(current_bgm) if current_bgm in bgm_values else 0
        bgm_label_selected = st.selectbox("背景音樂 (Background Music)", bgm_labels, index=bgm_index)
        app_bgm_id = bgm_options[bgm_label_selected]

        st.markdown("### 🤖 AI 模型設定 (AI Models)")
        divination_model = st.text_input("主解讀模型 (Divination Model)", value=conf.ai_models.divination_model)
        summarization_model = st.text_input("時事摘要模型 (Summarizer)", value=conf.ai_models.summarization_model)
        tts_voice = st.text_input("語音合成口音 (TTS Voice)", value=conf.ai_models.tts_voice)
        
        st.markdown("### 🔮 塔羅牌提示詞設定 (Tarot Prompts)")
        tarot_system = st.text_area("系統提示詞 (System Prompt)", value=conf.prompts.tarot_system, height=100)
        tarot_requirements = st.text_area("解讀要求 (Requirements)", value=conf.prompts.tarot_requirements, height=200)

        st.markdown("### ☯️ 易經提示詞設定 (I-Ching Prompts)")
        iching_system = st.text_area("系統提示詞 (System Prompt)", value=conf.prompts.iching_system, height=100)
        iching_requirements = st.text_area("解讀要求 (Requirements)", value=conf.prompts.iching_requirements, height=200)

        st.markdown("### 🔍 搜尋摘要提示詞設定 (Search Summarizer Prompts)")
        search_summarizer = st.text_area("搜尋摘要提示詞 (Summarizer Prompt)", value=conf.prompts.search_summarizer, height=150)
        
        submit = st.form_submit_button("💾 儲存設定 (Save Configuration)")
        
        if submit:
            conf.app.port = app_port
            conf.app.api_port = api_port
            conf.app.bgm_id = app_bgm_id
            
            conf.ai_models.divination_model = divination_model
            conf.ai_models.summarization_model = summarization_model
            conf.ai_models.tts_voice = tts_voice
            
            conf.prompts.tarot_system = tarot_system
            conf.prompts.tarot_requirements = tarot_requirements
            
            conf.prompts.iching_system = iching_system
            conf.prompts.iching_requirements = iching_requirements
            
            conf.prompts.search_summarizer = search_summarizer
            
            config_manager.save()
            st.success(f"✅ 設定檔 `{selected_profile}` 已成功儲存！")
            
    st.markdown("---")
    st.markdown("### 🔄 還原出廠設定")
    if st.button("還原為預設值 (Factory Reset)", type="secondary"):
        config_manager.reset_to_default()
        st.success(f"已成功將 `{selected_profile}` 還原為出廠預設值！")
        st.rerun()
