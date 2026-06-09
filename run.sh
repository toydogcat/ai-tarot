#!/bin/bash

# --- AI-Tarot Full Stack Deployment Script (Prod Test) ---

# Ensure we are in the script's directory
cd "$(dirname "$0")"

echo "🚀 Starting AI-Tarot Isolated Production Deployment..."

# --- 0. Environment Setup & Tool Detection ---
echo "🔍 0/4: Setting up environment and detecting tools..."

# Detect Python
if command -v python3 &>/dev/null; then
  PYTHON_EXE="python3"
elif command -v python &>/dev/null; then
  PYTHON_EXE="python"
else
  echo "❌ Error: Python not found."
  exit 1
fi

# Load NVM if available (necessary for some server environments)
if [ -s "$HOME/.nvm/nvm.sh" ] && ! command -v npm &>/dev/null; then
  echo "ℹ️  Sourcing NVM from $HOME/.nvm/nvm.sh..."
  . "$HOME/.nvm/nvm.sh"
fi

# Final Tool Check
for cmd in npm firebase docker; do
  if ! command -v $cmd &>/dev/null; then
    echo "❌ Error: $cmd not found in PATH."
    exit 1
  fi
done

# 0. Pre-flight Check: Ensure ports 8001 & 8002 are available
echo "🔍 0.1/4: Checking for port conflicts on 8001 & 8002..."
CONFLICT_8001=$(lsof -t -i:8001)
CONFLICT_8002=$(lsof -t -i:8002)

if [ ! -z "$CONFLICT_8001" ]; then
  echo "⚠️  Port 8001 is occupied by PID $CONFLICT_8001. Killing it..."
  kill -9 $CONFLICT_8001
fi

if [ ! -z "$CONFLICT_8002" ]; then
  echo "⚠️  Port 8002 is occupied by PID $CONFLICT_8002. Killing it..."
  kill -9 $CONFLICT_8002
fi

# 1. Update Backend (Docker)
echo "📦 1/4: Rebuilding and restarting Backend Containers (Rooms)..."
docker compose down
docker compose up -d --build

# 2. Catch Cloudflare Tunnel URL
echo "🔍 2/4: Catching Tunnel URL (Monitoring Logs)..."
$PYTHON_EXE catch_url.py

# 3. Build Frontend
echo "🏗️ 3/4: Building Frontend for Production..."
cd frontend
npm run build:prod
cd ..

# 4. Deploy to Firebase
echo "🚀 4/4: Deploying to Firebase Hosting..."
firebase deploy

echo ""
echo "✅ All done! Your AI-Tarot platform is live with the latest Tunnel configuration."
echo "🔗 Access your site at: https://ai-factory-tarot.web.app"
