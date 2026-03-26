import streamlit as st
import asyncio
from datetime import datetime
from core.daliuren.engine import DaliurenEngine
from core.daliuren.interpreter import interpret_daliuren
from core.history import save_complete_reading
from core.tts import generate_audio
from core.audio_input import process_transcription
from streamlit_mic_recorder import mic_recorder
from ui.tarot_ui import render_ai_interpretation
from core.config_manager import config_manager
from ui.daliuren_ui import render_daliuren

def render_dlr_page(dlr_draw_button):
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

    if dlr_draw_button:
        if not user_question.strip():
            st.warning("請先輸入祈問的問題 🙏")
        else:
            with st.spinner("🌌 正在起課與推演天機..."):
                engine_dlr = DaliurenEngine()
                result = engine_dlr.draw_lesson()
                st.session_state["last_dlr_result"] = result
                st.session_state["last_dlr_question"] = user_question.strip()
                
                # 使用統一的紀錄生命週期管理器
                record_id, interp = asyncio.run(save_complete_reading(
                    record_type="daliuren",
                    question=user_question.strip(),
                    result=result,
                    get_interpretation_func=interpret_daliuren,
                    build_prompt_func=None,
                    search_func=None,
                    generate_audio_func=generate_audio,
                    client_id=config_manager.get().app.get("guide_name", "toby")
                ))
                
                st.session_state["last_dlr_interpretation"] = interp
                st.session_state["last_dlr_record_id"] = record_id
                
                if interp and not interp.startswith(("⚠️", "error")):
                    st.session_state["last_dlr_audio"] = f"history/audio/{datetime.now().strftime('%Y-%m-%d')}/{record_id}.mp3"
                else:
                    st.session_state["last_dlr_audio"] = None

    if "last_dlr_result" in st.session_state:
        res = st.session_state["last_dlr_result"]
        st.markdown("---")
        st.markdown(f"### 取得大六壬神課：")
        render_daliuren(res)
        
        interp = st.session_state.get("last_dlr_interpretation")
        if interp:
            if st.session_state.get("last_dlr_audio"):
                st.audio(st.session_state["last_dlr_audio"])
            render_ai_interpretation(interp, title="🌌 AI 大六壬解讀")
    else:
        st.markdown("<div style='text-align: center; padding: 60px;'><h1>🌌 大六壬神課</h1></div>", unsafe_allow_html=True)
