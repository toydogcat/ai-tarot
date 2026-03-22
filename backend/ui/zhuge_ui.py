import streamlit as st

def render_zhuge(res: dict):
    st.markdown("""
    <style>
    .zg-container {
        background-color: rgba(30, 30, 30, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        color: #E8D5B7;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .zg-header {
        font-size: 1.4rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 15px;
        color: #D4AF37;
        letter-spacing: 2px;
    }
    .zg-poem {
        font-size: 1.3rem;
        line-height: 2;
        text-align: center;
        margin: 20px 0;
        color: #F8F0E3;
        font-family: 'Noto Serif TC', serif;
        word-break: keep-all;
    }
    .zg-explanation-title {
        color: #B8A88A;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 10px;
        font-size: 1.1rem;
        border-left: 4px solid #D4AF37;
        padding-left: 10px;
    }
    .zg-explanation {
        font-size: 1rem;
        line-height: 1.8;
        color: #CCCCCC;
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    lot_id = res.get("id", "")
    poem = res.get("poem", "")
    interp1 = res.get("interp1", res.get("explanation", ""))
    interp2 = res.get("interp2", "")

    import textwrap
    
    # Layout
    html = textwrap.dedent(f"""
    <div class="zg-container">
        <div class="zg-header">
            🎋 諸葛神算 第 {lot_id} 籤
        </div>
        <div class="zg-poem">
            {poem}
        </div>
    """)
    
    if interp1:
        html += textwrap.dedent(f"""
        <div class="zg-explanation-title">白話解讀</div>
        <div class="zg-explanation">
            {interp1}
        </div>
        """)
    
    if interp2:
        html += textwrap.dedent(f"""
        <div class="zg-explanation-title">古典意象</div>
        <div class="zg-explanation">
            {interp2}
        </div>
        """)
        
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)
