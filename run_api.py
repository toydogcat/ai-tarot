import uvicorn
from config import conf

if __name__ == "__main__":
    # 將 API 和 Streamlit (預設 8501) 開在不同的 Port 避免衝突
    port = conf.app.api_port if hasattr(conf.app, 'api_port') else 8000
    if not isinstance(port, int):
        port = 8000
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True)
