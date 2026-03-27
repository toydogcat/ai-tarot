import streamlit as st
import time
from datetime import datetime
from core.history import get_history_dates, load_history, search_history_records, delete_record, delete_records_batch

def render_history_page():
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
                st.markdown(f"**占卜類型：** {record_type.capitalize()}")
                
            st.markdown(f"**求問者：** `{record.get('client_name', 'toby')}`")
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
            elif record_type == "xiaoliuren":
                res = record.get("result", {})
                st.markdown("**🎲 課象：**")
                st.markdown(f"- **初傳：** {res.get('chuchuan')} ({res.get('chuchuan_desc')})")
                st.markdown(f"- **中傳：** {res.get('zhongchuan')} ({res.get('zhongchuan_desc')})")
                st.markdown(f"- **終傳：** {res.get('zhongchuan2')} ({res.get('zhongchuan2_desc')})")
            elif record_type == "daliuren":
                res = record.get("result", {})
                st.markdown("**🌌 課象：**")
                st.markdown(f"- **格局：** {', '.join(res.get('pattern', []))}")

            st.markdown("---")
            if text_status == "error":
                st.error("AI 解牌失敗。可使用 Gemini CLI 技能修復此紀錄。")
                st.code(f"修復指令參考：\n日期: {record.get('_date', 'YYYY-MM-DD')}\nID: {record['id']}", language="text")
            else:
                if record.get("recovered_at"):
                    st.success(f"已於 {record['recovered_at']} 修復")
                if record.get("audio_path"):
                    import os
                    audio_file = record.get("audio_path")
                    # 如果是相對路徑，嘗試從 BASE_DIR 找
                    if not os.path.exists(audio_file):
                        from config import BASE_DIR
                        full_path = os.path.join(BASE_DIR, audio_file)
                        if os.path.exists(full_path):
                            audio_file = full_path
                    
                    if os.path.exists(audio_file):
                        st.audio(audio_file)
                    else:
                        st.warning("⚠️ 語音檔案遺失。")
                st.markdown(f"**AI 解讀：**\n\n{record['ai_interpretation']}")

            st.markdown("---")
            if st.button("🗑️ 刪除", key=f"del_{record['id']}"):
                r_date = record.get("_date")
                if r_date and delete_record(r_date, record['id']):
                    st.toast("✅ 紀錄已成功刪除！")
                    time.sleep(0.5)
                    st.rerun()

    search_query = st.text_input("🔍 搜尋歷史解讀（輸入關鍵字）", "")
    
    dates = get_history_dates()
    if not dates:
        st.info("目前尚無任何占卜紀錄。去占卜一次吧！🔮")
        st.stop()

    selected_date = st.selectbox("📅 選擇日期", dates)
    records_for_date = load_history(selected_date)
    all_clients = set(r.get("client_name", "toby") for r in records_for_date)
    all_mentors = set(r.get("mentor_id", "toby") for r in records_for_date)
            
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        mentor_filter = st.selectbox("🧙‍♂️ 導師篩選", ["顯示全部"] + sorted(list(all_mentors)))
    with col_filter2:
        client_filter = st.selectbox("👤 客戶篩選", ["顯示全部"] + sorted(list(all_clients)))
    
    st.markdown("---")
    
    if search_query:
        records = search_history_records(search_query)
        if mentor_filter != "顯示全部":
            records = [r for r in records if r.get("mentor_id", "toby") == mentor_filter]
        if client_filter != "顯示全部":
            records = [r for r in records if r.get("client_name", "toby") == client_filter]
            
        if not records:
            st.info("找不到符合的紀錄。")
        else:
            st.markdown(f"找到 **{len(records)}** 筆相關紀錄，依關聯度排序：")
            if st.button(f"🗑️ 刪除目前顯示的 {len(records)} 筆紀錄", type="primary", key="batch_del_search"):
                deleted_count = delete_records_batch(records)
                st.toast(f"✅ 成功刪除 {deleted_count} 筆紀錄！")
                time.sleep(0.5)
                st.rerun()

            for record in records:
                render_history_record(record, show_date=True)
    else:
        records = records_for_date
        for r in records: r["_date"] = selected_date
        
        if mentor_filter != "顯示全部":
            records = [r for r in records if r.get("mentor_id", "toby") == mentor_filter]
        if client_filter != "顯示全部":
            records = [r for r in records if r.get("client_name", "toby") == client_filter]

        if not records:
            st.info(f"{selected_date} 沒有符合篩選的紀錄。")
        else:
            st.markdown(f"共 **{len(records)}** 筆紀錄")
            if st.button(f"🗑️ 刪除目前顯示的 {len(records)} 筆紀錄", type="primary", key=f"batch_del_date"):
                deleted_count = delete_records_batch(records)
                st.toast(f"✅ 成功刪除 {deleted_count} 筆紀錄！")
                time.sleep(0.5)
                st.rerun()
                
            for record in reversed(records):
                render_history_record(record)
