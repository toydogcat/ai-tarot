---
name: docker-ops
description: 教導 AI 助理如何扮演「苦力工程獅」，維護與管理 AI Tarot 的 Docker 多房間部署架構，包含啟動/停止容器以及透過 Admin API 動態修改房間設定。
---

# Docker Operations & Admin API Skill (苦力工程獅維運指南)

這份文件教導身為 AI 助理的你，如何操作 Docker 來管理 AI Tarot 的多房間部署架構，以及如何針對運行中的特定房間（容器）透過 Admin API 動態調配資源 (如更換 API Key 或可用次數)。
當人類要求你「幫我管理房間」、「開一個新房間」或「幫 room-1 儲值次數」時，你應該依賴這項技能。

## 🐳 1. Docker 基礎操作 (Lifecycle Management)

專案提供了 `docker-compose.yml` 來定義 Mentor 房間。每個房間等同於一個獨立的 FastAPI + Vite 服務實體。

- **啟動所有房間 (背景執行)**:
  使用您的 `run_command` 工具在專案根目錄執行：
  ```bash
  docker compose up -d
  ```

- **重啟特定房間**:
  若發生任何預期外的系統停擺，或是想要將環境變數重置回 Git 初始狀態：
  ```bash
  docker compose restart <service_name>
  # 範例：docker compose restart mentor-room-1
  ```

- **查看房間狀態與日誌**:
  用來排查無法啟動或 `500 Internal Server Error` 的問題：
  ```bash
  docker compose ps
  docker compose logs --tail=50 mentor-room-1
  ```

## ⚙️ 2. 動態設定覆寫 (Admin API 操作)

你能夠直接**熱重載**每個房間的 `.env` 變數與 `customer*.yaml` 設定！這全部歸功於專屬的 Admin API，不需要重新啟動 Docker 容器。
- **預設 Admin Token**: 預設密碼寫在原始 `.env` 的 `ADMIN_TOKEN` 中 (若未設定則為 `default_secret_token`)。
- **對應正確的 Port**: 每次動手前，先查閱 `docker-compose.yml` 確認該操作「房間」所綁定的 Host Port（例如：`mentor-room-1` 通常綁定 `8001`，`mentor-room-2` 綁定 `8002`）。

### 動作 A：修改 Gemini API Key (或任何環境變數)
當人類抱怨「Token 爆了」或者要求「換一把鑰匙」時：
**Endpoint:** `POST /api/admin/config/env`

**範例呼叫 (針對 Room 1, Port 8001):**
```bash
curl -X POST "http://127.0.0.1:8001/api/admin/config/env" \
     -H "X-Admin-Token: default_secret_token" \
     -H "Content-Type: application/json" \
     -d '{"key": "GEMINI_API_KEY", "value": "AIzaSy_NEW_YOUR_KEY_HERE"}'
```
*註：呼叫成功後，下一次的占卜請求就會立刻使用這把新的 Key！*

### 動作 B：修改使用次數上限 (Usage Limit) 與各種參數
當人類要求「幫這間房儲值」或「修改占卜模型」時：
**Endpoint:** `POST /api/admin/config/yaml`

利用「深層屬性字串」(Dot Notation) 輕鬆覆寫 YAML 內容：
- `app.usage_limit` = 負責次數追蹤
- `modes.tarot.model_name` = 修改塔羅牌指定的 Gemini 模型

**範例呼叫 (幫 Room 2, Port 8002 儲值 50 次):**
```bash
curl -X POST "http://127.0.0.1:8002/api/admin/config/yaml" \
     -H "X-Admin-Token: default_secret_token" \
     -H "Content-Type: application/json" \
     -d '{
       "filename": "customer2.yaml",
       "updates": {
         "app.usage_limit": 50
       }
     }'
```
*註：這會立刻修改對應容器內的 YAML 檔案。前端只要重新整理，就能看到剩餘可用次數變成 50。*

## 💡 給 AI 苦力工程獅的最高原則
1. **絕對不亂動 Host 檔案系統的 `.env`**：在 Docker 多房間架構下，每間房有獨立的宇宙。你應該**只透過 Admin API** 去控制那個容器內的環境，絕對不要直接修改本機外層的 `.env` 或 `customer.yaml` 原始檔，因為這會干擾下次的啟動。
2. **先幫人類檢查日誌**：如果被告知房間壞了，請優先查看 `docker compose logs`，接著再去檢查是否額度用盡。
