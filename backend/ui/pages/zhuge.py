import streamlit as st
import asyncio
from datetime import datetime
from core.zhuge.engine import ZhugeEngine
from core.zhuge.interpreter import interpret_zhuge
from core.history import save_complete_reading
from core.tts import generate_audio
from core.audio_input import process_transcription
from streamlit_mic_recorder import mic_recorder
from ui.tarot_ui import render_ai_interpretation
from core.config_manager import config_manager
from ui.zhuge_ui import render_zhuge

def render_zhuge_page(zhuge_draw_button):
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

    if zhuge_draw_button:
        if not user_question.strip():
            st.warning("請先輸入祈問的問題 🙏")
        else:
            engine_zg = ZhugeEngine()
            result = engine_zg.draw_lot()
            if result:
                st.session_state["last_zg_result"] = result
                st.session_state["last_zg_question"] = user_question.strip()
                
                # 使用統一的紀錄生命週期管理器
                record_id, interp, audio_path = asyncio.run(save_complete_reading(
                    record_type="zhuge",
                    question=user_question.strip(),
                    result=result,
                    get_interpretation_func=interpret_zhuge,
                    build_prompt_func=None,
                    search_func=None,
                    generate_audio_func=generate_audio,
                    client_id=config_manager.get().app.get("guide_name", "toby")
                ))
                
                st.session_state["last_zg_interpretation"] = interp
                st.session_state["last_zg_record_id"] = record_id
                st.session_state["last_zg_audio"] = audio_path

    if "last_zg_result" in st.session_state:
        res = st.session_state["last_zg_result"]
        st.markdown("---")
        render_zhuge(res)
        
        interp = st.session_state.get("last_zg_interpretation")
        if interp:
            if st.session_state.get("last_zg_audio"):
                st.audio(st.session_state["last_zg_audio"])
            render_ai_interpretation(interp, title="🎋 AI 諸葛神算解讀")
    else:
        st.markdown("<div style='text-align: center; padding: 60px;'><h1>🎋 諸葛神算</h1></div>", unsafe_allow_html=True)
