import streamlit as st
import asyncio
from datetime import datetime
from core.tarot.interpreter import get_ai_interpretation, build_interpretation_prompt
from core.logger import get_logger
from core.history import save_complete_reading
from core.tts import generate_audio
from core.audio_input import process_transcription
from streamlit_mic_recorder import mic_recorder
from ui.tarot_ui import render_spread_result, render_ai_interpretation
from core.config_manager import config_manager

logger = get_logger("page_tarot")

def render_tarot_page(engine, selected_spread, draw_button, allow_reversed):
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

    # 使用者提問輸入框
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

            # 使用統一的紀錄生命週期管理器
            from core.search import perform_tavily_search
            
            record_id, interpretation = asyncio.run(save_complete_reading(
                record_type="tarot",
                question=user_question.strip(),
                result=result,
                get_interpretation_func=get_ai_interpretation,
                build_prompt_func=build_interpretation_prompt,
                search_func=perform_tavily_search,
                generate_audio_func=generate_audio,
                client_id=config_manager.get().app.get("guide_name", "toby")
            ))
            
            st.session_state["last_interpretation"] = interpretation
            st.session_state["last_record_id"] = record_id
            
            if interpretation and not interpretation.startswith(("⚠️", "error")):
                st.session_state["last_audio_path"] = f"history/audio/{datetime.now().strftime('%Y-%m-%d')}/{record_id}.mp3"
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
