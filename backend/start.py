#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("starter")

def start_admin():
    """啟動 Streamlit 管理介面 (預設 Port 10000)"""
    os.environ.setdefault("ACTIVE_CUSTOM_CONFIG", "customer1")
    # 確保 .streamlit/config.toml 會被讀取，或者直接指定 port
    # 由於我們已經有 .streamlit/config.toml (10000)，直接啟動即可
    logger.info("Starting Admin UI (Streamlit) on port 10000...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    subprocess.run(cmd)

def start_api():
    """啟動 FastAPI 提供前端占卜服務 (預設 Port 8000)"""
    os.environ.setdefault("ACTIVE_CUSTOM_CONFIG", "customer2")
    # 從 config 讀取 port
    try:
        from core.config_manager import config_manager
        conf = config_manager.get()
        port = getattr(conf.app, 'api_port', 8000)
    except:
        port = 8000
        
    logger.info(f"Starting API Server (FastAPI) on port {port}...")
    cmd = [
        sys.executable, "-m", "uvicorn", "api.main:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--reload"
    ]
    subprocess.run(cmd)

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="AI-Factory Multi-Tenant Launcher")
    parser.add_argument("module", choices=["admin", "api"], help="Module to start: admin or api")
    parser.add_argument("--profile", help="Override ACTIVE_CUSTOM_CONFIG profile")
    
    args = parser.parse_args()
    
    if args.profile:
        os.environ["ACTIVE_CUSTOM_CONFIG"] = args.profile
        logger.info(f"Custom profile set to: {args.profile}")

    if args.module == "admin":
        start_admin()
    elif args.module == "api":
        start_api()

if __name__ == "__main__":
    main()
