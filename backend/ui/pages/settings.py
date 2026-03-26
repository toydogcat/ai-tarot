import streamlit as st
from core.config_manager import config_manager

def render_settings_page():
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
        guide_name = st.text_input("導師名稱 (Guide Name)", value=conf.app.get('guide_name', 'toby'))
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

        st.markdown("### 🎋 諸葛神算提示詞設定 (Zhuge Prompts)")
        zhuge_system = st.text_area("系統提示詞 (System Prompt)", value=conf.prompts.get('zhuge_system', ''), height=100, key='zg_sys')
        zhuge_requirements = st.text_area("解讀要求 (Requirements)", value=conf.prompts.get('zhuge_requirements', ''), height=200, key='zg_req')

        st.markdown("### 🎲 小六壬提示詞設定 (Xiao Liu Ren Prompts)")
        xiaoliuren_system = st.text_area("系統提示詞 (System Prompt)", value=conf.prompts.get('xiaoliuren_system', ''), height=100, key='xlr_sys')
        xiaoliuren_requirements = st.text_area("解讀要求 (Requirements)", value=conf.prompts.get('xiaoliuren_requirements', ''), height=200, key='xlr_req')

        st.markdown("### 🌌 大六壬提示詞設定 (Da Liu Ren Prompts)")
        daliuren_system = st.text_area("系統提示詞 (System Prompt)", value=conf.prompts.get('daliuren_system', ''), height=100, key='dlr_sys')
        daliuren_requirements = st.text_area("解讀要求 (Requirements)", value=conf.prompts.get('daliuren_requirements', ''), height=200, key='dlr_req')

        st.markdown("### 🔍 搜尋摘要提示詞設定 (Search Summarizer Prompts)")
        search_summarizer = st.text_area("搜尋摘要提示詞 (Summarizer Prompt)", value=conf.prompts.search_summarizer, height=150)
        
        submit = st.form_submit_button("💾 儲存設定 (Save Configuration)")
        
        if submit:
            conf.app.guide_name = guide_name
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
            
            conf.prompts.zhuge_system = zhuge_system
            conf.prompts.zhuge_requirements = zhuge_requirements
            
            conf.prompts.xiaoliuren_system = xiaoliuren_system
            conf.prompts.xiaoliuren_requirements = xiaoliuren_requirements

            conf.prompts.daliuren_system = daliuren_system
            conf.prompts.daliuren_requirements = daliuren_requirements
            
            conf.prompts.search_summarizer = search_summarizer
            
            config_manager.save()
            st.success(f"✅ 設定檔 `{selected_profile}` 已成功儲存！")
            
    st.markdown("---")
    st.markdown("### 🔄 還原出廠設定")
    if st.button("還原為預設值 (Factory Reset)", type="secondary"):
        config_manager.reset_to_default()
        st.success(f"已成功將 `{selected_profile}` 還原為出廠預設值！")
        st.rerun()
