# 🧠 AI 長期記憶與多維度資料庫架構草案 (Memory & Database System)

> **建立日期**：2026-03-23
> **當前狀態**：草案與想法儲存 (Draft & Ideation)
> **目標**：解決目前 AI 「無狀態、無記憶、不知時事」的痛點，引進長短期記憶機制 (Long-Term/Short-Term Memory) 與外掛知識庫。

## 1. 核心動機 (Motivation)

目前的 AI Tarot & I-Ching 系統是建立在純粹的**無狀態 (Stateless)** API 上。雖然能確保高併發與輕量化，但也導致 AI：
1. **不認識老客戶**：無法記得上次占卜的結果與客戶的背景資料。
2. **缺乏時間與時事感知**：不知道當下世界發生的大事，解讀可能過於空泛。
3. **沒有對話脈絡**：每一次請求對 AI 來說都是第一次見面。

為此，我們需要實作一套「記憶組件 (Memory Components)」與「可抽換式資料庫架構 (Pluggable Database Architecture)」。

---

## 2. 預計支援的資料庫引擎 (Supported DB Providers)

為了兼顧「本機快速開發」與「雲端企業級佈署」，記憶系統將支援多種底層引擎驅動：

1. **Local SQLite (簡化版/預設)**：給開發者本機測試使用，輕量且不需額外設定，使用 JSON 欄位儲存對話歷史或簡易向量。
2. **PostgreSQL (pg/pgvector)**：企業級關聯式資料庫，搭配 `pgvector` 可完美支援 RAG (檢索增強生成) 與海量客戶資料庫查詢。
3. **Supabase**：基於 Postgres 的雲端 BaaS，提供即時的 Auth 與 Database 功能，適合快速上雲與多端同步。
4. **Elasticsearch**：專為海量日誌與全文檢索設計，適合用來搜尋歷年所有占卜紀錄中的特定關鍵字與「時事/趨勢」分析。

---

## 3. 架構設計思維 (Architecture Strategy)

### 📌 YAML 設定檔動態切換 (Dynamic Configuration)
系統不綁死單一資料庫，而是透過 `customer*.yaml` 來動態宣告：

```yaml
memory_system:
  provider: "supabase" # 可選: sqlite, postgres, supabase, elasticsearch
  connection_string: "${ENV:SUPABASE_URL}"
  enable_vector_search: true
  history_limit: 50
```

### 👨‍💻 Streamlit 戰情中心熱重載
負責看管後台的「人類工程師/導師」，可以直接在 Streamlit 的 Admin UI 中：
1. **切換當前連接的資料庫引擎**
2. 檢視該客戶在某資料庫中的過往「記憶實體 (Memory Entities)」，例如：`[職業: 工程師, 上次占卜: 感情不順]`。
3. **強制清除或修改** AI 對某客戶的錯誤記憶。

---

## 4. 未來實作階段劃分 (Implementation Phases)

*   **Phase 1：基礎 SQLite 記憶體**
    *   實作 SQLAlchemy 或純原生 SQLite 讀寫。
    *   在每次呼叫 Gemini 前，自動從資料庫把「前 5 次歷史紀錄」塞進 System Prompt 當中。
*   **Phase 2：Streamlit UI + YAML 管理**
    *   在戰情中心新增「記憶與資料庫管理」分頁。
    *   實作動態更換 Database Provider 的 Adapter 模式 (Repository Pattern)。
*   **Phase 3：企業級資料庫上線 (Supabase/PG)**
    *   導入 Supabase SDK，實作進階的用戶認證 (Auth) 與雲端資料同步。
*   **Phase 4：Elasticsearch 引入與 RAG 結合**
    *   將外部時事或歷史判例寫入 ES，讓 AI 在解讀大六壬或復雜案件時，能主動檢索過往類似案例。
