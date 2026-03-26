"""TTS (Text-to-Speech) 功能模組"""
import os
import socket
import asyncio
import pyttsx3
from pathlib import Path

from core.logger import get_logger
from config import BASE_DIR
from core.config_manager import config_manager

logger = get_logger("tts")

# Note: Using config.py which loaded via config_manager
conf = config_manager.get()
AUDIO_DIR = BASE_DIR / conf.paths.history_dir / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def check_internet(host="8.8.8.8", port=53, timeout=2) -> bool:
    """檢查是否有網路連線"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

def clean_text(text: str) -> str:
    """清理文字，移除 markdown 等無法發音的符號"""
    if not text:
        return ""
    # 簡單移除 markdown 標籤等
    text = text.replace("*", "").replace("#", "").replace("`", "")
    return text

async def _edge_tts_generate(text: str, output_path: str):
    """"使用 edge-tts非同步生成語音"""
    # edge-tts 本身有 python API
    import edge_tts
    conf = config_manager.get()
    VOICE = conf.ai_models.tts_voice
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

async def generate_audio(text: str, record_id: str) -> str | None:
    """
    將文字轉換為語音並回傳檔案路徑 (相對專案根目錄，或絕對路徑)
    
    Args:
        text: 要轉換的文字
        record_id: 作為檔名的一部份
        
    Returns:
        生成的音檔路徑 (絕對路徑字串)，若失敗則回傳 None
    """
    if not text or text == "error" or text.startswith("⚠️"):
        return None
        
    cleaned_text = clean_text(text)
    output_path_mp3 = AUDIO_DIR / f"{record_id}.mp3"
    output_path_wav = AUDIO_DIR / f"{record_id}.wav"
    
    # 如果已經存在，就不重複生成
    if output_path_mp3.exists():
        return str(output_path_mp3)
    if output_path_wav.exists():
        return str(output_path_wav)

    try:
        has_internet = check_internet()
        if has_internet:
            logger.info("檢測到網路連線，使用 edge-tts 生成高音質語音...")
            await _edge_tts_generate(cleaned_text, str(output_path_mp3))
            return str(output_path_mp3)
        else:
            logger.info("無網路連線，使用 pyttsx3 離線生成語音...")
            engine = pyttsx3.init()
            # 調整語速 (依需求微調)
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate - 30) 
            engine.save_to_file(cleaned_text, str(output_path_wav))
            engine.runAndWait()
            return str(output_path_wav)
            
    except Exception as e:
        logger.error(f"語音生成失敗: {e}")
        return None
