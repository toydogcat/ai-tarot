import streamlit as st
import time

def render_xiaoliuren(result_data: dict, question: str):
    """渲染小六壬結果"""
    nums = result_data.get("numbers", [])
    small_states = result_data.get("small_six_states", [])
    big_states = result_data.get("big_nine_states", [])
    final_state = result_data.get("final_state", "")
    details = result_data.get("details", {})

    st.markdown("### 🎲 小六壬占卜結果")
    st.markdown(f"**您的問題**：{question}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**初傳**\n\n數字：{nums[0] if len(nums)>0 else ''}\n\n落宮：{small_states[0] if len(small_states)>0 else ''}")
    with col2:
        st.info(f"**中傳**\n\n數字：{nums[1] if len(nums)>1 else ''}\n\n落宮：{small_states[1] if len(small_states)>1 else ''}")
    with col3:
        st.success(f"**終傳 (定局)**\n\n數字：{nums[2] if len(nums)>2 else ''}\n\n落宮：{final_state}")

    st.markdown("---")
    st.markdown(f"#### 📜 【{final_state}】傳統卦義")
    
    st.write(f"**斷曰**：{details.get('resolution', '')}")
    st.write(f"**籤詩**：{details.get('poem', '')}")
    
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        st.write(f"**五行方位**：{details.get('attributes', '')}")
        st.write(f"**星君神明**：{details.get('deity', '')}")
    with w_col2:
        st.write(f"**關鍵字**：{details.get('keywords', '')}")
        st.write(f"**吉凶涵義**：{details.get('description', '')}")
