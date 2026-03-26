import os

app_path = "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add new imports
new_imports = """
from core.zhuge.engine import ZhugeEngine
from core.zhuge.interpreter import interpret_zhuge
from core.daliuren.engine import DaliurenEngine
from core.daliuren.interpreter import interpret_daliuren
"""
content = content.replace("from core.config_manager import config_manager", "from core.config_manager import config_manager\nimport asyncio\n" + new_imports)

# 2. Add to side menu
content = content.replace(
    '["🔮 塔羅占卜", "☯️ 易經卜卦", "📜 歷史紀錄", "⚙️ 設定管理"]',
    '["🔮 塔羅占卜", "☯️ 易經卜卦", "🎋 諸葛神算", "🌌 大六壬", "📜 歷史紀錄", "⚙️ 設定管理"]'
)

# 3. Add sidebar UI
target_sidebar = 'elif page == "☯️ 易經卜卦":'
zhuge_dlr_sidebar = """
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
"""
if 'elif page == "🎋 諸葛神算":' not in content:
    content = content.replace(target_sidebar, zhuge_dlr_sidebar.strip(), 1)


# 4. Add pages content
target_page = 'elif page == "📜 歷史紀錄":'
zhuge_dlr_pages = """
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
                    audio_path = asyncio.run(generate_audio(interp, record_id))
                    update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interp, audio_path)
                    st.session_state["last_zg_audio"] = audio_path

    if "last_zg_result" in st.session_state:
        res = st.session_state["last_zg_result"]
        st.markdown("---")
        st.markdown(f"### 第 {res.get('id')} 籤")
        st.markdown(f"**【籤詩】** {res.get('poem')}")
        
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
            engine_dlr = DaliurenEngine()
            result = engine_dlr.draw_lesson()
            st.session_state["last_dlr_result"] = result
            st.session_state["last_dlr_question"] = user_question.strip()
            
            with st.spinner("🌌 正在推演天機..."):
                interp = interpret_daliuren(user_question.strip(), result)
                st.session_state["last_dlr_interpretation"] = interp
            
            record_id = save_reading("daliuren", user_question.strip(), result, interp)
            if interp and not interp.startswith("⚠️"):
                audio_path = asyncio.run(generate_audio(interp, record_id))
                update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interp, audio_path)
                st.session_state["last_dlr_audio"] = audio_path

    if "last_dlr_result" in st.session_state:
        res = st.session_state["last_dlr_result"]
        st.markdown("---")
        st.markdown(f"### 取得大六壬神課：")
        import json
        st.json(res)
        
        interp = st.session_state.get("last_dlr_interpretation")
        if interp:
            if st.session_state.get("last_dlr_audio"):
                st.audio(st.session_state["last_dlr_audio"])
            render_ai_interpretation(interp, title="🌌 AI 大六壬解讀")
    else:
        st.markdown("<div style='text-align: center; padding: 60px;'><h1>🌌 大六壬神課</h1></div>", unsafe_allow_html=True)

elif page == "📜 歷史紀錄":
"""
if '# === 諸葛神算頁面 ===' not in content:
    content = content.replace(target_page, zhuge_dlr_pages.strip())

# 5. Patch history rendering
history_replace_code = """
            elif record_type == "iching":
                res = record.get("result", {})
                st.markdown("**☯️ 卦象：**")
                st.markdown(f"- **本卦：** {res.get('original_hexagram')}")
                if res.get('has_moving_lines'):
                    st.markdown(f"- **之卦：** {res.get('changed_hexagram')}")
                    moving = [i+1 for i, v in enumerate(res.get('lines_info', [])) if v.get('moving')]
                    st.markdown(f"- **動爻：** 第 {', '.join(map(str, moving))} 爻")
"""

history_new_code = """
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
"""
if 'elif record_type == "zhuge":' not in content:
    content = content.replace(history_replace_code.strip('\n'), history_new_code.strip('\n'))

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)
