import streamlit as st
import asyncio
from datetime import datetime
from core.xiaoliuren.engine import XiaoliurenEngine
from core.xiaoliuren.interpreter import interpret_xiaoliuren
from core.history import save_complete_reading_sync
from core.tts import generate_audio
from core.audio_input import process_transcription
from streamlit_mic_recorder import mic_recorder
from ui.tarot_ui import render_ai_interpretation
from core.config_manager import config_manager
from ui.xiaoliuren_ui import render_xiaoliuren

def render_xlr_page(xlr_draw_button):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("🗣️ **語音輸入問題**")
        audio_record = mic_recorder(
            start_prompt="點擊開始錄音 🎤", stop_prompt="停止並辨識 ⏹️", key='xlr_recorder'
        )
        if audio_record:
            audio_bytes = audio_record['bytes']
            audio_hash = hash(audio_bytes)
            if st.session_state.get("last_xlr_audio_hash") != audio_hash:
                result = process_transcription(audio_bytes, format_hint="webm")
                if result and not result.startswith(("⚠️", "❌")):
                    st.session_state["xlr_user_question_input"] = result
                    st.success("✅ 辨識成功！")
                st.session_state["last_xlr_audio_hash"] = audio_hash

    user_question = st.text_area(
        "🎲 請輸入你想測算的問題：", placeholder="例如：尋物 / 謀事結果如何？", height=80, key="xlr_user_question_input"
    )

    if xlr_draw_button:
        if not user_question.strip():
            st.warning("請先輸入祈問的問題 🙏")
        else:
            with st.spinner("🎲 正在推演小六壬..."):
                engine_xlr = XiaoliurenEngine()
                res = engine_xlr.draw_lesson(None, None, None)
                if res:
                    st.session_state["last_xlr_result"] = res
                    st.session_state["last_xlr_question"] = user_question.strip()
                    
                # 使用統一的紀錄生命週期管理器
                record_id, interp = asyncio.run(save_complete_reading(
                    record_type="xiaoliuren",
                    question=user_question.strip(),
                    result=res,
                    get_interpretation_func=interpret_xiaoliuren,
                    build_prompt_func=None,
                    search_func=None,
                    generate_audio_func=generate_audio,
                    client_id=config_manager.get().app.get("guide_name", "toby")
                ))
                
                st.session_state["last_xlr_interpretation"] = interp
                st.session_state["last_xlr_record_id"] = record_id
                
                if interp and not interp.startswith(("⚠️", "error")):
                    st.session_state["last_xlr_audio"] = f"history/audio/{datetime.now().strftime('%Y-%m-%d')}/{record_id}.mp3"
                else:
                    st.session_state["last_xlr_audio"] = None

    if "last_xlr_result" in st.session_state:
        res = st.session_state["last_xlr_result"]
        ques = st.session_state.get("last_xlr_question", "")
        st.markdown("---")
        render_xiaoliuren(res, ques)
        
        interp = st.session_state.get("last_xlr_interpretation")
        if interp:
            if st.session_state.get("last_xlr_audio"):
                st.audio(st.session_state["last_xlr_audio"])
            render_ai_interpretation(interp, title="🎲 AI 小六壬解讀")
    else:
        st.markdown("<div style='text-align: center; padding: 60px;'><h1>🎲 小六壬</h1></div>", unsafe_allow_html=True)
