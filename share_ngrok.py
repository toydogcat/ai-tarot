import os
import sys
import subprocess
from dotenv import load_dotenv

# 讀取 .env 中的 NGROK_AUTHTOKEN
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

def start_ngrok(port):
    try:
        from pyngrok import ngrok, conf
    except ImportError:
        print("未安裝 pyngrok，正在為您動態安裝...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
        from pyngrok import ngrok, conf
        
    auth_token = os.getenv("NGROK_AUTHTOKEN")
    if auth_token:
        ngrok.set_auth_token(auth_token)
    else:
        print("====== ⚠️ 尚未設定 NGROK_AUTHTOKEN ======")
        print("請在 backend/.env 檔案中加入：")
        print("NGROK_AUTHTOKEN=您的_ngrok_api_key")
        print("=========================================\n")

    print(f"=====================================")
    print(f"啟動 ngrok 代理 local port {port}...")
    try:
        # 開啟 tunnel
        public_url = ngrok.connect(port).public_url
        print(f"=====================================")
        print(f"🎉 成功分享！您的對外公開網址為:")
        print(f"👉 {public_url}")
        print(f"=====================================")
        print("請將此網址分享給其他人即可使用占卜功能。")
        print("請保持此視窗開啟，按下 Ctrl+C 結束分享。")
    except Exception as e:
        print(f"連線失敗: {e}")
        print("如果出現 authtoken 錯誤，請先註冊 ngrok 帳號，並執行：")
        print("ngrok config add-authtoken <你的 token>")
        return
    
    try:
        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print("\n正在關閉 ngrok...")
        ngrok.kill()

if __name__ == "__main__":
    start_ngrok(8000)
