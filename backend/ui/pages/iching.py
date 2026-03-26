import streamlit as st
import asyncio
from datetime import datetime
from core.iching.engine import perform_divination
from core.iching.interpreter import get_ai_interpretation as get_iching_interp, build_interpretation_prompt as build_iching_prompt
from ui.iching_ui import render_hexagram
from core.logger import get_logger
from core.history import save_complete_reading
from core.tts import generate_audio
from core.audio_input import process_transcription
from streamlit_mic_recorder import mic_recorder
from ui.tarot_ui import render_ai_interpretation
from core.config_manager import config_manager

logger = get_logger("page_iching")

def render_iching_page(iching_draw_button):
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

    if iching_draw_button:
        if not user_question.strip():
            st.warning("請先輸入你想卜問的問題 🙏")
        else:
            logger.info(f"使用者提問(易經)：{user_question.strip()}")

            result = perform_divination()
            st.session_state["last_iching_result"] = result
            st.session_state["last_iching_question"] = user_question.strip()

            # 使用統一的紀錄生命週期管理器
            from core.search import perform_tavily_search
            
            record_id, interpretation = asyncio.run(save_complete_reading(
                record_type="iching",
                question=user_question.strip(),
                result=result,
                get_interpretation_func=get_iching_interp,
                build_prompt_func=build_iching_prompt,
                search_func=perform_tavily_search,
                generate_audio_func=generate_audio,
                client_id=config_manager.get().app.get("guide_name", "toby")
            ))
            
            st.session_state["last_iching_interpretation"] = interpretation
            st.session_state["last_iching_record_id"] = record_id
            
            if interpretation and not interpretation.startswith(("⚠️", "error")):
                st.session_state["last_iching_audio_path"] = f"history/audio/{datetime.now().strftime('%Y-%m-%d')}/{record_id}.mp3"
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
