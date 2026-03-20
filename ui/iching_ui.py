import streamlit as st

def render_line(is_yang, is_moving=False):
    color = "#FF4B4B" if is_moving else "#F0F0F0"
    
    if is_yang:
        return f"<div style='width: 100%; height: 32px; background-color: {color}; margin-bottom: 8px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);'></div>"
    else:
        return f"<div style='display: flex; justify-content: space-between; margin-bottom: 8px;'><div style='width: 45%; height: 32px; background-color: {color}; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);'></div><div style='width: 45%; height: 32px; background-color: {color}; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);'></div></div>"

def render_hexagram(hexagram_data, lines_binary, moving_indices=None):
    if moving_indices is None:
        moving_indices = []
        
    from config import ICHING_ASSETS_DIR
    import os
    
    hex_id = hexagram_data.get('id')
    if hex_id:
        prefer_format = st.session_state.get("prefer_image_format", "jpg")
        img_dir = ICHING_ASSETS_DIR / "hexagrams"
        img_path = img_dir / f"{hex_id}.{prefer_format}"
        
        # Fallback to other format if preferred doesn't exist
        if not img_path.exists():
            alt_format = "png" if prefer_format == "jpg" else "jpg"
            img_path = img_dir / f"{hex_id}.{alt_format}"
            
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
            
    st.markdown(f"### {hexagram_data['name']}")
    st.markdown(f"**{hexagram_data['trigrams']['upper']}上 {hexagram_data['trigrams']['lower']}下**")
    
    html = "<div style='width: 200px; margin: 15px 0;'>"
    # Render from top to bottom (index 5 down to 0)
    for i in reversed(range(6)):
        is_yang = lines_binary[i] == 1
        is_moving = i in moving_indices
        html += render_line(is_yang, is_moving)
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)
    
    if moving_indices:
        st.markdown("<small style='color:#FF4B4B;'>*紅色代表動爻*</small>", unsafe_allow_html=True)
    
    st.markdown(f"*{hexagram_data['description']}*")
    
    with st.expander("爻辭 (Lines)"):
        # The lines in hexagram_data["lines"] are from bottom to top order.
        for i, line_text in enumerate(hexagram_data["lines"]):
            if i in moving_indices:
                st.markdown(f"**👉 <span style='color:#FF4B4B;'>{line_text}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(line_text)
