# 🔮 AI Tarot & ☯️ I-Ching

[English](README.md) | [繁體中文](README_zh.md)

An AI-driven Tarot card and I-Ching (Hexagram) divination web application, featuring intuitive user interfaces and a professional management backend.

### 🌟 General User Interface (Vite Frontend)
<p align="center">
  <img src="sample/demo2.jpg" alt="AI Tarot & I-Ching UI" width="600">
  <img src="sample/demo2_android.jpg" alt="Mobile UI" height="340">
</p>

### ⚙️ Professional Reading & Management (Streamlit Backend)
### ⚙️ Professional Reading & Management (Streamlit Backend)
<p align="center">
  <img src="sample/demo1.jpg" alt="AI Tarot & I-Ching Backend" width="800">
</p>
<p align="center">
  <img src="sample/demo1_room.jpg" alt="Real-time Mentoring Monitor" width="800">
</p>

### 💬 Chat Bot Integration (n8n AI Agent)
<p align="center">
  <img src="sample/demo3.jpg" alt="Discord Bot Integration" width="800">
</p>

## Features

- 💬 **Multi-Platform Chat Bots**: Utilizing n8n Advanced AI as a conversational state machine, providing a stateless API backend for seamless Line / Discord integration.
- 🔮 **Tarot Reading**: Full 78 cards, 6 classic spreads, upright/reversed meanings, and detailed interpretations.
- ☯️ **I-Ching Divination**: Simulates traditional coin tossing to generate hexagrams, displaying original/changed hexagrams and moving lines.
- 🎋 **Zhuge Shensuan**: Provides 384 traditional lots with poetic explanations and AI analysis.
- 🎲 **Xiao Liu Ren**: Fast and intuitive 3-state divination based on traditional numerology, perfect for quick daily guidance.
- 🌌 **Da Liu Ren**: Generates a simplified time-based pattern with San Chuan (Three Transmissions) and Si Ke (Four Hexagrams) for deep AI divination.
- 🗣️ **Voice Input & Async TTS**: Supports microphone speech-to-text recognition, with manual text editing. Now fully asynchronous with high-quality edge-tts integration to prevent event-loop conflicts.
- 🔍 **Tavily Web Search**: Automatically searches the web for the latest background topics/news (summarized via Gemma 3) to contextually enhance readings.
- 🤖 **Gemini AI Deep Analysis**: Combines spread/hexagram symbols with external context using the latest Gemini engines for profound readings.
- 💾 **Unified History & Client Filtering**: Comprehensively logs all readings and audio data. Supports exclusive dropdown filtering by "Client Name" in the backend, plus detailed CLI skills for recovering failed predictions.
- ⚡ **WebSocket Real-Time Multi-User Communication**: Ensures a truly live connection bridging the "Toby" supervisor and active "Clients" seamlessly, with optimized reconnection logic.
- 🛡️ **Security Hardening**: Mentor accounts are secured with **Bcrypt** password hashing, replacing legacy plaintext storage.
- ⚙️ **Hydra Dynamic Configuration**: Switch AI models natively via YAML (Customer1, Customer2), and instantly edit context-specific system prompts (Tarot, I-Ching, Zhuge, Da Liu Ren) directly from the Streamlit UI.
- 🎵 **Background Music (BGM)**: Seamlessly toggle different meditation tracks via config to enhance the divination atmosphere.
- 🎨 **Custom Image Format**: Supports flawless switching between high-quality AI-generated `.jpg` and `.png` image formats.
- 🛡️ **Admin Control & Real-Time Monitoring**: Deploy fully independent "Mentor Rooms" via Docker Compose, dynamically adjust AI configs, and track live connection states, usage quotas, and execute Kick controls directly from the Streamlit Observation Dashboard. Fully supports the **AI-Factory Global Identity Tier** for shared mentor social data across projects.
- 📱 **PWA Support**: Native-like app experience with Progressive Web App support—install the app on your home screen for full-screen, standalone usage.
- 🚀 **FastAPI & AI Agent Skills**: Exposes independent backend API endpoints (e.g. `/api/tarot/draw`) and AI skill documentation, allowing future AI agents to call the services directly.

## Quick Start

The project currently utilizes a **Monorepo (Frontend/Backend Separation)** architecture:
- `backend/`: Fast API server, AI logic, and the Streamlit admin/testing interface.
- `frontend/`: A highly customized HTML/CSS/JS frontend built with Vite.

### 1. Launch Backend API & Streamlit Interface

```bash
cd backend

# [Recommended] Fast initialization using uv
uv sync
source .venv/bin/activate
# (Fallback) Or use traditional Conda
# conda activate toby

# (Fallback) Or use traditional Conda/venv
# conda create -n toby python=3.10 && conda activate toby
# pip install -r requirements.txt

# Start API Server (FastAPI)
python start.py api

# Start Admin & Testing Interface (Streamlit)
python start.py admin
```

### 2. Launch the Vite Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```
Then open `http://localhost:5173` in your browser to experience the ultimate divination UI.

### 3. Download Image Assets

Due to their large size, the image assets are not included in the repository. Please download the `ai-tarot-images.zip` file from the following link:
[👉 Click here to download image resources (Google Drive)](https://drive.google.com/file/d/1e0_HGeluSyamB-rykJzBZsJj6w8Nln09/view?usp=sharing)

After downloading, place `ai-tarot-images.zip` into the `assets/` folder and extract the `images/` directory.
The final structure should look like this:
```
assets/
└── images/
    ├── tarot/
    └── iching/
```
If you start the app without images, the UI will automatically fall back to text boxes without crashing.

### 4. Setup Environment Variables

```bash
# Copy the example environment file inside the backend directory
cd backend
cp .env.example .env

# Edit backend/.env and fill in required API keys:
# GEMINI_API_KEY=your_gemini_key
# N8N_API_KEY=your_n8n_key (if using the Chat Bot agent)
```

## 🚀 Deployment & Testing Stages

The project is structured into three distinct environment stages to ensure stability from development to production.

### 1. Development Stage (Local Dev)
- **Goal**: Rapid backend logic & UI iteration.
- **Backend**: 
  ```bash
  cd backend && python start.py api
  ```
- **Frontend**: 
  ```bash
  cd frontend && npm install && npm run dev
  ```
- **Access**: `http://localhost:5173`

### 2. Staging Stage (Firebase Hosting Channel)
- **Goal**: Verify remote connectivity & mobile access using temporary URLs.
- **Backend (ngrok)**:
  ```bash
  # Automatically shares local API and updates .env.staging
  uv run python share_ngrok.py
  ```
- **Frontend (Firebase Channel)**:
  ```bash
  cd frontend
  npm run build:stg
  firebase hosting:channel:deploy staging
  ```
- **Access**: Via the temporary URL provided by Firebase (e.g., `ai-factory-tarot--staging-xxx.web.app`).

### 3. Production Isolation Test (Docker + Tunnel)
- **Goal**: Full containerized verification with "Limited Liability" plug-in architecture.

#### 🚀 The One-Line Deployment (Automated)
If you have `docker`, `python`, `npm`, and `firebase-tools` installed, you can run the entire production sync with one command:
```bash
./run.sh
```
This script will:
1. Kill any processes on ports 8001/8002.
2. Restart backend containers with `docker compose`.
3. Auto-sync the Cloudflare Tunnel URL to frontend configs via `catch_url.py`.
4. Build the production frontend and deploy to Firebase.

#### 🛠️ Manual Steps
- **Backend (Docker)**:
  ```bash
  docker compose up -d --build
  python catch_url.py
  ```
- **Frontend (Firebase Production)**:
  ```bash
  cd frontend && npm run build:prod && firebase deploy
  ```
- **Access**: `https://ai-factory-tarot.web.app` or the Cloudflare Tunnel URL directly (thanks to "Environment Aware" routing in `main.js`).

---

### 🐳 Docker Multi-Room Management
For hosting multiple independent "Mentor Rooms" via docker-compose:
```bash
docker compose up -d
```
This boots `tarot-room-1` (port 8001) and `tarot-room-2` (port 8002). Each room uses its own `/backend/history` volume for persistence.

## 🧪 Automated Testing (Unit Testing)

The project includes a comprehensive `pytest` test suite located in `backend/tests/`. It covers:
- **WebSocket Communication**: Ensures isolated "Toby" and "Client" connection channels and correct broadcasting.
- **Dynamic Configuration (ConfigManager)**: Validates reading/writing of YAML templates and fallback logic.
- **History API**: Verifies client-name-based data filtering and prediction deduplication logic.
- **AI Interpreters**: Mocks Gemini LLM APIs to validate dynamic prompt payload generation.

**Executing the tests:**

```bash
cd backend
# Activate virtual environment (uv or your conda env)
source .venv/bin/activate
uv pip install pytest pytest-asyncio httpx
uv run pytest -v tests/
```

## Project Structure

```text
ai-tarot/
├── frontend/               # Vite Frontend (User UI)
│   ├── index.html          # Main page & i18n tags
│   ├── src/main.js         # Frontend core logic & dynamic UI
│   ├── public/             # Static public assets
│   └── vite.config.js      # Vite dev server & API proxy config
├── backend/                # FastAPI / Streamlit Backend
│   ├── start.py            # Unified application entry point
│   ├── app.py              # Streamlit router (Main entry)
│   ├── api/                # FastAPI routes & schemas
│   ├── core/               # Core engines (Tarot, I-Ching, AI Interpretation, TTS)
│   ├── config/             # Hydra configs (default/customer YAML)
│   ├── assets/             # Tarot/I-Ching images & BGM soundtracks
│   ├── data/               # Static dataset (JSON)
│   ├── history/            # User reading history logs
│   ├── tools/              # Error recovery & migration scripts
│   └── ui/                 # Streamlit UI specific components
├── ai_notice/              # Development guidelines & agent documentation
├── share_ngrok.py          # Ngrok automated sharing script
├── .env.example            # Environment variables template
└── README.md               # Main project documentation (English)
```

## Image Guidelines

Card and hexagram images are placed under `backend/assets/images/`. Refer to [IMAGE_GUIDE.md](ai_notice/IMAGE_GUIDE.md) to understand filename formatting and image generation prompts.

## Credits

Special thanks to the following tools and teams for supporting this project:
- 🎵 **Background Music (BGM)**: Generated by [Suno](https://suno.com/) AI music platform, making it incredibly easy to craft atmospheric meditation tracks for ultimate immersion.
- 🎨 **Visual Assets (Images)**: Tarot cards and hexagram images were generated by the powerful [Nano Banana2](https://civitai.com/models/25995?modelVersionId=32988) vision-based model, blending profound Eastern Zen with mystical esoteric vibes.
- 💻 **Collaboration Engineer (Programming)**: Project architecture, API integration, and code refactoring were co-developed with **Antigravity**, an agentic AI software engineer by Google DeepMind.

<div align="right">
  <sub><i>💡 <a href="ai_notice/VISION_ARCHITECTURE.md">Sneak peek: The visionary blueprint of the AI Consultant Framework</a></i></sub>
</div>

## License

MIT
