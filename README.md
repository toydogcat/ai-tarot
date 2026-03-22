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
- 🗣️ **Voice Input**: Supports microphone speech-to-text recognition, with manual text editing capabilities.
- 🔍 **Tavily Web Search**: Automatically searches the web for the latest background topics/news (summarized via Gemma 3) to contextually enhance readings.
- 🤖 **Gemini AI Deep Analysis**: Combines spread/hexagram symbols with external context using the latest Gemini engines for profound readings.
- 💾 **Unified History & Client Filtering**: Comprehensively logs all readings and audio data. Supports exclusive dropdown filtering by "Client Name" in the backend, plus detailed CLI skills for recovering failed predictions.
- ⚡ **WebSocket Real-Time Multi-User Communication**: Ensures a truly live connection bridging the "Toby" supervisor and active "Clients" seamlessly, eliminating overlaps and syncing readings continuously.
- ⚙️ **Hydra Dynamic Configuration**: Switch AI models natively via YAML (Customer1, Customer2), and instantly edit context-specific system prompts (Tarot, I-Ching, Zhuge, Da Liu Ren) directly from the Streamlit UI.
- 🎵 **Background Music (BGM)**: Seamlessly toggle different meditation tracks via config to enhance the divination atmosphere.
- 🎨 **Custom Image Format**: Supports flawless switching between high-quality AI-generated `.jpg` and `.png` image formats.
- 🛡️ **Admin Control & Real-Time Monitoring**: Deploy fully independent "Mentor Rooms" via Docker Compose, dynamically adjust AI configs, and track live connection states, usage quotas, and execute Kick controls directly from the Streamlit Observation Dashboard.
- 🚀 **FastAPI & AI Agent Skills**: Exposes independent backend API endpoints (e.g. `/api/tarot/draw`) and AI skill documentation, allowing future AI agents to call the services directly.

## Quick Start

The project currently utilizes a **Monorepo (Frontend/Backend Separation)** architecture:
- `backend/`: Fast API server, AI logic, and the Streamlit admin/testing interface.
- `frontend/`: A highly customized HTML/CSS/JS frontend built with Vite.

### 1. Launch Backend API & Streamlit Interface

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start FastAPI (Default Port: 8000)
python run_api.py

# (Optional) Start Streamlit Admin & Testing Interface (Default Port: 8501)
streamlit run app.py
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

### 5. Running the Application

This project supports **Local Start** (0.0.0.0) as well as **Ngrok Remote Tunneling**.

#### Standard Local Start (0.0.0.0)
```bash
cd backend
python run.py
# Or use streamlit directly:
# streamlit run app.py --server.address=0.0.0.0
```
Your browser will auto-open `http://localhost:8501`. Other devices on the same local network can access the app via your local IP (e.g., `http://192.168.1.xxx:8501`).

#### API Server (For AI Agents / Extensions)
To start just the FastAPI backend service, open a terminal and run:
```bash
cd backend
python run_api.py
```
The API will run on `http://localhost:8000`. You can test endpoints via Swagger UI at `http://localhost:8000/docs`.

#### Ngrok Remote Public Sharing
To share your application publicly online, the project integrates an automated Ngrok script:
1. Register for Ngrok and get an [Auth Token](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Add your token to the `backend/.env` file: `NGROK_AUTHTOKEN=your_token_here`
3. Check that `frontend/vite.config.js` has `allowedHosts: true` (already configured).
4. Run the sharing script smoothly from the root directory:
   ```bash
   python share_ngrok.py
   ```
5. The terminal will output a public URL such as `https://1234abcd.ngrok-free.app`. Share this link with anyone!

#### 🐳 Docker Multi-Room Deployment (Production Mode)
For hosting scalable environments with completely independent config overrides:
```bash
# Build and launch multiple independent "Mentor Rooms" via docker-compose
docker compose up -d --build
```
This automatically boots up `tarot-room-1` (port 8001) and `tarot-room-2` (port 8002), serving both the FastAPI backend and pre-compiled Vite frontend dynamically.

## 🧪 Automated Testing (Unit Testing)

The project includes a comprehensive `pytest` test suite located in `backend/tests/`. It covers:
- **WebSocket Communication**: Ensures isolated "Toby" and "Client" connection channels and correct broadcasting.
- **Dynamic Configuration (ConfigManager)**: Validates reading/writing of YAML templates and fallback logic.
- **History API**: Verifies client-name-based data filtering and prediction deduplication logic.
- **AI Interpreters**: Mocks Gemini LLM APIs to validate dynamic prompt payload generation.

**Executing the tests:**

```bash
cd backend
# Activate virtual environment (or your conda env)
source venv/bin/activate
pip install pytest pytest-asyncio httpx
PYTHONPATH=. pytest -v tests/
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
│   ├── run_api.py          # FastAPI entry point (8000)
│   ├── app.py              # Streamlit test & admin UI (8501)
│   ├── run.py              # Unified startup script
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

## License

MIT
