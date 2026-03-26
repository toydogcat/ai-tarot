import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def render_page_agent():
    """
    將 Alibaba Page-Agent 嵌入 Streamlit 頁面。
    此組件會運行於瀏覽器端，並使用環境變數中的 GEMINI_API_KEY。
    """
    
    # 從環境變數或 Streamlit Secrets 取得 API KEY
    gemini_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    
    if not gemini_key:
        return # 若無金鑰則不顯示
        
    # Page-Agent HTML 範本 (具有 iframe 穿透能力)
    page_agent_html = f"""
    <script>
      (function() {{
        // 確保在主視窗中加載，而非僅在 iframe 中
        const targetWindow = window.parent || window;
        const targetDoc = targetWindow.document;

        if (targetWindow.PageAgent) {{
            console.log("Page-Agent already initialized in parent.");
            return;
        }}

        // 定義 CSS 強制將 Page-Agent 移向左邊
        const style = targetDoc.createElement('style');
        style.innerHTML = `
          /* 強制將 Page-Agent 的懸浮球與面板移動到左側 */
          #page-agent-container, 
          .page-agent-trigger,
          [class*="page-agent"] {{
            left: 20px !important;
            right: auto !important;
          }}
        `;
        targetDoc.head.appendChild(style);

        // 動態建立 script 標籤插入主視窗 head
        const script = targetDoc.createElement('script');
        script.src = "https://cdn.jsdelivr.net/npm/@alibaba/page-agent@latest/dist/index.iife.js";
        script.crossOrigin = "anonymous";
        
        script.onload = function() {{
          console.log("Page-Agent SDK loaded successfully.");
          if (targetWindow.PageAgent) {{
            targetWindow.PageAgent.init({{
              llm: {{
                provider: 'gemini',
                apiKey: '{gemini_key}',
                model: 'gemini-1.5-flash'
              }}
            }});
            console.log("Page-Agent initialized at the left side.");
          }}
        }};

        targetDoc.head.appendChild(script);
      }})();
    </script>
    """
    
    import streamlit.components.v1 as components
    # 這裡我們仍使用 components.html 作為觸發器
    components.html(page_agent_html, height=0, width=0)
