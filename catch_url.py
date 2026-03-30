import subprocess
import re
import os
import sys

# --- Configuration ---
ENV_FILE = os.path.join(os.path.dirname(__file__), "frontend", ".env.production")
# Docker Compose 預設會加上資料夾名稱作為前綴 (ai-tarot-xxxx)
CONTAINER_NAME = "ai-tarot-cloudflared-test-1" 

def catch_and_update():
    print(f"🔍 正在監控 {CONTAINER_NAME} 的日誌以獲取 Cloudflare URL...")
    
    # Run docker logs -f --since 1m to avoid picking up stale URLs from previous runs
    process = subprocess.Popen(
        ["docker", "logs", "-f", "--since", "1m", CONTAINER_NAME],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
    
    try:
        for line in process.stdout:
            match = url_pattern.search(line)
            if match:
                new_url = match.group(0)
                print(f"🎉 攔截到 Cloudflare 網址: {new_url}")
                
                # Update frontend/.env.production
                update_env(new_url)
                
                print("\n✅ 更新完成！您現在可以執行：")
                print(f"   cd frontend && npm run build:prod && firebase deploy")
                
                # Stop monitoring once found
                process.terminate()
                return
    except KeyboardInterrupt:
        process.terminate()
        print("\n停止監控。")

def update_env(url):
    if not os.path.exists(ENV_FILE):
        print(f"⚠️ 找不到環境檔: {ENV_FILE}，將手動建立。")
        with open(ENV_FILE, "w") as f:
            f.write(f"VITE_API_URL={url}\n")
        return

    with open(ENV_FILE, "r") as f:
        lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.startswith("VITE_API_URL="):
            new_lines.append(f"VITE_API_URL={url}\n")
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f"VITE_API_URL={url}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(new_lines)
    print(f"📝 已寫入 {ENV_FILE}")

if __name__ == "__main__":
    catch_and_update()
