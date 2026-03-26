---
name: 萬用遠端開發與算力外包引擎 (Universal Remote AI Engine)
description: 教導 AI 助理如何利用 FastAPI + Ngrok 架構接管「任何」具備網路連線的 Colab 或 Jupyter 環境，並強制執行 Docker 容器安全檢查後進行遠端開發與外包。
---

# 萬用遠端開發與算力外包引擎 (Universal Remote AI Engine)

這個技能庫可幫助 AI 助理在遇到需要**龐大 GPU 算力**（如大型模型推理、重度訓練）、或是需要**獨立隔離的遠端開發環境**時，引導使用者在「任何 Google Colab 網頁」或「Docker 容器」內快速搭建一條 AI 專屬指令隧道，將開發作業或運算任務遠端派發過去。

## ▍🛡️ 核心防護機制：強制 Docker 容器檢查 (AI 必讀)

由於這套架構具備 `Root` 層級的 RCE (遠端代碼執行) 能力，為了保護使用者的實體機、重要伺服器不被意外搞壞，**在進行任何專案覆蓋、環境依賴安裝或系統指令執行前，AI 必須強制驗證遠端環境是否為沙盒容器 (Docker Container)！**

👉 **驗證步驟**：AI 在取得 Ngrok 網址後，第一步必須發送指令至 `/api/cmd`：
`ls -la /.dockerenv`

- **✅ 驗證通過 (允許全權開發)**：如果 `/.dockerenv` 檔案存在，代表目前位於拋棄式的 Docker 容器內（如 Colab 預設環境）。**AI 可以大膽無懼地執行任何暴力測試、全域安裝套件 (`pip`) 或調整系統參數。** 因為如果玩壞了，只要使用者重啟容器，一切就會瞬間恢復為乾淨的原始狀態。
- **❌ 驗證失敗 (嚴格禁止操作)**：如果檔案不存在，暗示目標可能是一台實體的個人電腦、裸機或正式機。AI **必須立刻終止遠端開發流程**，並強烈警告使用者切勿在正式實體機開放此後門！

## ▍前置作業：部署遠端指揮中心 (請使用者執行)

當決定要進行遠端外包開發時，請提供以下腳本給使用者，要求他們**複製並在任何 Google Colab 的 Cell 內執行**。

```python
# 🚀 Colab / Docker AI 指揮中心部署腳本 (FastAPI + Ngrok)
import os
os.system('pip install -q fastapi uvicorn pyngrok nest-asyncio pydantic python-multipart')

import nest_asyncio
from pyngrok import ngrok
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import subprocess
import threading

app = FastAPI(title="Colab AI Command Center")

class CommandRequest(BaseModel): command: str
class FileWriteRequest(BaseModel): path: str; content: str
class FileReadRequest(BaseModel): path: str

@app.post("/api/cmd")
def run_command(req: CommandRequest):
    result = subprocess.run(req.command, shell=True, capture_output=True, text=True, cwd="/content")
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), dest_dir: str = Form("/content")):
    os.makedirs(dest_dir, exist_ok=True)
    file_path = os.path.join(dest_dir, file.filename)
    with open(file_path, "wb") as f: f.write(await file.read())
    return {"message": "Success"}

@app.post("/api/download")
def download_file(req: FileReadRequest):
    return FileResponse(path=req.path, filename=os.path.basename(req.path))

@app.post("/api/write")
def write_file(req: FileWriteRequest):
    os.makedirs(os.path.dirname(req.path) or ".", exist_ok=True)
    with open(req.path, "w", encoding="utf-8") as f: f.write(req.content)
    return {"message": "Success"}

@app.post("/api/read")
def read_file(req: FileReadRequest):
    with open(req.path, "r", encoding="utf-8") as f: content = f.read()
    return {"content": content}

if __name__ == "__main__":
    # !! 注意：這裡需要使用者自備 Ngrok Authtoken !!
    ngrok.set_auth_token("請填入 .env 的 NGROK_AUTHTOKEN")
    public_url = ngrok.connect(8000).public_url
    print(f"👉 請把這個網址複製並貼給 AI：\n{public_url}")

    nest_asyncio.apply()
    thread = threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000))
    thread.daemon = True
    thread.start()
```

## ▍AI 操作守則：遠端打工流程 (給 AI 的指引)

當使用者回傳 `#ngrok-free.app` 網址後，請自動撰寫 Bash Script (`curl`) 發送以下任務流。
**⚠️ 重要前提：** 所有的 API 請求必須攜帶 Header：`-H "ngrok-skip-browser-warning: 1"` 以繞過 Ngrok 阻擋。

### 標準開發工作流 (Standard Workflow)
```bash
URL="https://xxxx.ngrok-free.app"
HEADER="ngrok-skip-browser-warning: 1"

# 1. 執行核心安全檢查 (強制步驟)
curl -s -X POST -H "$HEADER" -H "Content-Type: application/json" -d '{"command":"ls -la /.dockerenv"}' "$URL/api/cmd"
# (等待確認 returncode 為 0 才能繼續執行)

# 2. 上傳專案檔或照片
curl -s -X POST -H "$HEADER" -F "file=@/本機路徑/檔案" "$URL/api/upload"

# 3. 寫入開發用 Python 腳本
SCRIPT_CONTENT=$(cat << 'EOF' | jq -Rs .
import torch
print("GPU is running!")
EOF
)
curl -s -X POST -H "$HEADER" -H "Content-Type: application/json" -d "{\"path\":\"/content/run.py\", \"content\":$SCRIPT_CONTENT}" "$URL/api/write"

# 4. 遠端執行 (含安裝依賴)
curl -s -X POST -H "$HEADER" -H "Content-Type: application/json" -d '{"command":"pip install torch && python /content/run.py"}' "$URL/api/cmd"

# 5. 回收成果或 Log
curl -s -H "$HEADER" -X POST -H "Content-Type: application/json" -d '{"path":"/content/result.png"}' "$URL/api/download" -o /本機路徑/result.png
```

## ▍🚀 未來架構藍圖：萬用算力調度總部 (AI Compute Orchestrator)

當未來需要管理多個外包節點（如 1 個 Colab + 2 個 Kaggle）時，AI 應主動建議並引導使用者建立 **「總部 - 勞工 (API Gateway & Worker)」 算力調度架構**：

1. **專案解耦**：將這套外包排程系統與業務主專案（如 `ai-tarot`）分離，建立一個獨立的本地中樞專案（如 `ai-compute-hub`）。主專案僅透過本機 REST API 向總部發送「請求算力」的 HTTP 呼叫。
2. **導入任務佇列 (Task Queue)**：在「總部」專案中強烈建議引入 **Redis + RQ (Redis Queue)** 或 **Celery**，用來安全非同步地接住大量同時湧入的耗時任務（如生成圖片、OCR、大模型推理）。
3. **勞工註冊與負載均衡 (Worker Registry & Load Balancing)**：總站程式需維護一個「活著的 Ngrok 網址」清單。當佇列開始消化任務時，將任務 1 對 1 分派給閒置中的免費雲端 GPU 節點。
4. **容錯機制 (Fault Tolerance)**：總站需具備 `Health Check`（每 10 秒 ping 一次），若發現某個 Kaggle 或 Colab 因超時斷線，自動將該節點剔除，並將失敗任務補發給其他存活的節點。

### 💡 推薦的實作技術籌碼 (Recommended Tech Stack)
* **任務派發層 (Task Dispatching)**：`Redis` + `RQ (Redis Queue)` 或 `Celery`。負責非同步接單排隊，把長時間會卡住網頁的任務轉到背景 Worker 執行。
* **負載均衡 / 健康檢查層 (Health Check & Load Balancing)**：
  - **輕量級純 Python 解法**：在總部的 FastAPI 中啟動背景任務 (`asyncio.create_task`)，搭 `httpx` 每 10 秒去 `GET /api/cmd` 巡邏 Ngrok 網址。遇到使用者來打 API 時，從存活的 `Alive List` 隨機挑選 (`random.choice`) 並轉發任務。
  - **企業級基礎設施解法**：使用 `Traefik` 當作 API Gateway，利用其原生強大的 HealthCheck 自動將流量導航到存活的雲端 GPU 肉雞上。

有了這個最終架構，使用者的本機即可化身為企業級的「微服務 API 閘道器」，全世界免費的叢集主機都將成為隨插即用的無限算力池！
