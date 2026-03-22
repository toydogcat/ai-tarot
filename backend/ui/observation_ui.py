import streamlit as st
import requests
import asyncio
import concurrent.futures

def fetch_status(port):
    try:
        url = f"http://127.0.0.1:{port}/api/admin/status"
        response = requests.get(url, timeout=1.5)
        if response.status_code == 200:
            data = response.json()
            data['port'] = port
            return data
    except requests.exceptions.RequestException:
        pass
    return None

def kick_user(port, role):
    try:
        url = f"http://127.0.0.1:{port}/api/admin/kick_{role}"
        requests.post(url, timeout=2)
        st.toast(f"成功發送踢除指令至房間 {port} 的 {role}")
    except Exception as e:
        st.error(f"無法與房間連線: {e}")

def render_observation_ui():
    st.header("🌐 即時觀測中心 (Real-time Mentoring Monitor)")
    st.markdown("在此檢視所有後端包廂（包含 Docker 多房間）的即時連線與資源使用狀況。")
    
    if st.button("🔄 重新整理", type="primary"):
        st.rerun()

    # 針對可能開啟的 8000, 8001, 8002, 8003 進行掃描
    ports_to_scan = [8000, 8001, 8002, 8003, 8004, 8005]
    active_rooms = []
    
    with st.spinner("掃描系統包廂中..."):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(fetch_status, ports_to_scan))
            for res in results:
                if res:
                    active_rooms.append(res)
                    
    if not active_rooms:
        st.warning("目前找不到任何運行中的包廂 (掃描範圍: 8000 - 8005)。請確認 FastAPI 或 Docker 是否已啟動。")
        return

    st.success(f"掃描完畢！共發現 {len(active_rooms)} 個運作中的包廂。")
    
    for room in active_rooms:
        port = room['port']
        guide = room['guide_name'].capitalize()
        usage = room['usage_limit']
        t_online = "🟢 在線" if room['toby_online'] else "🔴 離線"
        c_online = f"🟢 在線 ({room['client_name']})" if room['client_online'] else "🔴 離線"
        
        with st.expander(f"🚪 房間 [Port {port}] - 導師: {guide}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("剩餘使用次數", usage)
            col2.markdown(f"**導師狀態**<br>{t_online}", unsafe_allow_html=True)
            col3.markdown(f"**顧客狀態**<br>{c_online}", unsafe_allow_html=True)
            
            with col4:
                if room['toby_online']:
                    if st.button(f"踢出導師", key=f"kt_{port}"):
                        kick_user(port, "toby")
                        st.rerun()
                if room['client_online']:
                    if st.button(f"踢出顧客", key=f"kc_{port}"):
                        kick_user(port, "client")
                        st.rerun()
