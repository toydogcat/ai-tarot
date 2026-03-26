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

def kick_user(port, role, mentor_id, client_name=None):
    try:
        if role == "mentor":
            url = f"http://127.0.0.1:{port}/api/admin/rooms/{mentor_id}/kick/mentor"
        else:
            url = f"http://127.0.0.1:{port}/api/admin/rooms/{mentor_id}/kick/client"
            
        params = {}
        if client_name: params['client_name'] = client_name
        response = requests.post(url, params=params, timeout=2)
        if response.status_code == 200:
            st.toast(f"成功發送踢除指令至 {mentor_id} ({client_name or role})")
        else:
            st.error(f"踢除失敗: {response.text}")
    except Exception as e:
        st.error(f"無法與房間連線: {e}")

def update_room_config(port, mentor_id, level=None, usage=None):
    try:
        if level:
            url = f"http://127.0.0.1:{port}/api/admin/rooms/{mentor_id}/level"
            requests.post(url, json={"level": level}, timeout=2)
        if usage is not None:
            url = f"http://127.0.0.1:{port}/api/admin/rooms/{mentor_id}/usage"
            requests.post(url, json={"limit": usage}, timeout=2)
        st.toast("設定已更新")
    except Exception as e:
        st.error(f"更新失敗: {e}")

def render_observation_ui():
    st.header("🌐 即時觀測中心 (Real-time Mentoring Monitor)")
    st.markdown("在此檢視所有後端包廂（包含 Docker 多房間）的即時連線與資源使用狀況。")
    
    if st.button("🔄 重新整理", type="secondary"):
        st.rerun()

    # 針對可能開啟的 8000 - 8005 進行掃描
    ports_to_scan = [8000, 8001, 8002, 8003, 8004, 8005]
    all_active_rooms = []
    
    with st.spinner("掃描系統包廂中..."):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(fetch_status, ports_to_scan))
            for res in results:
                if res and 'rooms' in res:
                    # Each result is an instance status containing one or more rooms
                    for room_data in res['rooms']:
                        room_data['port'] = res['port']
                        all_active_rooms.append(room_data)
                    
    if not all_active_rooms:
        st.warning("目前找不到任何運行中的包廂 (掃描範圍: 8000 - 8005)。請確認 FastAPI 或 Docker 是否已啟動。")
        return

    st.success(f"掃描完畢！共發現 {len(all_active_rooms)} 個運作中的導師房間。")
    
    # 搜尋過濾
    search_query = st.text_input("🔍 搜尋導師名稱 (Mentor ID)", key="mentor_search").strip().lower()
    
    if search_query:
        all_active_rooms = [r for r in all_active_rooms if search_query in r.get('mentor_id', '').lower()]
    
    for room in all_active_rooms:
        port = room.get('port', 0)
        mid = room.get('mentor_id', 'Unknown')
        usage = room.get('usage_limit', 0)
        level = room.get('room_level', 'single')
        clients = room.get('clients', [])
        online_status = "🟢 在線" if room.get('mentor_online', False) else "🔴 離線"
        
        # 預設不要展開 (expanded=False)
        with st.expander(f"🚪 房間 [Port {port}] - 導師: {mid} | 等級: {level.upper()} | {online_status}", expanded=False):
            col_info, col_ctrl = st.columns([2, 1])
            
            with col_info:
                # 剩餘使用次數控制
                c1, c2 = st.columns([1, 1])
                new_usage = c1.number_input(f"剩餘次數 ({mid})", value=usage, step=1, key=f"usage_{port}_{mid}")
                if new_usage != usage:
                    if c1.button("💾 更新次數", key=f"upd_usage_{port}_{mid}"):
                        update_room_config(port, mid, usage=new_usage)
                        st.rerun()
                
                # 房間等級控制
                levels = ["single", "double", "multi"]
                l_idx = levels.index(level) if level in levels else 0
                new_level = c2.selectbox(f"房間等級 ({mid})", levels, index=l_idx, key=f"level_{port}_{mid}")
                if new_level != level:
                    update_room_config(port, mid, level=new_level)
                    st.rerun()

                st.markdown("---")
                # 導師與客戶清單
                if room.get('mentor_online', False) and st.button(f"踢出導師 ({mid})", key=f"kt_{port}_{mid}"):
                    kick_user(port, "mentor", mid)
                    st.rerun()
                
                st.markdown("**客戶及其角色**:")
                if not clients:
                    st.info("目前無客戶在線")
                else:
                    for i, c in enumerate(clients):
                        role_icon = "👑 " if c['is_main'] else "👁️ "
                        cc1, cc2 = st.columns([3, 1])
                        cc1.markdown(f"{role_icon} **{c['name']}**")
                        if cc2.button("踢出", key=f"kc_{port}_{mid}_{i}"):
                            kick_user(port, "client", mid, client_name=c['name'])
                            st.rerun()
            
                st.metric("房間總連線數", len(clients) + (1 if room.get('mentor_online', False) else 0))
                st.caption("小提示：多人房最多支援 4 位客戶。")
