import streamlit as st

def render_daliuren(res: dict):
    st.markdown("""
    <style>
    .dlr-container {
        background-color: rgba(30, 30, 30, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        color: #E8D5B7;
    }
    .dlr-header {
        font-size: 1.2rem;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 10px;
    }
    .dlr-row {
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin: 10px 0;
    }
    .dlr-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 8px;
        min-width: 60px;
    }
    .dlr-label {
        font-size: 0.8rem;
        color: #B8A88A;
        margin-bottom: 5px;
    }
    .dlr-val {
        font-size: 1.1rem;
        font-weight: bold;
    }
    .dlr-title {
        color: #B8A88A;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    jieqi = res.get("jieqi", "")
    date_str = res.get("date", "")
    patterns = res.get("pattern", [])
    san_chuan = res.get("san_chuan", {})
    si_ke = res.get("si_ke", {})

    pattern_str = "、".join(patterns) if patterns else "無特殊格局"

    import textwrap
    
    # HTML Layout - NO leading whitespace to avoid Markdown code blocks
    html = f"""<div class="dlr-container">
<div class="dlr-header">🌌 <b>時局</b>：{date_str} ({jieqi}) &nbsp;|&nbsp; <b>格局</b>：{pattern_str}</div>"""

    # 三傳 (San Chuan)
    html += '<div class="dlr-title">三傳</div><div class="dlr-row">'
    chuan_keys = ["初傳", "中傳", "末傳"]
    for k in chuan_keys:
        if k in san_chuan:
            val = san_chuan[k]
            display_val = val[0] if isinstance(val, list) and len(val) > 0 else str(val)
            sub_val = val[1] if isinstance(val, list) and len(val) > 1 else ""
            html += f"""<div class="dlr-item">
<span class="dlr-label">{k}</span>
<span class="dlr-val">{display_val}</span>
<span class="dlr-label" style="margin-top:2px;">{sub_val}</span>
</div>"""
    html += '</div>'

    # 四課 (Si Ke)
    html += '<div class="dlr-title">四課</div><div class="dlr-row">'
    ke_keys = ["四課", "三課", "二課", "一課"]
    for k in ke_keys:
        if k in si_ke:
            val = si_ke[k]
            display_val = val[0] if isinstance(val, list) and len(val) > 0 else str(val)
            if len(display_val) >= 2:
                top = display_val[0]
                bottom = display_val[1]
                html += f"""<div class="dlr-item">
<span class="dlr-label">{k}</span>
<span class="dlr-val">{top}</span>
<span class="dlr-val">{bottom}</span>
</div>"""
            else:
                html += f"""<div class="dlr-item">
<span class="dlr-label">{k}</span>
<span class="dlr-val">{display_val}</span>
</div>"""
    html += '</div>'

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
