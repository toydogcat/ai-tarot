import streamlit as st
from sqlalchemy import update, select
from core.db import mentors, FactorySessionLocal as SessionLocal

def render_approval_page():
    st.title("🛡️ 導師帳號核准 (Mentor Approval)")
    st.info("這裡顯示已通過 Email 驗證但尚未核准使用的帳號。")
    
    with SessionLocal() as db_session:
        # 查詢待核准 (verifying_done) 或 待驗證 (pending) 的使用者
        query = select(mentors).where(mentors.c.status.in_(['verifying_done', 'pending']))
        pending_users = db_session.execute(query).fetchall()
        
        if not pending_users:
            st.success("目前沒有待處理的申請。")
        else:
            for user in pending_users:
                with st.expander(f"👤 {user.mentor_id} ({user.email}) - 狀態: {user.status}"):
                    st.write(f"註冊時間: {user.created_at}")
                    col1, col2 = st.columns(2)
                    if col1.button(f"✅ 核准 {user.mentor_id}", key=f"appr_{user.mentor_id}"):
                        db_session.execute(update(mentors).where(mentors.c.mentor_id == user.mentor_id).values(status='active'))
                        db_session.commit()
                        st.success(f"已核准 {user.mentor_id}！其密碼為: `{user.password}` (請轉告用戶)")
                        st.rerun()
                    if col2.button(f"❌ 拒絕 {user.mentor_id}", key=f"rej_{user.mentor_id}"):
                        db_session.execute(update(mentors).where(mentors.c.mentor_id == user.mentor_id).values(status='rejected'))
                        db_session.commit()
                        st.warning(f"已拒絕 {user.mentor_id}")
                        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 註冊紀錄日誌 (signups.json)")
    try:
        import json
        import os
        if os.path.exists("data/signups.json"):
            with open("data/signups.json", 'r', encoding='utf-8') as f:
                logs = json.load(f)
            st.table(logs)
        else:
            st.write("尚無 JSON 紀錄。")
    except Exception as e:
        st.error(f"讀取紀錄失敗: {e}")
